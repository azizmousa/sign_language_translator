import numpy as np
import tensorflow as tf
import mediapipe as mp
from cv2 import cv2


def read_labels(labels_path):
    """
    def read_labels(labels_path)

    function to read labels from names file

    Args:
        labels_path (str): names file path

    Returns: dictionary of labels, id pairs.

    """
    with open(labels_path, 'r') as names_file:
        lines = names_file.read()
    i = 0
    names_dict = {}
    for word in lines.split('\n'):
        names_dict[word] = i
        i += 1
    return names_dict


class Model:
    """
    Model class is a class to start continuous stream from the input source and classify the motions of
    sign language to words

    Attributes:
        sequence_length (int): the length of the sequence that the model already trained on

        __model (keras_model): the model that will predict the signs

        __actions (list): list of labels

        __mp_holistic_model (object): object that control the holistic model

        __mp_drawing (object): object to control the drawing utils

        __holistic (object): the holistic model to detect the landmarks

        __stream_source (int/str): the input source i.e. (camera/video)

        __display_keypoint (bool): True if you want to display landmarks on the output image
                                False otherwise

        __display_window (bool): True if you want the class to display the output window
                              False otherwise

    """

    def __init__(self, stream_source, sequence_length, model_path, labels_path,
                 display_keypoint=False, display_window=True):
        actions_map = read_labels(labels_path)

        self.__sequence_length = sequence_length

        self.__model = tf.keras.models.load_model(model_path)

        self.__actions = list(actions_map.keys())

        self.__mp_holistic_model = mp.solutions.holistic
        self.__mp_drawing = mp.solutions.drawing_utils
        self.__holistic = self.__mp_holistic_model.Holistic(min_detection_confidence=0.7, min_tracking_confidence=0.5)
        self.__stream_source = stream_source

        self.__display_keypoint = display_keypoint
        self.__display_window = display_window

    def detect_keypoints(self, image):
        """
        detect the keypoints from an input image

        Args:
            image (2d-np-array): the input image

        Returns:
            image: the input image,
            results: the keypoints results

        """
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.__holistic.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        return image, results

    def draw_landmarks(self, image, results):
        """
        function to draw the landmarks on the input image

        Args:
            image: input image that you want to draw the landmarks on
            results: the landmarks that you want to draw

        Returns:
            None

        """
        self.__mp_drawing.draw_landmarks(image, results.face_landmarks, self.__mp_holistic_model.FACEMESH_CONTOURS,
                                         self.__mp_drawing.DrawingSpec(color=(10, 194, 80), thickness=1, circle_radius=1),
                                         self.__mp_drawing.DrawingSpec(color=(214, 200, 80), thickness=1, circle_radius=1))
        self.__mp_drawing.draw_landmarks(image, results.pose_landmarks, self.__mp_holistic_model.POSE_CONNECTIONS,
                                         self.__mp_drawing.DrawingSpec(color=(90, 194, 80), thickness=2, circle_radius=4),
                                         self.__mp_drawing.DrawingSpec(color=(230, 200, 80), thickness=2, circle_radius=4))
        self.__mp_drawing.draw_landmarks(image, results.right_hand_landmarks, self.__mp_holistic_model.HAND_CONNECTIONS,
                                         self.__mp_drawing.DrawingSpec(color=(20, 194, 80), thickness=2, circle_radius=4),
                                         self.__mp_drawing.DrawingSpec(color=(190, 200, 80), thickness=2, circle_radius=4))
        self.__mp_drawing.draw_landmarks(image, results.left_hand_landmarks, self.__mp_holistic_model.HAND_CONNECTIONS,
                                         self.__mp_drawing.DrawingSpec(color=(20, 194, 80), thickness=2, circle_radius=4),
                                         self.__mp_drawing.DrawingSpec(color=(190, 200, 80), thickness=2, circle_radius=4))

    def extract_keypoints(self, results):
        """
        function to extrack the keypoints from the landmarks

        Args:
            results: object that contains the keypoints

        Returns:
            np-array that contain all keypoints sequentially

        """
        # face_landmarks = np.array([[lm.x, lm.y, lm.z] for lm in
        #                            results.face_landmarks.landmark]).flatten() \
        #     if results.face_landmarks else np.zeros(468 * 3)
        pose_landmarks = np.array([[lm.x, lm.y, lm.z, lm.visibility] for lm in
                                   results.pose_landmarks.landmark]).flatten() \
            if results.pose_landmarks else np.zeros(33 * 4)
        right_hand_landmarks = np.array([[lm.x, lm.y, lm.z] for lm in
                                         results.right_hand_landmarks.landmark]).flatten() \
            if results.right_hand_landmarks else np.zeros(21 * 3)
        left_hand_landmarks = np.array([[lm.x, lm.y, lm.z] for lm in
                                        results.left_hand_landmarks.landmark]).flatten() \
            if results.left_hand_landmarks else np.zeros(21 * 3)
        return np.concatenate([pose_landmarks, left_hand_landmarks, right_hand_landmarks])

    def start_stream(self):
        """
        function to start the source input and predict the sign language from the source

        Returns:
            generator of the predicted words

        """
        sequence = []
        sentence = []
        predictions = []
        threshold = 0.75

        # read the video frames and save it in a list
        cap = cv2.VideoCapture(self.__stream_source)
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
            sequence = sequence[-self.__sequence_length:]

            if len(sequence) == self.__sequence_length:
                res = self.__model.predict(np.expand_dims(sequence, axis=0))[0]
                predictions.append(np.argmax(res))

            display = frame
            if self.__display_keypoint:
                display = image
            if self.__display_window:
                cv2.imshow(f"Stream", display)
            key_input = cv2.waitKey(1)
            success, frame = cap.read()

            if key_input == ord('q'):
                break

            if len(predictions) > 0 and np.unique(predictions[-18:])[0] == np.argmax(res):
                if res[np.argmax(res)] > threshold:
                    if len(sentence) > 0:
                        if self.__actions[np.argmax(res)] != sentence[-1]:
                            sentence.append(self.__actions[np.argmax(res)])
                            yield sentence[-1], display
                    else:
                        sentence.append(self.__actions[np.argmax(res)])
                        yield sentence[-1], display

            yield '', display

        cap.release()
        cv2.destroyAllWindows()
