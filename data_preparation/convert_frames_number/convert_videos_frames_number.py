import pandas as pd
import numpy as np
from cv2 import cv2
import sys
import os


def cut_videos(input_path, output_path, word, video_id, row_index, num_of_frames):
    print(f"processing video frames number >> Word:({word}), Video Id:({video_id}), data index -> ({row_index}).")
    
    # create output path 
    output_path = os.path.join(output_path, f"videos_with_{num_of_frames}_frames")
    os.makedirs(output_path, exist_ok=True)
    
    # read the video frames and save it in a list
    cap = cv2.VideoCapture(os.path.join(input_path, str(video_id)+".mp4"))
    success = success, frame = cap.read()
    frame_number = 1
    frames_list = []
    while cap.isOpened() and success and frame_number <= num_of_frames:
        frame = cv2.resize(frame, (600, 600))
        frames_list.append(frame)
        success, frame = cap.read()

        frame_number += 1
    

    # fill the rest of the frames with blank frame
    if frame_number < num_of_frames:
        blank_image = np.zeros((600, 600, 3), np.uint8)
        blank_list = [blank_image] * (num_of_frames - frame_number)
        frames_list.extend(blank_list)

    # video writer
    out = cv2.VideoWriter(os.path.join(output_path, f'{video_id}.avi'),cv2.VideoWriter_fourcc(*'DIVX'), 20.0, (600, 600))

    # write the video frames to a new file
    for frm in frames_list:
        out.write(frm)
    out.release()

    cap.release()
    cv2.destroyAllWindows()


def main(argv):
    videos_df = pd.read_csv("gloss_videos_frames.csv", dtype={'video_id': str})
    if len(argv) == 4:
        videos_df.apply(lambda row: cut_videos(argv[1], argv[2],row['gloss'], row['video_id'], row.name, int(argv[3])), axis=1)
    elif len(argv) == 3:
        videos_df.apply(lambda row: cut_videos(argv[1], "",row['gloss'], row['video_id'], row.name, int(argv[2])), axis=1)
    elif len(argv) < 3:
        print("you should enter the input path and the number of frames of the output.")


if __name__ == "__main__":
    main(sys.argv)