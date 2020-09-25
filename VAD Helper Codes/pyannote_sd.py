import torch 
import os

from pyannote.core import *
from pyannote.audio.features import RawAudio
from IPython.display import Audio

import collections
import contextlib
import sys
import wave
import pandas as pd 
import numpy as np
from sklearn import metrics
from scipy.optimize import brentq
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import torch
import os

def read_wave(path):
    """Reads a .wav file.
    Takes the path, and returns (PCM audio data, sample rate).
    """
    wf = wave.open(path,'rb')
    num_channels = wf.getnchannels()
    sample_width = wf.getsampwidth()
    sample_rate = wf.getframerate()
    # print(sample_width)
    no_of_samples = wf.getnframes()
    duration = no_of_samples / float(sample_rate)
    pcm_data = wf.readframes(wf.getnframes())
    return pcm_data, sample_rate,duration

def frame_generator(frame_duration_ms, audio, sample_rate,duration):
    """Generates audio frames from PCM audio data.
    Takes the desired frame duration in milliseconds, the PCM data, and
    the sample rate.
    Yields Frames of the requested duration.
    """
    n = int(sample_rate * (frame_duration_ms / 1000.0) * 2)
    offset = 0
    timestamp = 0.0
    frame_duration = frame_duration_ms / 1000.0
    while timestamp + frame_duration < duration:
        yield audio[offset:offset + n]
        timestamp += frame_duration
        offset += n


def predict(frame_duration_ms,frames,path):
    pipeline = torch.hub.load('pyannote/pyannote-audio', 'dia')
    diarization = pipeline({'audio': path})
    diarization_list = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
      diarization_list.append([speaker,turn.start,turn.end])
    diarization_df = pd.DataFrame(diarization_list,columns = ['Speaker','Start','End'])
    return diarization_df

def main():
  #audio,sample_rate,duration = read_wave('/home/an46/s_summer2020/Local Recordings/AudioBand/Mono/AudioBand1d.wav')
  audio,sample_rate,duration = read_wave('/home/an46/s_summer2020/Local Recordings/AudioBand/Mono/AudioBand9a.wav')
  frames = frame_generator(30,audio,sample_rate,duration)
  frames = list(frames)
  diarization_df = predict(30,frames,'/home/an46/s_summer2020/Local Recordings/AudioBand/Mono/AudioBand9a.wav')
  print(diarization_df)

main()

    
        
