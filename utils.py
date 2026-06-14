import cv2
import numpy as np

def load_video_frames(video_path, max_frames=10, target_size=(64,64)):
    cap = cv2.VideoCapture(video_path)
    frames = []
    while len(frames) < max_frames:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, target_size)
        frames.append(frame)
    cap.release()

    # Pad if less than max_frames
    while len(frames) < max_frames:
        frames.append(np.zeros_like(frames[0]))

    frames = np.array(frames) / 255.0
    return np.expand_dims(frames, axis=0)  # shape: (1, max_frames, H, W, C)
