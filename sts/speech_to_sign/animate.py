import os.path
from cv2 import cv2
from os import listdir
from os.path import isfile, join
import pandas as pd
from zipfile import ZipFile
from sts.sign_to_speech.model_prepare import download_file


class Animate:
    def __init__(self, path):
        self.caps = []
        self.vid = 0
        self.flag = True
        self.speed = 20

        download_file('https://drive.google.com/u/0/uc?id=1N6sBkh9CA1srl9FuWUa0Z7CmJLcxS3Fd&export=download',
                      os.path.join(path, 'videos.zip'))
        with ZipFile(os.path.join(path, 'videos.zip'), 'r') as videos:
            videos.extractall(path)

        self.path = os.path.join(path, 'videos')

        files = [f for f in listdir(self.path) if isfile(join(self.path, f))]
        print(files)
        self.files_df = pd.DataFrame(files, columns=['path'])
        self.files_df['file_name'] = [file.split('.')[0] for file in files]
        self.files_df['full_path'] = [join(self.path, file).replace('\\', '/') for file in files]

    def get_path(self, name):
        """Get the video path of a given word

        Args:
            name (str): The video name

        Returns:
            path (str): The path of the video

        """

        try:
            path = self.files_df[self.files_df['file_name'] == name]['full_path'].values[0]
            return path
        except:
            path = None
            print('no file named ' + name)
        return path

    def display(self):
        for video_cap in self.caps:
            ret, frame = video_cap.read()
            while ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                cv2.waitKey(self.speed)
                ret, frame = video_cap.read()
                yield gray
            video_cap.release()
        self.caps = []

    def show_sign(self, phrase):
        """Get the video paths of the sentence's words and display them

        Args:
            phrase (str): The predicted sentence

        Returns:
            Sign videos frames
        """

        self.flag = True
        self.vid = 0
        words = phrase.split(' ')  # split the sentence into words
        print('Display:', words)
        videos = [self.get_path(word.lower()) for word in words
                  if self.files_df['file_name'].str.contains(word.lower()).sum() > 0]  # list of video paths
        print('videos:', videos)
        self.caps = [cv2.VideoCapture(video) for video in videos]
        for frame in self.display():
            yield frame

    def set_speed(self, speed):
        """Controls the speed of videos

        Args:
            speed (int): The video speed

        Output:
            Sign videos display with custom speed
        """
        self.speed = speed
