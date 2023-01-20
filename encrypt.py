from PIL import Image
import numpy as np
import math
import random
import os

source_foldet = 'Images/'
destination_folder = 'Encrypted/'

def permutation_2d_henon_sine_map(pixels, a, b, x0, y0):
    x = x0
    y = y0
    permuted_pixels = np.empty(pixels.shape)
    for i in range(pixels.shape[0]):
        x_new = y + 1 - a * (np.sin(x) * np.sin(x))
        y_new = b * x
        x = x_new
        y = y_new

        # Apply the permutation map to the pixels
        permuted_pixels[i] = pixels[int(x) % pixels.shape[0]]

    indices = list(range(len(pixels)))
    random.shuffle(indices)
    permuted_pixels = np.zeros(len(pixels))
    for i in range(len(pixels)):
        permuted_pixels[i] = pixels[indices[i]]
    return permuted_pixels

def encrypt(img_grey, a, b, x0, y0):
    # Convert the image to a 1D array of pixels
    pixels = np.array(img_grey).flatten() 

    # Apply the permutation map to the pixels
    permuted_pixels = permutation_2d_henon_sine_map(pixels, a, b, x0, y0)

    dna_bases = ['A', 'C', 'G', 'T']
    encrypted_pixels = [dna_bases[int(p) % 4] for p in permuted_pixels]

    # Save the DNA sequence to a file
    # with open("encrypted_image.dna", "w") as f:
    #     f.write("".join(encrypted_pixels))

    return encrypted_pixels   
    
def dna_to_image(encrypted_pixels):
    # Convert the DNA sequence to a 1D array of pixels
    scale_values = np.empty(len(encrypted_pixels))

    # Convert the DNA bases to pixel values
    base_values = {'A': 0, 'C': 64, 'G': 128, 'T': 255}
    for i in range(len(encrypted_pixels)):
        scale_values[i] = base_values[encrypted_pixels[i]]
    return scale_values

def main_encrypt():
    a = 1.4
    b = 0.3
    x0 = 0.1
    y0 = 0.1

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    for file in os.listdir(source_foldet):
        img = Image.open(os.path.join(source_foldet, file))
        (m, n) = img.size
        img_grey = img.convert('L')
        encrypted_pixels = encrypt(img_grey, a, b, x0, y0)

        image = dna_to_image(encrypted_pixels).reshape(n, m)
        img_encrypted = Image.fromarray(image)

        img_encrypted = img_encrypted.convert('RGB')
        img_encrypted.save(os.path.join(destination_folder, 'encrypted_' + file))

if __name__ == "__main__":
    # for encrypting
    main_encrypt()
