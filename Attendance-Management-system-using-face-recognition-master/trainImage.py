import csv
import os, cv2
import numpy as np
import pandas as pd
import datetime
import time
from PIL import Image

# Train Image
def TrainImage(haarcasecade_path, trainimage_path, trainimagelabel_path, message, text_to_speech):
    # Basic checks
    if not os.path.exists(trainimage_path):
        os.makedirs(trainimage_path, exist_ok=True)

    faces, Ids = getImagesAndLables(trainimage_path)

    if len(faces) == 0 or len(Ids) == 0:
        res = "No training images found. Please capture images first."
        try:
            message.configure(text=res)
        except Exception:
            pass
        text_to_speech(res)
        return

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(faces, np.array(Ids))
    # Ensure label dir exists
    label_dir = os.path.dirname(trainimagelabel_path)
    if label_dir and not os.path.exists(label_dir):
        os.makedirs(label_dir, exist_ok=True)
    recognizer.save(trainimagelabel_path)

    res = "Images trained successfully."
    try:
        message.configure(text=res)
    except Exception:
        pass
    text_to_speech(res)


def getImagesAndLables(path):
    """
    Collect face images and labels from TrainingImage folder.

    Supports both:
      1) All images directly inside TrainingImage folder, OR
      2) Images inside subfolders.

    Expected filename pattern includes an ID after the first underscore:
      e.g. user_100_20250731_213358_1.jpg  -> ID = 100
    """
    valid_exts = {".jpg", ".jpeg", ".png", ".bmp"}
    image_files = []

    # Gather all images directly
    for f in os.listdir(path):
        fp = os.path.join(path, f)
        if os.path.isfile(fp) and os.path.splitext(fp)[1].lower() in valid_exts:
            image_files.append(fp)

    # Also gather from subfolders, if any
    for root, dirs, files in os.walk(path):
        for f in files:
            fp = os.path.join(root, f)
            if os.path.splitext(fp)[1].lower() in valid_exts and fp not in image_files:
                image_files.append(fp)

    faces = []
    Ids = []

    for imagePath in image_files:
        try:
            pilImage = Image.open(imagePath).convert("L")
        except Exception:
            continue  # skip unreadable

        imageNp = np.array(pilImage, "uint8")

        # Extract ID from filename: split by '_' and take index 1
        # Example filename: user_100_20250731_213358_1.jpg
        fname = os.path.basename(imagePath)
        parts = fname.split("_")
        if len(parts) < 2:
            # Fallback: try digits in filename
            num = "".join([ch for ch in fname if ch.isdigit()])
            if num == "":
                continue
            try:
                Id = int(num)
            except Exception:
                continue
        else:
            try:
                Id = int(parts[1])
            except Exception:
                # fallback to digits
                num = "".join([ch for ch in fname if ch.isdigit()])
                if num == "":
                    continue
                try:
                    Id = int(num)
                except Exception:
                    continue

        faces.append(imageNp)
        Ids.append(Id)

    return faces, Ids
