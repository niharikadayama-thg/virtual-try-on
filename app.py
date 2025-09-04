from fastapi import FastAPI, UploadFile, File, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import cv2
import numpy as np
from skimage import color
from colormath.color_objects import LabColor
from colormath.color_diff import delta_e_cie2000
import json
import base64
import io
import os

# Monkey patch numpy to add back the removed asscalar function
if not hasattr(np, 'asscalar'):
    np.asscalar = lambda array: array.item()

# Define Pydantic model for adjust request
class AdjustRequest(BaseModel):
    user_lab: List[float]
    undertone: str
    adjustment: str

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- utils ---
def gray_world_wb(img_bgr):
    img = img_bgr.astype(np.float32)
    avg = img.reshape(-1,3).mean(axis=0)
    scale = avg.mean() / (avg + 1e-6)
    wb = np.clip(img * scale, 0, 255).astype(np.uint8)
    return wb

def bgr_to_lab(img_bgr):
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB) / 255.0
    lab = color.rgb2lab(img_rgb)
    return lab  # float64 HxWx3

def ita_from_lab(lab_pixels):
    L = lab_pixels[...,0]; b = lab_pixels[...,2]
    ita = np.degrees(np.arctan2((L - 50), b + 1e-6))
    return np.nanmedian(ita)

def hue_angle_lab(lab_pixels):
    a = lab_pixels[...,1]; b = lab_pixels[...,2]
    h = (np.degrees(np.arctan2(b, a)) + 360) % 360
    return np.nanmedian(h)

def undertone_from_lab(lab_pixels):
    a = np.nanmedian(lab_pixels[...,1])
    b = np.nanmedian(lab_pixels[...,2])
    h = hue_angle_lab(lab_pixels)
    # very simple heuristic; refine with data:
    if h >= 35 and h <= 85 and b > 12: tone = "warm"
    elif h >= 300 or h <= 20 or a < 6: tone = "cool"
    else: tone = "neutral"
    return tone, float(a), float(b), float(h)

def deltaE2000(lab1, lab2):
    c1 = LabColor(lab_l=lab1[0], lab_a=lab1[1], lab_b=lab1[2])
    c2 = LabColor(lab_l=lab2[0], lab_a=lab2[1], lab_b=lab2[2])
    result = delta_e_cie2000(c1, c2)
    # Handle numpy array result without using deprecated asscalar
    if hasattr(result, 'item'):
        return result.item()
    return float(result)

