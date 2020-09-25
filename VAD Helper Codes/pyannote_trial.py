!pip install -q https://github.com/pyannote/pyannote-audio/tarball/develop


from pyannote.core import Segment, notebook
from pyannote.audio.features import RawAudio
from IPython.display import Audio


import google.colab
own_file, _ = google.colab.files.upload().popitem()
OWN_FILE = {'audio': own_file}
notebook.reset()
# load audio waveform and play it
waveform = RawAudio(sample_rate=16000)(OWN_FILE).data
Audio(data=waveform.squeeze(), rate=16000, autoplay=True)


from google.colab import files
uploaded = files.upload()


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

def read_wave(path):
    """Reads a .wav file.
    Takes the path, and returns (PCM audio data, sample rate).
    """
    wf = wave.open(path,'rb')
    num_channels = wf.getnchannels()
    sample_width = wf.getsampwidth()
    sample_rate = wf.getframerate()
    print(sample_rate)
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

def ground_truth(frame_duration_ms,frames):
    gt_df = gt_df = pd.read_csv(io.BytesIO(uploaded['memo10_annotated.csv']))
    gt_df['name'] = (gt_df['name'] > 0).astype(int)
    gt_list = []
    timestamp = 0.0
    duration = (frame_duration_ms / 1000.0)
    for frame in frames:
        for i in range(0,gt_df.shape[0]):
            if (timestamp >= gt_df.iloc[i,1] and timestamp < gt_df.iloc[i,2]):
                gt_list.append(gt_df.iloc[i,3])
                break
        timestamp += duration
    return gt_list
    
def predict(frame_duration_ms,frames):
    pipeline = torch.hub.load('pyannote/pyannote-audio', 'sad', pipeline=True)
    speech_activity_detection = pipeline(OWN_FILE)
    speech_list = []
    for speech_region in speech_activity_detection.get_timeline():
      speech_list.append([speech_region.start,speech_region.end])
    predicted_df = pd.DataFrame(speech_list)
    pred_list = []
    timestamp = 0.0
    duration = (frame_duration_ms / 1000.0)
    for frame in frames:
      j = 0
      for i in range(0,predicted_df.shape[0]):
        if (timestamp >= predicted_df.iloc[i,0] and timestamp < predicted_df.iloc[i,1]):
          pred_list.append(1)
          j += 1
          break
      if j == 0:
        pred_list.append(0)
      timestamp += duration
    return pred_list
        
def main():
    audio, sample_rate, duration = read_wave('Memo 010_W_20200606_123211.wav')
    frames = frame_generator(30, audio, sample_rate,duration)
    frames = list(frames)
    pred_list = predict(30,frames)
    gt_list = ground_truth(30, frames)
    pred_array = np.array(pred_list)
    gt_array = np.array(gt_list)
    fpr, tpr, thresholds = metrics.roc_curve(gt_array,pred_array, pos_label=1)
    eer = brentq(lambda x : 1. - x - interp1d(fpr, tpr)(x), 0., 1.)
    acc = np.sum(gt_array == pred_array)/len(gt_list)
    print(acc)
    print(eer)
    print(gt_list[0:100])
    print(pred_list[0:100])

main()