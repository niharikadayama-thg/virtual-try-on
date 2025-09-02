#!/bin/bash

echo "Starting Foundation Shade Finder..."
echo "Make sure you have installed the required dependencies:"
echo "pip install -r requirements.txt"
echo ""

# Check if the model file exists
if [ ! -f "res10_300x300_ssd_iter_140000_fp16.caffemodel" ]; then
    echo "Warning: Face detection model file not found."
    echo "Please download res10_300x300_ssd_iter_140000_fp16.caffemodel and place it in this directory."
    echo "You can download it from: https://github.com/opencv/opencv_3rdparty/blob/dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000.caffemodel"
    echo ""
fi

# Start the server
echo "Starting server on http://localhost:8000..."
echo "Open your browser and navigate to http://localhost:8000"
python3 -m uvicorn app:app --reload --port 8000 &
SERVER_PID=$!

# Function to handle script termination
function cleanup {
    echo "Stopping server..."
    kill $SERVER_PID
    exit
}

# Set up trap to catch termination signals
trap cleanup SIGINT SIGTERM

echo ""
echo "Servers are running. Press Ctrl+C to stop."
echo ""

# Keep the script running
wait