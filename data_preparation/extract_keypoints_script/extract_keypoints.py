import pandas as pd
import numpy as np
from cv2 import cv2
import sys
import os
import datetime
import mediapipe as mp
from ast import literal_eval


def detect_keypoints(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = model.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return image, results


def draw_landmarks(mp_drawing, mp_holistic_model, image, results):
    mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic_model.FACEMESH_CONTOURS, 
                             mp_drawing.DrawingSpec(color=(10, 194, 80), thickness=1, circle_radius=1), 
                             mp_drawing.DrawingSpec(color=(214, 200, 80), thickness=1, circle_radius=1))
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic_model.POSE_CONNECTIONS, 
                             mp_drawing.DrawingSpec(color=(90, 194, 80), thickness=2, circle_radius=4), 
                             mp_drawing.DrawingSpec(color=(230, 200, 80), thickness=2, circle_radius=4))
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic_model.HAND_CONNECTIONS, 
                             mp_drawing.DrawingSpec(color=(20, 194, 80), thickness=2, circle_radius=4), 
                             mp_drawing.DrawingSpec(color=(190, 200, 80), thickness=2, circle_radius=4))
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic_model.HAND_CONNECTIONS, 
                             mp_drawing.DrawingSpec(color=(20, 194, 80), thickness=2, circle_radius=4), 
                             mp_drawing.DrawingSpec(color=(190, 200, 80), thickness=2, circle_radius=4))


def extract_keypoints(results):
    face_landmarks = np.array([[lm.x, lm.y, lm.z] for lm in results.face_landmarks.landmark]).flatten()if results.face_landmarks else np.zeros(468*3)
    pose_landmarks = np.array([[lm.x, lm.y, lm.z, lm.visibility] for lm in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
    righ_hand_landmarks = np.array([[lm.x, lm.y, lm.z] for lm in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
    left_hand_landmarks = np.array([[lm.x, lm.y, lm.z] for lm in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
    return np.concatenate([pose_landmarks, face_landmarks, left_hand_landmarks, righ_hand_landmarks])


def create_word_folders(output_path, word, num_of_videos):
    print(f"create {word} directory.")
    main_path = os.path.join(output_path, "keypoints", word)
    os.makedirs(main_path, exist_ok=True)
    for i in range(num_of_videos):
        print(f"\tcreate video number ({i}) directory.")
        os.makedirs(os.path.join(main_path, str(i)), exist_ok=True)


def create_np_keypoints_file(videos_path, videos_extention, output_path, mp_drawing, mp_holistic_model, word, videos_list, row_index, holistic_model, start_time):
    print(f"extracting the keypoints for ({word}) of index -> ({row_index}).")

    for i in range(len(videos_list)):
        print(f"\textracting the keypoints from video number ({i}) ...")
        cap = cv2.VideoCapture(os.path.join(videos_path, f"{videos_list[i]}.{videos_extention}"))
        success = success, frame = cap.read()
        frame_number = 1
        while cap.isOpened() and success:
            frame = cv2.resize(frame, (600, 600))
            image, results = detect_keypoints(frame, holistic_model)
            draw_landmarks(mp_drawing, mp_holistic_model, image, results)
    
            keypoints = extract_keypoints(results)
            save_path = os.path.join(output_path, "keypoints", word, str(i), f"frame_{frame_number}")
            np.savez_compressed(save_path, keypoints)

            keypoints = None
            del keypoints

            success, frame = cap.read()
            frame_number += 1

        cap.release()
        cv2.destroyAllWindows()
    end = datetime.datetime.now()
    print(f"\tprocess took about: {end-start_time}")


def main(argv):
    
    mp_holistic_model = mp.solutions.holistic
    mp_drawing = mp.solutions.drawing_utils 
    holistic = mp_holistic_model.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    
    dataset = pd.read_csv("gloss_videos.csv")
    dataset['videos_ids'] = dataset['videos_ids'].apply(literal_eval)

    dataset.apply(lambda row: create_word_folders(".", row['gloss'], len(row['videos_ids'])), axis=1)
    start = datetime.datetime.now()
    
    if len(argv) == 4:
        dataset.apply(lambda row: create_np_keypoints_file(argv[1], argv[3], argv[2], mp_drawing, mp_holistic_model, 
                            row['gloss'], row['videos_ids'], row.name, holistic, start), axis=1)
    elif len(argv) == 3:
        dataset.apply(lambda row: create_np_keypoints_file(argv[1], argv[2], ".", mp_drawing, mp_holistic_model, 
                            row['gloss'], row['videos_ids'], row.name, holistic, start), axis=1)
    elif len(argv) < 3:
        print("you should enter the input path and the videos extention.")


if __name__ == "__main__":
    main(sys.argv)
