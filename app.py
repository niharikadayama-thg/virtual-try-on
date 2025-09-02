from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import cv2
import numpy as np
from skimage import color
from colormath.color_objects import LabColor
from colormath.color_diff import delta_e_cie2000
import json

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
    return delta_e_cie2000(c1, c2)

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

# very basic face box using OpenCV DNN (or swap with MediaPipe client-side)
try:
    net = cv2.dnn.readNetFromCaffe(
        prototxt="deploy.prototxt",
        caffeModel="res10_300x300_ssd_iter_140000_fp16.caffemodel"
    )
except:
    print("Warning: Face detection model files not found. Please download them.")
    net = None

def detect_face(img_bgr):
    # Use the fallback method for face detection
    # This is a simple approach that assumes the face is in the center of the image
    h, w = img_bgr.shape[:2]
    # Return a box that covers the center portion of the image
    return (w//4, h//4, w//2, h//2)

# --- shade catalog ---
# Example minimal catalog; replace with your brands (LAB, undertone tag)
SHADE_DB = [
  {"brand":"Fenty Beauty", "shade":"Pro Filt'r 100", "lab":[92.8, 1.2, 10.5], "undertone":"neutral"},
  {"brand":"Fenty Beauty", "shade":"Pro Filt'r 150", "lab":[89.5, 3.8, 15.2], "undertone":"warm"},
  {"brand":"Fenty Beauty", "shade":"Pro Filt'r 290", "lab":[73.5, 9.8, 21.2], "undertone":"neutral"},
  {"brand":"Fenty Beauty", "shade":"Pro Filt'r 420", "lab":[53.2, 12.8, 23.5], "undertone":"neutral"},
  {"brand":"Fenty Beauty", "shade":"Pro Filt'r 490", "lab":[35.2, 12.5, 16.8], "undertone":"neutral"},
  
  {"brand":"Estée Lauder", "shade":"Double Wear 1C0 Shell", "lab":[90.5, 2.8, 9.8], "undertone":"cool"},
  {"brand":"Estée Lauder", "shade":"Double Wear 2C3 Fresco", "lab":[82.1, 4.5, 12.3], "undertone":"cool"},
  {"brand":"Estée Lauder", "shade":"Double Wear 4W1 Honey Bronze", "lab":[62.3, 11.5, 24.2], "undertone":"warm"},
  {"brand":"Estée Lauder", "shade":"Double Wear 8N1 Espresso", "lab":[29.8, 12.8, 15.5], "undertone":"neutral"},
  
  {"brand":"MAC Cosmetics", "shade":"Studio Fix NC10", "lab":[89.7, 3.5, 11.2], "undertone":"warm"},
  {"brand":"MAC Cosmetics", "shade":"Studio Fix NC25", "lab":[82.5, 5.8, 17.5], "undertone":"warm"},
  {"brand":"MAC Cosmetics", "shade":"Studio Fix NC42", "lab":[65.8, 11.2, 23.5], "undertone":"warm"},
  {"brand":"MAC Cosmetics", "shade":"Studio Fix NW45", "lab":[43.5, 15.8, 22.5], "undertone":"neutral warm"},
  
  {"brand":"NARS", "shade":"Natural Radiant Mont Blanc", "lab":[85.2, 4.1, 12.8], "undertone":"neutral"},
  {"brand":"NARS", "shade":"Natural Radiant Syracuse", "lab":[64.5, 10.8, 22.8], "undertone":"warm"},
  {"brand":"NARS", "shade":"Natural Radiant Macao", "lab":[34.5, 13.2, 17.5], "undertone":"warm"},
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

@app.get("/")
async def root():
    return FileResponse("frontend/index.html")

# Mount the static files directory
app.mount("/", StaticFiles(directory="frontend"), name="frontend")