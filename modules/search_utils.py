from PIL import Image
from modules.encoding import decode_image, SIGNATURE
from modules.video_utils import extract_video, is_video

def search_image(image_path):
    if not image_path.lower().endswith('.png'):
        print("Only PNG images are supported for searching.")
        return None
    
    try:
        image = Image.open(image_path, 'r')
        data = decode_image(image)
        if data is not None:
            return data
        else:
            print("No signature found. Checking for other hidden data...")
            # Add heuristic checks for other hidden data here if needed
    except Exception as e:
        print(f"Error searching image: {e}")
    return None

def search_video(video_path):
    if not video_path.lower().endswith('.mp4'):
        print("Only MP4 videos are supported for searching.")
        return None
    
    try:
        data = extract_video(video_path)
        if data.startswith(SIGNATURE):
            return data[len(SIGNATURE):]
        else:
            print("No signature found. Checking for other hidden data...")
            # Add heuristic checks for other hidden data here if needed
    except Exception as e:
        print(f"Error searching video: {e}")
    return None

def is_encrypted(data):
    return data.startswith(b'encrypted:')

