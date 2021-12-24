import os
import numpy as np
import tensorflow as tf
import mediapipe as mp
from cv2 import cv2


def read_labels():
    with open(os.path.join('model', 'names'), 'r') as names_file:
        lines = names_file.read()
    i = 0
    names_dict = {}
    for word in lines.split('\n'):
        names_dict[word] = i
        i += 1
    return names_dict


class Model:

    def __init__(self, stream_source, sequence_length, display_keypoint=False, display_window=True):
        actions_map = read_labels()

        self.sequence_length = sequence_length

        self.model = tf.keras.models.load_model(os.path.join('model', 'cv_model.h5'))

        self.actions = list(actions_map.keys())

        self.mp_holistic_model = mp.solutions.holistic
        self.mp_drawing = mp.solutions.drawing_utils
        self.holistic = self.mp_holistic_model.Holistic(min_detection_confidence=0.7, min_tracking_confidence=0.5)
        self.stream_source = stream_source

        self.display_keypoint = display_keypoint
        self.display_window = display_window

    def detect_keypoints(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.holistic.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        return image, results

    def draw_landmarks(self, image, results):
        self.mp_drawing.draw_landmarks(image, results.face_landmarks, self.mp_holistic_model.FACEMESH_CONTOURS,
                                       self.mp_drawing.DrawingSpec(color=(10, 194, 80), thickness=1, circle_radius=1),
                                       self.mp_drawing.DrawingSpec(color=(214, 200, 80), thickness=1, circle_radius=1))
        self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.mp_holistic_model.POSE_CONNECTIONS,
                                       self.mp_drawing.DrawingSpec(color=(90, 194, 80), thickness=2, circle_radius=4),
                                       self.mp_drawing.DrawingSpec(color=(230, 200, 80), thickness=2, circle_radius=4))
        self.mp_drawing.draw_landmarks(image, results.right_hand_landmarks, self.mp_holistic_model.HAND_CONNECTIONS,
                                       self.mp_drawing.DrawingSpec(color=(20, 194, 80), thickness=2, circle_radius=4),
                                       self.mp_drawing.DrawingSpec(color=(190, 200, 80), thickness=2, circle_radius=4))
        self.mp_drawing.draw_landmarks(image, results.left_hand_landmarks, self.mp_holistic_model.HAND_CONNECTIONS,
                                       self.mp_drawing.DrawingSpec(color=(20, 194, 80), thickness=2, circle_radius=4),
                                       self.mp_drawing.DrawingSpec(color=(190, 200, 80), thickness=2, circle_radius=4))

    def extract_keypoints(self, results):
        face_landmarks = np.array([[lm.x, lm.y, lm.z] for lm in
                                   results.face_landmarks.landmark]).flatten() \
            if results.face_landmarks else np.zeros(468 * 3)
        pose_landmarks = np.array([[lm.x, lm.y, lm.z, lm.visibility] for lm in
                                   results.pose_landmarks.landmark]).flatten() \
            if results.pose_landmarks else np.zeros(33 * 4)
        right_hand_landmarks = np.array([[lm.x, lm.y, lm.z] for lm in
                                         results.right_hand_landmarks.landmark]).flatten() \
            if results.right_hand_landmarks else np.zeros(21 * 3)
        left_hand_landmarks = np.array([[lm.x, lm.y, lm.z] for lm in
                                        results.left_hand_landmarks.landmark]).flatten() \
            if results.left_hand_landmarks else np.zeros(21 * 3)
        return np.concatenate([pose_landmarks, face_landmarks, left_hand_landmarks, right_hand_landmarks])

    def start_stream(self):

        sequence = []
        sentence = []
        predictions = []
        threshold = 0.75

        # read the video frames and save it in a list
        cap = cv2.VideoCapture(self.stream_source)
        cap.set(3, 600)
        cap.set(4, 600)
        cap.set(10, 0)
        success, frame = cap.read()
        res = []
        while success:
            image, results = self.detect_keypoints(frame)
            self.draw_landmarks(image, results)

            KeyPoints = self.extract_keypoints(results)

            sequence.append(KeyPoints)
            sequence = sequence[-self.sequence_length:]

            if len(sequence) == self.sequence_length:
                res = self.model.predict(np.expand_dims(sequence, axis=0))[0]
                predictions.append(np.argmax(res))

            if len(predictions) > 0 and np.unique(predictions[-15:])[0] == np.argmax(res):
                if res[np.argmax(res)] > threshold:
                    if len(sentence) > 0:
                        if self.actions[np.argmax(res)] != sentence[-1]:
                            sentence.append(self.actions[np.argmax(res)])
                    else:
                        sentence.append(self.actions[np.argmax(res)])

            display = frame
            if self.display_keypoint:
                display = image
            if self.display_window:
                cv2.imshow(f"Rec", display)
            key_input = cv2.waitKey(1)
            success, frame = cap.read()

            if key_input == ord('q'):
                break

            yield sentence, display

        cap.release()
        cv2.destroyAllWindows()
