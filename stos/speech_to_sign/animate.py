import os.path
from cv2 import cv2
from os import listdir
from os.path import isfile, join
import pandas as pd
from zipfile import ZipFile
from stos.sign_to_speech.model_prepare import download_file


class Animate:
    def __init__(self, path):
        self.__caps = []
        self.__speed = 20

        self.__path = os.path.join(path, 'videos')
        if not os.path.exists(self.__path):
            print('downloading videos.')
            download_file('https://drive.google.com/u/0/uc?id=1N6sBkh9CA1srl9FuWUa0Z7CmJLcxS3Fd&export=download',
                          os.path.join(path, 'videos.zip'))
            with ZipFile(os.path.join(path, 'videos.zip'), 'r') as videos:
                videos.extractall(path)

        files = [f for f in listdir(self.__path) if isfile(join(self.__path, f))]
        self.files_df = pd.DataFrame(files, columns=['__path'])
        self.files_df['file_name'] = [file.split('.')[0] for file in files]
        self.files_df['full_path'] = [join(self.__path, file).replace('\\', '/') for file in files]

    def get_path(self, name):
        """Get the video __path of a given word

        Args:
            name (str): The video name

        Returns:
            __path (str): The __path of the video

        """

        try:
            path = self.files_df[self.files_df['file_name'] == name]['full_path'].values[0]
            return path
        except:
            path = None
            print('no file named ' + name)
        return path

    def display(self):
        for video_cap in self.__caps:
            ret, frame = video_cap.read()
            while ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                cv2.waitKey(self.__speed)
                ret, frame = video_cap.read()
                yield gray
            video_cap.release()
        self.__caps = []

    def show_sign(self, phrase):
        """Get the video paths of the sentence's words and display them

        Args:
            phrase (str): The predicted sentence

        Returns:
            Sign videos frames
        """

        words = phrase.split(' ')  # split the sentence into words
        print('Display:', words)
        videos = [self.get_path(word.lower()) for word in words
                  if self.files_df['file_name'].str.contains(word.lower()).sum() > 0]  # list of video paths
        print('videos:', videos)
        self.__caps = [cv2.VideoCapture(video) for video in videos]
        for frame in self.display():
            yield frame

    def set_speed(self, speed):
        """Controls the __speed of videos

        Args:
            speed (int): The video __speed

        Output:
            Sign videos display with custom __speed
        """
        self.__speed = speed
