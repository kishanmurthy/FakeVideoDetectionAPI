import torch
from model import BATFD
import cv2
import numpy as np

check_point = "./weights/baftd_default.ckpt"
model = BATFD.load_from_checkpoint(check_point)

from flask import Flask, jsonify, request
app = Flask(__name__)

def preprocess_video(video_path, height=128, width=128):
    cap = cv2.VideoCapture(video_path)
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (height, width), interpolation=cv2.INTER_LINEAR)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB).astype(np.float32)
        frame -= [123.68, 116.779, 103.939]  # subtract RGB mean
        frame /= 255.0  # scale pixel values to [0, 1]
        frames.append(frame)
    cap.release()
    return np.array(frames)

@app.route("/predict", methods = ["POST"])
def predict():
    video_path = request.join["video_path"]
    video_data = preprocess_video(video_path)
    with torch.no_grad():
        output = model(video_data)
    return jsonify({"output": output.tolist()})

if __name__ == "__main__":
    app.run(debug = True)




