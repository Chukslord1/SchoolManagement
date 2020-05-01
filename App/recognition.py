import cv2
import face_recognition
import base64
import io
import os
import numpy as np
from imageio import imread

def get_face_encoding(image):
    face_encoding = face_recognition.face_encodings(image)[0]
    return {
        "face_encoding": face_encoding
    }

def match_encoding(image, db_encodings):
    face_encoding = get_face_encoding(image)["face_encoding"]

    matches = face_recognition.compare_faces(db_encodings[0], face_encoding)
    name = "Unknown"

    face_distances = face_recognition.face_distance(db_encodings[0], face_encoding)
    best_match_index = np.argmin(face_distances)
    if matches[best_match_index]:
        name = db_encodings[1][best_match_index]

    if name != "Unknown":
        return {
            "valid": True,
            "face_encoding": face_encoding,
            "name": name
        }
    else:
        return {
            "valid": False,
            "name": name
        }

def save_new_encoding(image, name, testing=False):
    face_encoding = get_face_encoding(image)["face_encoding"]
    if testing:
        return face_encoding, name
    else:
        # add encoding and name to db
        db_encodings = [[], []]

        # save as a 2D array; face on left, name on right
        db_encodings[0].append(face_encoding)
        db_encodings[1].append(name)

def base64_to_img(base64):
    image = imread(io.BytesIO(base64.b64decode(base64)))
    return {
        "image": image
    }

def imgfile_to_img(file):
    image = cv2.cvtColor(cv2.imread(file), cv2.COLOR_BGR2RGB)
    return {
        "image": image
    }

def run_test():
    base_path = "test/"
    known_dir = "known/"
    others_dir = "others/"

    known_images = [[], []]
    for file in os.listdir(os.path.join(base_path, known_dir)):
        face_encoding, name = save_new_encoding(imgfile_to_img(os.path.join(base_path, known_dir, file))["image"], file, True)
        known_images[0].append(face_encoding)
        known_images[1].append(name)

    for file in os.listdir(os.path.join(base_path, others_dir)):
        match = match_encoding(imgfile_to_img(os.path.join(base_path, others_dir, file))["image"], known_images)
        if match["valid"]:
            print("Registered face", match["name"])
        else:
            print("Unregistered face", match["name"])
