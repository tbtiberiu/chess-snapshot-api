import cv2 as cv
import numpy as np

from flask import Flask, request, jsonify
from detectors.chess_position_detector import ChessPositionDetector


app = Flask(__name__)

@app.route('/')
def hello_chess_snapshot():
    return 'Hello, Chess Snapshot!'

@app.route('/api/get_chess_position', methods=['POST'])
def get_chess_position():
    if 'image' not in request.files:
        return 'No image uploaded', 400

    image_file = request.files['image']
    image_bytes = image_file.read()

    nparr = np.frombuffer(image_bytes, np.uint8)
    original_image = cv.imdecode(nparr, cv.IMREAD_COLOR)

    chess_position_detector = ChessPositionDetector()
    fen = chess_position_detector.detect(original_image)

    return jsonify({'fen': fen})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
