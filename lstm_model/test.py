import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from cv2 import KeyPoint, cv2
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
import mediapipe as mp
import os


def read_labels(path):
    names_list = os.listdir(path)
    equ_num_list = list(range(len(names_list)))
    num_of_videos_list = []
    
    for i in range(len(names_list)):
        sub_path = os.path.join(path, names_list[i])
        nov = len(os.listdir(sub_path))
        num_of_videos_list.append(nov)
    print(names_list)   
    df = pd.DataFrame(list(zip(names_list, equ_num_list, num_of_videos_list)), columns=['names', 'values', 'num_of_videos'])
    return df.set_index('names').iloc[:, 0].to_dict(), df.set_index('names').iloc[:, 1].to_dict()



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



def start_stream(mp_holistic_model, holistic_model, mp_drawing, model, actions, sequence_length):

    sequence = []
    sentence = []
    predictions = []
    threshold = 0.75

    # read the video frames and save it in a list
    cap = cv2.VideoCapture(1)
    cap.set(3, 600)
    cap.set(4, 600)
    cap.set(10, 0)
    success, frame = cap.read()
    res = []
    while success:    
        image, results = detect_keypoints(frame, holistic_model)
        draw_landmarks(mp_drawing, mp_holistic_model, image, results)

        KeyPoints = extract_keypoints(results)

        sequence.append(KeyPoints)
        sequence = sequence[-sequence_length:]


        if len(sequence) == sequence_length:
            res = model.predict(np.expand_dims(sequence, axis=0))[0]
            predictions.append(np.argmax(res))
            # print(actions[np.argmax(res)])

        if len(predictions)> 0 and np.unique(predictions[-15:])[0] == np.argmax(res):
            if res[np.argmax(res)] > threshold:
                if len(sentence) > 0:
                    if actions[np.argmax(res)] != sentence[-1]:
                        sentence.append(actions[np.argmax(res)])
                else:
                    sentence.append(actions[np.argmax(res)])
        

        cv2.imshow(f"Rec", image)
        key_input = cv2.waitKey(1)
        success, frame = cap.read()
        
        if key_input == ord('q'):
            break
	
        yield sentence

    cap.release()
    cv2.destroyAllWindows()    
    

def main(argv):
    actions_map, num_of_videos = read_labels('dataset')
    
    sequence_length = 40
    
    model = tf.keras.models.load_model('cv_model.h5')
    
    actions = list(actions_map.keys())
    
    mp_holistic_model = mp.solutions.holistic
    mp_drawing = mp.solutions.drawing_utils
    holistic = mp_holistic_model.Holistic(min_detection_confidence=0.7, min_tracking_confidence=0.5)
    

    for sentence in start_stream(mp_holistic_model, holistic, mp_drawing, model, actions, sequence_length):
        print(sentence)
    
    
            
if __name__ == '__main__':
    main('')    
