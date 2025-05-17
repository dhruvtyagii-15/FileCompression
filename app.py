from flask import Flask, render_template, request, send_file
import os
from huffman import compress_to_file, huffman_decompress

from dct_utils import compress_image_dct
import cv2
import numpy as np

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
COMPRESSED_FOLDER = 'compressed'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(COMPRESSED_FOLDER, exist_ok=True)

# Video compression using FFmpeg (H.265)
def compress_video(input_path, output_path):
    os.system(f"ffmpeg -i \"{input_path}\" -vcodec libx265 -crf 28 \"{output_path}\"")

@app.route('/')
def index():
    return render_template('index.html')

# Text Compression (Huffman)
@app.route('/compress_text', methods=['POST'])
def compress_text_route():
    file = request.files['file']
    if file:
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)
        with open(path, 'r') as f:
            text = f.read()
        out_path = os.path.join(COMPRESSED_FOLDER, file.filename + '.huff')
        compress_to_file(text, out_path)
        return render_template('index.html', text_compressed="Text compressed!", text_compressed_path=out_path)

# Text Decompression (Huffman)
@app.route('/decompress_text', methods=['POST'])
def decompress_text_route():
    file = request.files['file']
    if file:
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)
        text = huffman_decompress(path)
        out_path = os.path.join(COMPRESSED_FOLDER, file.filename.replace('.huff', '_decompressed.txt'))
        with open(out_path, 'w') as f:
            f.write(text)
        return render_template('index.html', text_compressed="Text decompressed using Huffman!", text_compressed_path=out_path)

@app.route('/compress_image', methods=['POST'])
def compress_image_route():
    file = request.files['file']
    if file:
        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        output_path = os.path.join(COMPRESSED_FOLDER, "compressed_" + file.filename)
        file.save(input_path)

        try:
            compress_image_dct(input_path, output_path, keep_fraction=0.2)
        except Exception as e:
            return render_template('index.html', image_compressed=f"❌ Compression failed: {e}")

        if not os.path.exists(output_path):
            return render_template('index.html', image_compressed="❌ Output file not found.")

        return render_template('index.html', image_compressed="✅ Image compressed in color using DCT!", image_compressed_path=output_path)


# Video Compression
@app.route('/compress_video', methods=['POST'])
def compress_video_route():
    file = request.files['file']
    if file:
        in_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(in_path)
        out_path = os.path.join(COMPRESSED_FOLDER, file.filename)
        compress_video(in_path, out_path)
        return render_template('index.html', video_compressed="Video compressed using ffmpeg + DCT", video_compressed_path=out_path)

if __name__ == '__main__':
    app.run(debug=True)
