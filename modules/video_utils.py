import os
import subprocess
import io

def compress_video(file_path):
    compressed_path = "compressed.mp4"
    command = [
        "ffmpeg",
        "-i", file_path,
        "-vcodec", "libx264",
        "-crf", "28",
        compressed_path
    ]
    subprocess.run(command, check=True)
    with open(compressed_path, "rb") as f:
        compressed_data = f.read()
    os.remove(compressed_path)
    return compressed_data

def save_video(data, output_file):
    with open(output_file, "wb") as f:
        f.write(data)

def embed_video(carrier_path, hidden_data, output_path):
    with open(carrier_path, "rb") as carrier_file:
        carrier_data = carrier_file.read()
    combined_data = carrier_data + b":::" + hidden_data  # Separator to distinguish data
    with open(output_path, "wb") as output_file:
        output_file.write(combined_data)

def extract_video(carrier_path):
    with open(carrier_path, "rb") as carrier_file:
        carrier_data = carrier_file.read()
    carrier_data, hidden_data = carrier_data.split(b":::", 1)
    return hidden_data

def is_video(file_path):
    return file_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))
