from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import json, os
import numpy as np

from model import model
from utils import load_video_frames

app = Flask(__name__)

# Load dataset mapping
with open("sign_map.json", "r", encoding="utf-8") as f:
    SIGN_MAP = json.load(f)

# 🎤 Speech-to-text
def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Speak now...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        return text.lower().strip()
    except:
        return ""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/record", methods=["POST"])
def record():
    text = speech_to_text()
    return jsonify({"text": text})

@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json()
    text = data.get("text", "").lower().strip()
    words = text.split()
    videos = []

    for word in words:
        if word in SIGN_MAP:
            video_path = "static/" + SIGN_MAP[word]

            # ---- CNN+RNN prediction ----
            frames = load_video_frames(video_path)
            y_pred = model.predict(frames)
            predicted_class = int(np.argmax(y_pred))
            print(f"✅ Predicted class for '{word}': {predicted_class}")

            videos.append({"word": word, "video": "/" + video_path})
        else:
            videos.append({"word": word, "error": f"No video found for '{word}'"}) 

    return jsonify({"videos": videos})

if __name__ == "__main__":
    app.run(debug=True)