# quick-and-dirty cheek masks (rects) centered on face box
def cheek_regions(box, H, W):
    x,y,w,h = box
    cx, cy = x + w//2, y + h//2
    side = int(0.18*w)
    off_y = int(0.05*h)
    left  = (max(0, x + int(0.15*w) - side//2), cy + off_y, side, side)
    right = (min(W-side, x + int(0.85*w) - side//2), cy + off_y, side, side)
    fore  = (max(0, cx - side//2), max(0, y + int(0.18*h)), side, side)
    jaw   = (max(0, cx - side//2), min(H-side, y + int(0.75*h)), side, side)
    return [left, right, fore, jaw]

# Try to load face cascade classifier as a fallback method
try:
    # Use Haar cascade for face detection instead of DNN
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    if face_cascade.empty():
        print("Warning: Haar cascade face detector could not be loaded")
        face_cascade = None
    else:
        print("Successfully loaded Haar cascade face detector")
except Exception as e:
    print(f"Warning: Error loading Haar cascade face detector: {e}")
    face_cascade = None

def detect_face(img_bgr):
    """
    Detect faces in an image using OpenCV Haar cascade face detector.
    Returns the bounding box of the largest face found.
    If no face is detected or an error occurs, falls back to a center-based approach.
    This function is configured to ONLY detect faces, not other objects.
    """
    h, w = img_bgr.shape[:2]
    
    # Use the fallback method if face cascade is not loaded
    if face_cascade is None:
        print("Face detector not loaded, using fallback method")
        return (w//4, h//4, w//2, h//2)
    
    try:
        # Convert to grayscale for Haar cascade
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        
        # Detect faces with Haar cascade
        # Parameters: image, scaleFactor, minNeighbors, flags, minSize, maxSize
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
    except Exception as e:
        print(f"Error in face detection: {e}")
        return (w//4, h//4, w//2, h//2)
    
    # If no faces detected, use fallback
    if len(faces) == 0:
        print("No face detected, using fallback method")
        return (w//4, h//4, w//2, h//2)
    
    # Find the largest face (by area)
    largest_face = None
    largest_area = 0
    
    for (x, y, width, height) in faces:
        # Calculate area
        area = width * height
        
        # Skip faces with unusual aspect ratios (faces are roughly square)
        aspect_ratio = width / float(height)
        if aspect_ratio < 0.5 or aspect_ratio > 2.0:
            continue
            
        # Update if this is the largest face
        if area > largest_area:
            largest_area = area
            largest_face = (x, y, width, height)
    
    # If a valid face was found, return it
    if largest_face is not None:
        return largest_face
    
    # Fallback if no valid face was found
    print("No valid face detected, using fallback method")
    return (w//4, h//4, w//2, h//2)

# --- shade catalog ---
# Expanded foundation shade database with more brands and shades
SHADE_DB = [
  # Fenty Beauty
  {"brand":"Fenty Beauty", "shade":"Pro Filt'r 100", "lab":[92.8, 1.2, 10.5], "undertone":"neutral"},
  {"brand":"Fenty Beauty", "shade":"Pro Filt'r 110", "lab":[91.5, 2.5, 11.8], "undertone":"neutral"},
  {"brand":"Fenty Beauty", "shade":"Pro Filt'r 120", "lab":[90.2, 3.0, 12.5], "undertone":"warm"},
  {"brand":"Fenty Beauty", "shade":"Pro Filt'r 140", "lab":[89.8, 3.5, 14.0], "undertone":"neutral"},
  {"brand":"Fenty Beauty", "shade":"Pro Filt'r 150", "lab":[89.5, 3.8, 15.2], "undertone":"warm"},
  {"brand":"Fenty Beauty", "shade":"Pro Filt'r 180", "lab":[85.2, 5.2, 17.5], "undertone":"warm"},
  {"brand":"Fenty Beauty", "shade":"Pro Filt'r 190", "lab":[83.5, 6.0, 18.2], "undertone":"neutral"},
  {"brand":"Fenty Beauty", "shade":"Pro Filt'r 220", "lab":[80.2, 7.5, 19.5], "undertone":"warm"},
  {"brand":"Fenty Beauty", "shade":"Pro Filt'r 240", "lab":[78.5, 8.2, 20.1], "undertone":"neutral"},
  {"brand":"Fenty Beauty", "shade":"Pro Filt'r 260", "lab":[76.0, 9.0, 20.8], "undertone":"neutral"},
  {"brand":"Fenty Beauty", "shade":"Pro Filt'r 290", "lab":[73.5, 9.8, 21.2], "undertone":"neutral"},
  {"brand":"Fenty Beauty", "shade":"Pro Filt'r 330", "lab":[68.2, 11.0, 22.5], "undertone":"warm"},
  {"brand":"Fenty Beauty", "shade":"Pro Filt'r 370", "lab":[62.5, 12.0, 23.0], "undertone":"warm"},
  {"brand":"Fenty Beauty", "shade":"Pro Filt'r 385", "lab":[58.0, 12.5, 23.2], "undertone":"neutral"},
  {"brand":"Fenty Beauty", "shade":"Pro Filt'r 420", "lab":[53.2, 12.8, 23.5], "undertone":"neutral"},
  {"brand":"Fenty Beauty", "shade":"Pro Filt'r 445", "lab":[48.5, 13.0, 22.0], "undertone":"cool"},
  {"brand":"Fenty Beauty", "shade":"Pro Filt'r 470", "lab":[42.0, 12.8, 19.5], "undertone":"neutral"},
  {"brand":"Fenty Beauty", "shade":"Pro Filt'r 490", "lab":[35.2, 12.5, 16.8], "undertone":"neutral"},
  {"brand":"Fenty Beauty", "shade":"Pro Filt'r 498", "lab":[30.5, 12.0, 15.0], "undertone":"cool"},
  
  # Estée Lauder
  {"brand":"Estée Lauder", "shade":"Double Wear 0N1 Alabaster", "lab":[92.0, 2.0, 9.0], "undertone":"neutral"},
  {"brand":"Estée Lauder", "shade":"Double Wear 1C0 Shell", "lab":[90.5, 2.8, 9.8], "undertone":"cool"},
  {"brand":"Estée Lauder", "shade":"Double Wear 1N1 Ivory Nude", "lab":[89.0, 3.0, 10.5], "undertone":"neutral"},
  {"brand":"Estée Lauder", "shade":"Double Wear 1W1 Bone", "lab":[88.5, 3.2, 12.0], "undertone":"warm"},
  {"brand":"Estée Lauder", "shade":"Double Wear 1W2 Sand", "lab":[87.0, 3.5, 13.5], "undertone":"warm"},
  {"brand":"Estée Lauder", "shade":"Double Wear 2C0 Cool Vanilla", "lab":[85.5, 3.8, 11.5], "undertone":"cool"},
  {"brand":"Estée Lauder", "shade":"Double Wear 2C3 Fresco", "lab":[82.1, 4.5, 12.3], "undertone":"cool"},
  {"brand":"Estée Lauder", "shade":"Double Wear 2N1 Desert Beige", "lab":[80.5, 5.0, 14.0], "undertone":"neutral"},
  {"brand":"Estée Lauder", "shade":"Double Wear 2W1 Dawn", "lab":[79.0, 5.5, 16.0], "undertone":"warm"},
  {"brand":"Estée Lauder", "shade":"Double Wear 3C1 Dusk", "lab":[75.0, 7.0, 15.0], "undertone":"cool"},
  {"brand":"Estée Lauder", "shade":"Double Wear 3N1 Ivory Beige", "lab":[73.0, 7.5, 17.0], "undertone":"neutral"},
  {"brand":"Estée Lauder", "shade":"Double Wear 3W1 Tawny", "lab":[70.0, 8.5, 19.0], "undertone":"warm"},
  {"brand":"Estée Lauder", "shade":"Double Wear 4C1 Outdoor Beige", "lab":[67.0, 9.5, 18.0], "undertone":"cool"},
  {"brand":"Estée Lauder", "shade":"Double Wear 4N1 Shell Beige", "lab":[65.0, 10.0, 20.0], "undertone":"neutral"},
  {"brand":"Estée Lauder", "shade":"Double Wear 4W1 Honey Bronze", "lab":[62.3, 11.5, 24.2], "undertone":"warm"},
  {"brand":"Estée Lauder", "shade":"Double Wear 5C1 Rich Chestnut", "lab":[55.0, 12.0, 19.0], "undertone":"cool"},
  {"brand":"Estée Lauder", "shade":"Double Wear 5N1 Rich Ginger", "lab":[52.0, 12.5, 21.0], "undertone":"neutral"},
  {"brand":"Estée Lauder", "shade":"Double Wear 5W1 Bronze", "lab":[50.0, 13.0, 23.0], "undertone":"warm"},
  {"brand":"Estée Lauder", "shade":"Double Wear 6C1 Rich Cocoa", "lab":[45.0, 13.5, 18.0], "undertone":"cool"},
  {"brand":"Estée Lauder", "shade":"Double Wear 6N1 Mocha", "lab":[42.0, 14.0, 19.0], "undertone":"neutral"},
  {"brand":"Estée Lauder", "shade":"Double Wear 6W1 Sandalwood", "lab":[40.0, 14.5, 21.0], "undertone":"warm"},
  {"brand":"Estée Lauder", "shade":"Double Wear 7C1 Rich Mahogany", "lab":[35.0, 13.5, 17.0], "undertone":"cool"},
  {"brand":"Estée Lauder", "shade":"Double Wear 7N1 Deep Amber", "lab":[32.0, 13.0, 16.0], "undertone":"neutral"},
  {"brand":"Estée Lauder", "shade":"Double Wear 8N1 Espresso", "lab":[29.8, 12.8, 15.5], "undertone":"neutral"},
  
  # MAC Cosmetics
  {"brand":"MAC Cosmetics", "shade":"Studio Fix NC10", "lab":[89.7, 3.5, 11.2], "undertone":"warm"},
  {"brand":"MAC Cosmetics", "shade":"Studio Fix NW10", "lab":[89.5, 3.0, 9.5], "undertone":"cool"},
  {"brand":"MAC Cosmetics", "shade":"Studio Fix NC15", "lab":[87.0, 4.0, 12.5], "undertone":"warm"},
  {"brand":"MAC Cosmetics", "shade":"Studio Fix NW15", "lab":[86.8, 3.8, 10.0], "undertone":"cool"},
  {"brand":"MAC Cosmetics", "shade":"Studio Fix NC20", "lab":[85.0, 4.5, 14.0], "undertone":"warm"},
  {"brand":"MAC Cosmetics", "shade":"Studio Fix NW20", "lab":[84.5, 4.2, 11.5], "undertone":"cool"},
  {"brand":"MAC Cosmetics", "shade":"Studio Fix NC25", "lab":[82.5, 5.8, 17.5], "undertone":"warm"},
  {"brand":"MAC Cosmetics", "shade":"Studio Fix NW25", "lab":[82.0, 5.5, 13.0], "undertone":"cool"},
  {"brand":"MAC Cosmetics", "shade":"Studio Fix NC30", "lab":[79.0, 7.0, 19.0], "undertone":"warm"},
  {"brand":"MAC Cosmetics", "shade":"Studio Fix NW30", "lab":[78.5, 6.5, 15.0], "undertone":"cool"},
  {"brand":"MAC Cosmetics", "shade":"Studio Fix NC35", "lab":[75.0, 8.0, 20.5], "undertone":"warm"},
  {"brand":"MAC Cosmetics", "shade":"Studio Fix NW35", "lab":[74.5, 7.5, 16.5], "undertone":"cool"},
  {"brand":"MAC Cosmetics", "shade":"Studio Fix NC40", "lab":[70.0, 9.5, 22.0], "undertone":"warm"},
  {"brand":"MAC Cosmetics", "shade":"Studio Fix NW40", "lab":[69.5, 9.0, 18.0], "undertone":"cool"},
  {"brand":"MAC Cosmetics", "shade":"Studio Fix NC42", "lab":[65.8, 11.2, 23.5], "undertone":"warm"},
  {"brand":"MAC Cosmetics", "shade":"Studio Fix NW42", "lab":[65.0, 10.5, 19.5], "undertone":"cool"},
  {"brand":"MAC Cosmetics", "shade":"Studio Fix NC45", "lab":[60.0, 12.5, 24.0], "undertone":"warm"},
  {"brand":"MAC Cosmetics", "shade":"Studio Fix NW45", "lab":[43.5, 15.8, 22.5], "undertone":"cool"},
  {"brand":"MAC Cosmetics", "shade":"Studio Fix NC50", "lab":[50.0, 14.0, 23.0], "undertone":"warm"},
  {"brand":"MAC Cosmetics", "shade":"Studio Fix NW50", "lab":[49.5, 13.5, 20.0], "undertone":"cool"},
  {"brand":"MAC Cosmetics", "shade":"Studio Fix NC55", "lab":[45.0, 14.5, 22.0], "undertone":"warm"},
  {"brand":"MAC Cosmetics", "shade":"Studio Fix NW55", "lab":[44.5, 14.0, 19.0], "undertone":"cool"},
  {"brand":"MAC Cosmetics", "shade":"Studio Fix NC60", "lab":[40.0, 14.0, 20.0], "undertone":"warm"},
  {"brand":"MAC Cosmetics", "shade":"Studio Fix NW60", "lab":[39.5, 13.5, 17.0], "undertone":"cool"},
  
  # NARS
  {"brand":"NARS", "shade":"Natural Radiant Oslo", "lab":[91.0, 2.5, 10.0], "undertone":"neutral"},
  {"brand":"NARS", "shade":"Natural Radiant Mont Blanc", "lab":[85.2, 4.1, 12.8], "undertone":"neutral"},
  {"brand":"NARS", "shade":"Natural Radiant Deauville", "lab":[82.0, 5.0, 15.0], "undertone":"neutral"},
  {"brand":"NARS", "shade":"Natural Radiant Fiji", "lab":[80.0, 5.5, 16.5], "undertone":"warm"},
  {"brand":"NARS", "shade":"Natural Radiant Punjab", "lab":[75.0, 7.0, 18.0], "undertone":"warm"},
  {"brand":"NARS", "shade":"Natural Radiant Vallauris", "lab":[72.0, 8.0, 17.0], "undertone":"neutral"},
  {"brand":"NARS", "shade":"Natural Radiant Barcelona", "lab":[70.0, 9.0, 19.0], "undertone":"warm"},
  {"brand":"NARS", "shade":"Natural Radiant Stromboli", "lab":[68.0, 9.5, 20.0], "undertone":"warm"},
  {"brand":"NARS", "shade":"Natural Radiant Syracuse", "lab":[64.5, 10.8, 22.8], "undertone":"warm"},
  {"brand":"NARS", "shade":"Natural Radiant Tahoe", "lab":[60.0, 11.5, 23.0], "undertone":"warm"},
  {"brand":"NARS", "shade":"Natural Radiant Cadiz", "lab":[55.0, 12.0, 22.0], "undertone":"warm"},
  {"brand":"NARS", "shade":"Natural Radiant Sammy", "lab":[50.0, 12.5, 21.0], "undertone":"neutral"},
  {"brand":"NARS", "shade":"Natural Radiant Huahine", "lab":[45.0, 13.0, 20.0], "undertone":"neutral"},
  {"brand":"NARS", "shade":"Natural Radiant Macao", "lab":[34.5, 13.2, 17.5], "undertone":"warm"},
  {"brand":"NARS", "shade":"Natural Radiant Trinidad", "lab":[30.0, 12.5, 16.0], "undertone":"neutral"},
  
  # Maybelline
  {"brand":"Maybelline", "shade":"Fit Me 102 Fair Porcelain", "lab":[90.0, 2.8, 10.5], "undertone":"neutral"},
  {"brand":"Maybelline", "shade":"Fit Me 110 Porcelain", "lab":[88.5, 3.2, 11.0], "undertone":"cool"},
  {"brand":"Maybelline", "shade":"Fit Me 115 Ivory", "lab":[87.0, 3.5, 12.0], "undertone":"warm"},
  {"brand":"Maybelline", "shade":"Fit Me 120 Classic Ivory", "lab":[85.5, 4.0, 13.0], "undertone":"neutral"},
  {"brand":"Maybelline", "shade":"Fit Me 125 Nude Beige", "lab":[83.0, 4.5, 14.0], "undertone":"warm"},
  {"brand":"Maybelline", "shade":"Fit Me 130 Buff Beige", "lab":[80.0, 5.0, 15.0], "undertone":"neutral"},
  {"brand":"Maybelline", "shade":"Fit Me 220 Natural Beige", "lab":[75.0, 6.5, 17.0], "undertone":"neutral"},
  {"brand":"Maybelline", "shade":"Fit Me 230 Natural Buff", "lab":[70.0, 8.0, 19.0], "undertone":"warm"},
  {"brand":"Maybelline", "shade":"Fit Me 310 Sun Beige", "lab":[65.0, 9.5, 20.0], "undertone":"warm"},
  {"brand":"Maybelline", "shade":"Fit Me 330 Toffee", "lab":[60.0, 11.0, 21.0], "undertone":"warm"},
  {"brand":"Maybelline", "shade":"Fit Me 355 Coconut", "lab":[50.0, 12.0, 20.0], "undertone":"neutral"},
  {"brand":"Maybelline", "shade":"Fit Me 375 Java", "lab":[40.0, 13.0, 18.0], "undertone":"neutral"},
  
  # L'Oréal
  {"brand":"L'Oréal", "shade":"True Match W1 Porcelain", "lab":[91.0, 2.5, 11.0], "undertone":"warm"},
  {"brand":"L'Oréal", "shade":"True Match C1 Alabaster", "lab":[90.5, 2.0, 9.5], "undertone":"cool"},
  {"brand":"L'Oréal", "shade":"True Match N1 Ivory", "lab":[90.0, 2.2, 10.0], "undertone":"neutral"},
  {"brand":"L'Oréal", "shade":"True Match W3 Nude Beige", "lab":[85.0, 4.0, 14.0], "undertone":"warm"},
  {"brand":"L'Oréal", "shade":"True Match C3 Creamy Natural", "lab":[84.5, 3.5, 11.5], "undertone":"cool"},
  {"brand":"L'Oréal", "shade":"True Match N3 Natural Buff", "lab":[84.0, 3.8, 12.5], "undertone":"neutral"},
  {"brand":"L'Oréal", "shade":"True Match W5 Sand Beige", "lab":[75.0, 7.0, 18.0], "undertone":"warm"},
  {"brand":"L'Oréal", "shade":"True Match C5 Classic Beige", "lab":[74.5, 6.5, 15.0], "undertone":"cool"},
  {"brand":"L'Oréal", "shade":"True Match N5 True Beige", "lab":[74.0, 6.8, 16.5], "undertone":"neutral"},
  {"brand":"L'Oréal", "shade":"True Match W7 Caramel Beige", "lab":[65.0, 10.0, 21.0], "undertone":"warm"},
  {"brand":"L'Oréal", "shade":"True Match C7 Nut Brown", "lab":[64.5, 9.5, 18.0], "undertone":"cool"},
  {"brand":"L'Oréal", "shade":"True Match N7 Amber", "lab":[64.0, 9.8, 19.5], "undertone":"neutral"},
  {"brand":"L'Oréal", "shade":"True Match W9 Mahogany", "lab":[45.0, 13.0, 19.0], "undertone":"warm"},
  {"brand":"L'Oréal", "shade":"True Match C9 Deep Cool", "lab":[44.5, 12.5, 16.0], "undertone":"cool"},
  {"brand":"L'Oréal", "shade":"True Match N9 Cocoa", "lab":[44.0, 12.8, 17.5], "undertone":"neutral"}
]

def recommend_shades(user_lab, undertone, topk=5):
    scored = []
    for row in SHADE_DB:
        # prefer same undertone but still allow close matches
        penalty = 0 if row["undertone"]==undertone else 1.5
        de = deltaE2000(user_lab, row["lab"]) + penalty
        scored.append((de, row))
    scored.sort(key=lambda x: x[0])
    return [{"brand":r["brand"],"shade":r["shade"],"undertone":r["undertone"],"deltaE":round(d,2)} 
            for d,r in scored[:topk]]

def ita_to_mst(ita):
    # Map ITA to approximate Monk Skin Tone scale (1-10)
    if ita > 55: return 1
    elif ita > 41: return 2
    elif ita > 35: return 3
    elif ita > 28: return 4
    elif ita > 19: return 5
    elif ita > 10: return 6
    elif ita > 0: return 7
    elif ita > -15: return 8
    elif ita > -30: return 9
    else: return 10

# Update the AdjustRequest model to include fine adjustments
class FineAdjustments(BaseModel):
    lightness: int
    warmth: int
    saturation: int

class AdjustRequest(BaseModel):
    user_lab: List[float]
    undertone: str
    adjustment: str
    fine_adjustments: Optional[FineAdjustments] = None

@app.post("/adjust")
async def adjust(request: AdjustRequest):
    # Extract parameters from request
    user_lab = request.user_lab
    current_undertone = request.undertone
    adjustment = request.adjustment
    fine_adjustments = request.fine_adjustments
    
    # Apply adjustments to LAB values
    adjusted_lab = user_lab.copy()
    adjusted_undertone = current_undertone
    
    # Handle preset adjustments
    if adjustment == "lighter":
        adjusted_lab[0] = min(100, adjusted_lab[0] + 5)  # Increase L by 5, max 100
    elif adjustment == "darker":
        adjusted_lab[0] = max(0, adjusted_lab[0] - 5)    # Decrease L by 5, min 0
    elif adjustment == "neutral":
        # Move a and b values closer to neutral
        adjusted_lab[1] = adjusted_lab[1] * 0.7  # Reduce a (green-red)
        adjusted_lab[2] = adjusted_lab[2] * 0.7  # Reduce b (blue-yellow)
        adjusted_undertone = "neutral"
    elif adjustment == "warm":
        # Increase a and b for warmer tone
        adjusted_lab[1] = min(25, adjusted_lab[1] * 1.2)  # Increase a (more red)
        adjusted_lab[2] = min(30, adjusted_lab[2] * 1.2)  # Increase b (more yellow)
        adjusted_undertone = "warm"
    elif adjustment == "cool":
        # Decrease a and increase b slightly for cooler tone
        adjusted_lab[1] = max(-10, adjusted_lab[1] * 0.8)  # Decrease a (less red)
        adjusted_lab[2] = max(5, adjusted_lab[2] * 0.9)    # Decrease b (less yellow)
        adjusted_undertone = "cool"
    # Handle fine-grained adjustments
    elif adjustment == "fine" and fine_adjustments:
        # Apply lightness adjustment (L value)
        lightness_factor = fine_adjustments.lightness * 0.5  # Scale factor (each slider unit = 0.5 L)
        adjusted_lab[0] = min(100, max(0, adjusted_lab[0] + lightness_factor))
        
        # Apply warmth adjustment (affects a and b values)
        warmth_factor = fine_adjustments.warmth * 0.3  # Scale factor
        if warmth_factor > 0:  # Warmer
            adjusted_lab[1] = min(25, adjusted_lab[1] + warmth_factor)  # Increase a (more red)
            adjusted_lab[2] = min(30, adjusted_lab[2] + warmth_factor)  # Increase b (more yellow)
            if warmth_factor > 2:  # If significant warmth adjustment
                adjusted_undertone = "warm"
        else:  # Cooler
            adjusted_lab[1] = max(-10, adjusted_lab[1] + warmth_factor)  # Decrease a (less red)
            adjusted_lab[2] = max(5, adjusted_lab[2] + warmth_factor * 0.5)  # Decrease b (less yellow)
            if warmth_factor < -2:  # If significant cool adjustment
                adjusted_undertone = "cool"
        
        # Apply saturation adjustment (affects chroma/intensity of a and b)
        saturation_factor = fine_adjustments.saturation * 0.1  # Scale factor
        if saturation_factor > 0:  # More saturated
            chroma_multiplier = 1 + saturation_factor / 10
            adjusted_lab[1] = adjusted_lab[1] * chroma_multiplier
            adjusted_lab[2] = adjusted_lab[2] * chroma_multiplier
        else:  # More neutral
            chroma_multiplier = 1 + saturation_factor / 10  # Will be < 1 for negative values
            adjusted_lab[1] = adjusted_lab[1] * chroma_multiplier
            adjusted_lab[2] = adjusted_lab[2] * chroma_multiplier
            if saturation_factor < -5:  # If significant neutralizing
                adjusted_undertone = "neutral"
    
    # Calculate ITA value for the adjusted LAB
    ita = np.degrees(np.arctan2((adjusted_lab[0] - 50), adjusted_lab[2] + 1e-6))
    
    # Map ITA to MST scale
    mst_level = ita_to_mst(ita)
    
    # Get new recommendations based on adjusted values
    recs = recommend_shades(adjusted_lab, adjusted_undertone, topk=5)
    
    return {
        "ITA": round(ita, 1),
        "user_lab": [round(v, 2) for v in adjusted_lab],
        "undertone": adjusted_undertone,
        "mst_level": mst_level,
        "recommendations": recs
    }

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    data = np.frombuffer(await file.read(), np.uint8)
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if img is None:
        return JSONResponse({"error":"bad image"}, status_code=400)

    img = gray_world_wb(img)
    box = detect_face(img)
    if box is None:
        return JSONResponse({"error":"no face detected"}, status_code=422)

    H,W = img.shape[:2]
    lab = bgr_to_lab(img)
    patches = []
    for (x,y,w,h) in cheek_regions(box, H, W):
        patch = lab[y:y+h, x:x+w, :]
        if patch.size: patches.append(patch.reshape(-1,3))
    if not patches:
        return JSONResponse({"error":"sampling failed"}, status_code=500)

    allpix = np.vstack(patches)
    # reject extreme pixels (hair/shadow) via luminance & simple chroma clip
    L = allpix[:,0]; A = allpix[:,1]; B = allpix[:,2]
    mask = (L>20)&(L<95)&(np.sqrt(A*A+B*B)<40)
    allpix = allpix[mask]
    ita = float(ita_from_lab(allpix))
    undertone, a_med, b_med, hue = undertone_from_lab(allpix)
    user_lab = [float(np.median(allpix[:,0])), float(np.median(allpix[:,1])), float(np.median(allpix[:,2]))]

    # Map ITA to MST scale
    mst_level = ita_to_mst(ita)

    recs = recommend_shades(user_lab, undertone, topk=5)
    return {
      "ITA": round(ita,1),
      "user_lab": [round(v,2) for v in user_lab],
      "undertone": undertone,
      "hue_angle": round(hue,1),
      "mst_level": mst_level,
      "recommendations": recs
    }

@app.post("/try-on")
async def try_on(request: AdjustRequest):
    """
    Apply virtual foundation try-on to the user's image.
    This endpoint applies the selected foundation shade to the user's face.
    """
    # Extract parameters from request
    user_lab = request.user_lab
    
    # Create a blank image (300x300) with the foundation shade
    width, height = 300, 300
    # Create a simple Lab image
    lab_image = np.zeros((height, width, 3), dtype=np.float32)
    lab_image[:, :, 0] = user_lab[0]  # L channel
    lab_image[:, :, 1] = user_lab[1]  # a channel
    lab_image[:, :, 2] = user_lab[2]  # b channel
    
    # Convert to BGR
    bgr_image = cv2.cvtColor(lab_image.astype(np.float32), cv2.COLOR_Lab2BGR)
    bgr_image = (bgr_image * 255).astype(np.uint8)
    
    # Create a circular mask to simulate a face
    mask = np.zeros((height, width), dtype=np.uint8)
    center = (width // 2, height // 2)
    radius = min(width, height) // 3
    cv2.circle(mask, center, radius, 255, -1)
    
    # Add some facial features (simplified)
    # Eyes
    eye_radius = radius // 5
    left_eye = (center[0] - radius // 2, center[1] - radius // 4)
    right_eye = (center[0] + radius // 2, center[1] - radius // 4)
    cv2.circle(bgr_image, left_eye, eye_radius, (255, 255, 255), 2)
    cv2.circle(bgr_image, right_eye, eye_radius, (255, 255, 255), 2)
    
    # Mouth
    mouth_width = radius
    mouth_height = radius // 3
    cv2.ellipse(bgr_image, (center[0], center[1] + radius // 3),
                (mouth_width // 2, mouth_height), 0, 0, 180, (255, 255, 255), 2)
    
    # Encode the image to base64 for sending to frontend
    _, buffer = cv2.imencode('.jpg', bgr_image)
    img_str = base64.b64encode(buffer).decode('utf-8')
    
    return {
        "try_on_image": f"data:image/jpeg;base64,{img_str}",
        "user_lab": user_lab
    }

@app.get("/")
async def root():
    return FileResponse("frontend/index.html")

# Mount the static files directory
app.mount("/", StaticFiles(directory="frontend"), name="frontend")