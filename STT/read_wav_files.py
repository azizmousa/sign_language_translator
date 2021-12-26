# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 16:12:11 2021

@author: H
"""

import pyaudio
import speech_recognition as sr
import glob
import os

r = sr.Recognizer()

def record_recognize_audio(file_name):

    with sr.AudioFile(file_name) as source:
    # listen to data (load audio to memory)
        audio_data = r.record(source)
    # recognize (convert from speech to text)
        text = r.recognize_google(audio_data,language = 'en-IN',show_all=True )
  
    return text

