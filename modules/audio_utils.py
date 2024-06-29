from pydub import AudioSegment
import io

def compress_audio(file_path):
    audio = AudioSegment.from_file(file_path)
    buffer = io.BytesIO()
    audio.export(buffer, format='mp3', bitrate='32k')  # Reduce bitrate further
    return buffer.getvalue()

def read_audio(file_path):
    with open(file_path, "rb") as f:
        return f.read()

def save_audio(data, output_file):
    audio = AudioSegment.from_file(io.BytesIO(data), format="mp3")
    audio.export(output_file, format="mp3")
