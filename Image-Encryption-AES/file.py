from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from PIL import Image
import os


def pad(data):
    length = 16 - (len(data) % 16)
    return data + bytes([length]) * length


def encrypt(data, key):
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    encryptor = cipher.encryptor()
    return encryptor.update(pad(data)) + encryptor.finalize()


def decrypt(encrypted_data, key):
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
    return padded_data[:-padded_data[-1]]

def hide_data(original_image_path, data_to_hide):
    img = Image.open(original_image_path)
    data_size = len(data_to_hide)

 
    img.putpixel((0, 0), (data_size >> 24, data_size >> 16, data_size >> 8, data_size))
    
    
    for i in range(1, data_size + 1):
        img.putpixel((i % img.width, i // img.width), (data_to_hide[i - 1],))
    
    return img


def extract_data(hidden_image_path, data_size):
    img = Image.open(hidden_image_path)
    extracted_data = []
  
    for i in range(1, data_size + 1):
        extracted_data.append(img.getpixel((i % img.width, i // img.width))[0])
    
    return bytes(extracted_data)


def main():
   
    original_image_path = "orig.jpeg"
    data_to_hide = b"Secret message to hide!"

    aes_key = os.urandom(32)

   
    encrypted_data = encrypt(data_to_hide, aes_key)

    
    hidden_image = hide_data(original_image_path, encrypted_data)
    hidden_image.save("hid.jpeg")

 
    extracted_data = extract_data("hid.jpeg", len(encrypted_data))

    decrypted_data = decrypt(extracted_data, aes_key)

    print("Original Data:", data_to_hide)
    print("Decrypted Data:", decrypted_data)

if __name__ == "__main__":
    main()
