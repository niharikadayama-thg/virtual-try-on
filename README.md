# Foundation Shade Finder

A web application that analyzes face images to recommend foundation shades that match your skin tone.

## Overview

Foundation Shade Finder uses computer vision and color science to detect your skin tone and undertone, then recommends foundation shades from popular brands that would be a good match for your complexion.

The application consists of:

- A FastAPI backend for face detection and skin tone analysis
- A simple HTML/CSS/JS frontend for user interaction

## Features

- Face detection using OpenCV
- Skin tone analysis using CIELAB color space
- Individual Typology Angle (ITA) calculation for objective skin tone measurement
- Undertone detection
- Foundation shade recommendations from multiple brands
- User feedback controls to adjust recommendations
- Webcam support for real-time analysis

## Installation

1. Clone this repository
2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```
3. Download the face detection model files:
   - You need to download the `res10_300x300_ssd_iter_140000_fp16.caffemodel` file
   - Place it in the root directory alongside the `deploy.prototxt` file
   - You can download it from [here](https://github.com/opencv/opencv_3rdparty/blob/dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000.caffemodel)

## How to Run

1. Start the FastAPI backend:
   ```
   uvicorn app:app --reload --port 8000
   ```
2. Open the frontend in your browser:
   ```
   # If you have Python installed:
   python -m http.server 8080 --directory frontend
   ```
   Then navigate to http://localhost:8080

## How It Works

1. **Image Capture**: Upload a selfie taken in daylight with indirect light and no heavy makeup, or use your webcam.

2. **Face Detection**: The application uses OpenCV's DNN module to detect facial landmarks.

3. **Skin Sampling**: It samples skin color from your cheeks, forehead, and jawline, avoiding areas like eyes, lips, and brows.

4. **White Balance Correction**: A Gray World algorithm is applied to neutralize color cast and ensure consistency.

5. **Color Analysis**:

   - Converts sampled pixels to CIELAB color space
   - Calculates ITA (Individual Typology Angle)
   - Determines skin tone category and undertone

6. **Shade Matching**: Matches your skin tone to foundation shades in the database using color distance in LAB space.

7. **User Feedback**: You can adjust results to be lighter, darker, warmer, cooler, or more neutral.

## Technologies Used

- **Backend**:

  - FastAPI for the API server
  - OpenCV for face detection
  - NumPy for numerical operations
  - scikit-image for color space conversions
  - colormath for color difference calculations

- **Frontend**:
  - HTML/CSS/JavaScript
  - Bootstrap for styling
  - Fetch API for communication with the backend

## Future Improvements

- Expand the foundation shade database
- Add more brands and products
- Improve undertone detection
- Implement user accounts to save preferences
- Add product purchase links
- Integrate with MediaPipe for more accurate face landmark detection
- Implement a mobile app version

## References

- ITA (Individual Typology Angle) is a well-established metric in dermatology for objective skin tone classification
- The Monk Skin Tone (MST) scale provides an inclusive framework for skin tone representation
