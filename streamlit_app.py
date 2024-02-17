import streamlit as st

if not hasattr(st, 'already_started_server'):
    # Hack the fact that Python modules (like st) only load once to
    # keep track of whether this file already ran.
    st.already_started_server = True

    st.write('''
        The first time this script executes it will run forever because it's
        running a Flask server.

        Just close this browser tab and open a new one to see your Streamlit
        app.
    ''')

    from flask import Flask, request
    import cv2 as cv
    import numpy as np
    from detectors.chess_position_detector import ChessPositionDetector

    app = Flask(__name__)

    @app.route('/')
    def hello_chess_snapshot():
        return 'Hello, Chess Snapshot!'

    @app.route('/get_chess_position', methods=['POST'])
    def get_chess_position():
        if 'image' not in request.files:
            return 'No image uploaded', 400

        image_file = request.files['image']
        image_bytes = image_file.read()

        nparr = np.frombuffer(image_bytes, np.uint8)
        original_image = cv.imdecode(nparr, cv.IMREAD_COLOR)

        chess_position_detector = ChessPositionDetector()
        fen = chess_position_detector.detect(original_image)

        return { 'fen': fen }

    app.run(port=8888)


# We'll never reach this part of the code the first time this file executes!

# Your normal Streamlit app goes here:
x = st.slider('Pick a number')
st.write('You picked:', x)