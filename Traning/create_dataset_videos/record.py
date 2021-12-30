import numpy as np
from cv2 import cv2
import mediapipe as mp
import sys
import os


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


def record_video(output_path, word, num_of_frames, mp_holistic_model, holistic_model, mp_drawing):
    # create output path 
    output_path = os.path.join(output_path, f"videos_with_{num_of_frames}_frames", word)
    os.makedirs(output_path, exist_ok=True)
    video_id = len(os.listdir(output_path))
    
    # read the video frames and save it in a list
    cap = cv2.VideoCapture(0)
    cap.set(3, 600)
    cap.set(4, 600)
    cap.set(10, 50)
    success, frame = cap.read()

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    while True:
        image, results = detect_keypoints(frame, holistic_model)
        no_text_image = np.copy(image)
        draw_landmarks(mp_drawing, mp_holistic_model, image, results)
        success, frame = cap.read()
        key_input = cv2.waitKey(1)
        frame_number = 1
        current_status_string = "Normal"
        cv2.putText(image, current_status_string, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
        cv2.imshow(f"Rec: {word}", image)
        if key_input == ord('r'):
            count = 3
            while count > 0:
                image = np.copy(no_text_image)
                current_status_string = f"Start Recording in {count} seconds."
                cv2.putText(image, current_status_string, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)
                count -= 1
                cv2.imshow(f"Rec: {word}", image)
                cv2.waitKey(1000)

            # video writer
            out = cv2.VideoWriter(os.path.join(output_path, f'{video_id}.mp4'),
                                  cv2.VideoWriter_fourcc(*'DIVX'), 20, (width, height))

            while frame_number <= num_of_frames:
                image, results = detect_keypoints(frame, holistic_model)
                draw_landmarks(mp_drawing, mp_holistic_model, image, results)
                current_status_string = f"Recording."
                cv2.putText(image, current_status_string, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                cv2.imshow(f"Rec: {word}", image)
                success, frame = cap.read()
                out.write(frame)
                frame_number += 1
                cv2.waitKey(1)
            video_id += 1
            out.release()
        elif key_input == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def main(argv):
    if len(argv) == 3:
        try:
            frames = int(argv[2])
        except ValueError:
            print("number of frames should be integer.")
            return

        mp_holistic_model = mp.solutions.holistic
        mp_drawing = mp.solutions.drawing_utils
        holistic = mp_holistic_model.Holistic(min_detection_confidence=0.7, min_tracking_confidence=0.7)

        record_video(".", argv[1], frames, mp_holistic_model, holistic, mp_drawing)

    elif len(argv) < 3:
        print("you should enter the input the word and the number of frames.")


if __name__ == "__main__":
    main(sys.argv)
