from flask import Flask, request, jsonify
import cv2
import numpy as np
from model import model

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['image']
    file_path = f'uploads/{file.filename}'
    file.save(file_path)

    # Run the ML model
    likelihood = model(file_path)
    return jsonify({'likelihood_cancerous': likelihood})
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')