import os
from PIL import Image
from modules.encoding import encode_enc, decode_image, calculate_required_pixels, SIGNATURE
from modules.image_utils import resize_image, compress_image
from modules.audio_utils import compress_audio, save_audio
from modules.crypto_utils import encrypt_data, decrypt_data
from modules.video_utils import compress_video, save_video, embed_video, extract_video, is_video
from modules.search_utils import search_image, search_video, is_encrypted

def get_file_paths(file_type):
    if file_type == "text":
        hidden_path = input("Enter the text you want to hide: ")
        carrier_path = input("Enter the path of the carrier image to hide the text into (with extension): ")
    elif file_type == "image":
        hidden_path = input("Enter the path of the image you want to hide: ")
        carrier_path = input("Enter the path of the carrier image to hide the data into (with extension): ")
    elif file_type == "audio":
        hidden_path = input("Enter the path of the audio file you want to hide: ")
        carrier_path = input("Enter the path of the carrier image to hide the audio into (with extension): ")
    elif file_type == "video":
        hidden_path = input("Enter the path of the video file you want to hide: ")
        carrier_path = input("Enter the path of the carrier video to hide the data into (with extension): ")
    else:
        raise ValueError("Unsupported file type.")
    return hidden_path, carrier_path

def process_encryption(data):
    encrypt = input("Do you want to encrypt the data? (yes/no): ").lower() == 'yes'
    if encrypt:
        password = input("Enter a password for encryption: ")
        data = encrypt_data(password, data)
        data = b'encrypted:' + data
    return data

def encode_text(text, carrier_path):
    data = text.encode()
    carrier_image = Image.open(carrier_path, 'r')
    return data, carrier_image

def encode_image(hidden_path, carrier_path):
    data = compress_image(hidden_path)
    carrier_image = Image.open(carrier_path, 'r')
    return data, carrier_image

def encode_audio(hidden_path, carrier_path):
    data = compress_audio(hidden_path)
    carrier_image = Image.open(carrier_path, 'r')
    return data, carrier_image

def encode_video(hidden_path, carrier_path):
    data = compress_video(hidden_path)
    return data, carrier_path

def encode():
    file_type = input("Enter the type of file to hide (text/audio/image/video): ").lower()
    hidden_path, carrier_path = get_file_paths(file_type)

    if file_type == "text":
        data, carrier = encode_text(hidden_path, carrier_path)
    elif file_type == "image":
        data, carrier = encode_image(hidden_path, carrier_path)
    elif file_type == "audio":
        data, carrier = encode_audio(hidden_path, carrier_path)
    elif file_type == "video":
        data, carrier_path = encode_video(hidden_path, carrier_path)
    else:
        raise ValueError('Unsupported file type.')

    if not data:
        raise ValueError('Data is empty')

    data = process_encryption(data)

    if is_video(carrier_path):
        output_file = input("Enter the name of the new video (with extension): ")
        embed_video(carrier_path, data, output_file)
        print(f"Data encoded successfully into {output_file}")
    else:
        required_pixels = calculate_required_pixels(len(data))
        current_pixels = carrier.size[0] * carrier.size[1]
        print(f"Required pixels: {required_pixels}")

        if required_pixels > current_pixels * 0.9:
            carrier = resize_image(carrier, required_pixels)

        for attempt in range(10):
            try:
                encode_enc(carrier, data)
                break
            except StopIteration:
                print(f"Encoding failed on attempt {attempt + 1}, resizing image by 10%")
                carrier = resize_image(carrier, required_pixels, increment=0.1)
                if carrier.size[0] * carrier.size[1] >= required_pixels * 1.1:
                    print(f"Resized image size: {carrier.size}, total pixels: {carrier.size[0] * carrier.size[1]}")
            else:
                raise ValueError('Unable to fit data into image even after maximum resizing attempts.')

        new_img_name = input("Enter the name of the new image (without extension): ")
        carrier.save(f"{new_img_name}.png", "PNG")
        print(f"Data encoded successfully into {new_img_name}.png")

def decode_data(data, file_type):
    if data.startswith(b'encrypted:'):
        data = data[len(b'encrypted:'):]
        password = input("Enter the password for decryption: ")
        try:
            data = decrypt_data(password, data)
        except Exception as e:
            print("Decryption failed. Incorrect password or corrupted data.")
            return

    if file_type == "text":
        decoded_text = data.decode('utf-8', errors='ignore')
        print(f"Decoded Text: {decoded_text}")
    else:
        output_file = input("Enter the name of the output file (with extension): ")
        with open(output_file, "wb") as f:
            f.write(data)
        if file_type == "audio":
            save_audio(data, output_file)
        print(f"Data decoded successfully into {output_file}")

def decode():
    file_type = input("Enter the type of file to decode (text/audio/image/video): ").lower()
    carrier_path = input("Enter the path of the carrier file to decode (with extension): ")

    if file_type in ["text", "audio", "image"]:
        carrier = Image.open(carrier_path, 'r')
        data = decode_image(carrier)
        decode_data(data, file_type)

    elif file_type == "video":
        data = extract_video(carrier_path)
        decode_data(data, file_type)

def search():
    file_type = input("Enter the type of file to search (image/video): ").lower()
    carrier_path = input("Enter the path of the carrier file to search (with extension): ")

    if file_type == "image":
        data = search_image(carrier_path)
    elif file_type == "video":
        data = search_video(carrier_path)
    else:
        print("Unsupported file type for search.")
        return

    if data:
        if is_encrypted(data):
            print("Hidden data found and it is encrypted.")
        else:
            print("Hidden data found and it is not encrypted.")
        decode_choice = input("Do you want to decode this data? (yes/no): ").lower()
        if decode_choice == 'yes':
            file_type = input("Enter the type of hidden data (text/audio/image/video): ").lower()
            decode_data(data, file_type)
    else:
        print("No hidden data found.")

def main():
    action = int(input(":: Welcome to Steganography ::\n1. Encode\n2. Decode\n3. Search for Hidden Data\n"))
    if action == 1:
        encode()
    elif action == 2:
        decode()
    elif action == 3:
        search()
    else:
        raise ValueError("Enter correct input")

if __name__ == '__main__':
    main()
