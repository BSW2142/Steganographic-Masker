from PIL import Image
import io
import math

def resize_image(image, required_pixels, increment=0.1):
    width, height = image.size
    current_pixels = width * height

    factor = 1.0
    while current_pixels < required_pixels * 1.1 and factor <= 2.0:  # Adding 10% buffer
        factor += increment
        new_size = (int(width * factor), int(height * factor))
        new_image = image.resize(new_size, Image.Resampling.LANCZOS)
        current_pixels = new_size[0] * new_size[1]
        print(f"Resized image to {new_size}, total pixels: {current_pixels}")
        image = new_image

    return image

def compress_image(file_path):
    img = Image.open(file_path)
    buffer = io.BytesIO()
    img.convert('RGB').save(buffer, format='JPEG', quality=50)
    return buffer.getvalue()
