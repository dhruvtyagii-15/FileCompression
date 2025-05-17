
import numpy as np
import cv2

def dct_1d(vector):
    N = len(vector)
    result = np.zeros(N)
    for k in range(N):
        coeff = np.sqrt(1 / N) if k == 0 else np.sqrt(2 / N)
        result[k] = coeff * np.sum(vector * np.cos(np.pi * (2 * np.arange(N) + 1) * k / (2 * N)))
    return result

def idct_1d(vector):
    N = len(vector)
    result = np.zeros(N)
    for n in range(N):
        sum_val = 0
        for k in range(N):
            coeff = np.sqrt(1 / N) if k == 0 else np.sqrt(2 / N)
            sum_val += coeff * vector[k] * np.cos(np.pi * (2 * n + 1) * k / (2 * N))
        result[n] = sum_val
    return result

def dct2(channel):
    return np.array([dct_1d(row) for row in channel]).T @ np.array([dct_1d(row) for row in channel.T]).T

def idct2(channel):
    return np.array([idct_1d(row) for row in channel]).T @ np.array([idct_1d(row) for row in channel.T]).T

def compress_image_color_dct(input_path, output_path, keep_fraction=0.1):
    image = cv2.imread(input_path)
    image = np.float32(image)

    compressed_channels = []
    for i in range(3):  # B, G, R channels
        channel = image[:, :, i]
        dct_channel = dct2(channel)

        # Zero high frequencies
        h, w = dct_channel.shape
        mask = np.zeros_like(dct_channel)
        h_keep = int(h * keep_fraction)
        w_keep = int(w * keep_fraction)
        mask[:h_keep, :w_keep] = 1
        dct_channel *= mask

        idct_channel = idct2(dct_channel)
        idct_channel = np.clip(idct_channel, 0, 255)
        compressed_channels.append(idct_channel)

    compressed_img = cv2.merge([np.uint8(c) for c in compressed_channels])
    cv2.imwrite(output_path, compressed_img)
