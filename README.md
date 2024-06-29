## Steganographic-Masker
This steganography program allows you to hide and retrieve text, images, audio, and video files within carrier images and videos. The program also supports encryption to secure the hidden data.

## Features

- **Hide text within images**: Example: "Hello. My name is Brandon." ---> carrier.png
- **Hide images within images**: Hides most image types, but the carrier image is always output as a lossless PNG to preserve hidden data.
- **Hide audio files within images**: Audio is compressed to fit within the pixel budget of carrier.png. The carrier image may be resized up to 10 times by 10% increments before failing.
- **Hide video files within videos**: Only supports .MP4 format. Compression occurs.
- **Option to encrypt hidden data for added security**: AES-256 encryption.

## Prerequisites

- Python 3.x
- Required Python packages:
  - `Pillow`
  - `cryptography`
  - `pydub`
  - `ffmpeg`
