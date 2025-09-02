import urllib.request
import os
import sys

def download_file(url, filename):
    """Download a file from a URL to a local file."""
    print(f"Downloading {filename}...")
    try:
        urllib.request.urlretrieve(url, filename)
        print(f"Successfully downloaded {filename}")
        return True
    except Exception as e:
        print(f"Error downloading {filename}: {e}")
        return False

def main():
    # URL for the face detection model
    model_url = "https://github.com/opencv/opencv_3rdparty/raw/dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000.caffemodel"
    model_filename = "res10_300x300_ssd_iter_140000_fp16.caffemodel"
    
    # Check if the model file already exists
    if os.path.exists(model_filename):
        print(f"Model file {model_filename} already exists.")
        overwrite = input("Do you want to download it again? (y/n): ")
        if overwrite.lower() != 'y':
            print("Download canceled.")
            return
    
    # Download the model file
    success = download_file(model_url, model_filename)
    
    if success:
        print("\nModel file downloaded successfully.")
        print("You can now run the application with: ./start.sh")
    else:
        print("\nFailed to download the model file.")
        print("Please download it manually from:")
        print(model_url)
        print(f"And save it as {model_filename} in the project directory.")

if __name__ == "__main__":
    main()