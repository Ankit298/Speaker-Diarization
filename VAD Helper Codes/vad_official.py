import collections
import contextlib
import sys
import wave
import pandas as pd 
import webrtcvad
import numpy as np
from sklearn import metrics
from scipy.optimize import brentq
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

# def sample_rate_change(path,sample_rate):
#     wfr = wave.open(path,'rb')
#     n_channels = wfr.getnchannels()
#     sample_width = wfr.getsampwidth()
#     s_read_rate = wfr.getframerate()
#     no_of_samples = wfr.getnframes()
#     duration = no_of_samples/s_read_rate
#     new_no_of_samples = int(duration * sample_rate)
#     pcm = wfr.readframes(new_no_of_samples)

#     wf_write = wave.open('16kaudio.wav','wb')
#     wf_write.setsampwidth(sample_width)
#     wf_write.setframerate(sample_rate)
#     wf_write.setnchannels(n_channels)
#     wf_write.writeframes(pcm)


# sample_rate_change('E:/Summer2020/Local Recordings/Youtube Videos/Extracted audios/shop1audio.wav',16000)

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
    gt_df = pd.read_csv("E:/Summer2020/Local Recordings/watch_recordings/Annotations/memo21_annotated.csv")
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
    
def vad_collector(sample_rate, frame_duration_ms,vad, frames):
    pred_list = []
    for frame in frames:
        is_speech = vad.is_speech(frame, sample_rate)
        if is_speech:
            pred_list.append(1)
        else:
            pred_list.append(0)
    return pred_list
        
def main():
    audio, sample_rate, duration = read_wave('E:/Summer2020/Local Recordings/watch_recordings/Memo 021_W_20200607_202657.wav')
    # audio, sample_rate, duration = read_wave('E:/Summer2020/Local Recordings/Recording1.wav')
    vad = webrtcvad.Vad(0)
    frames = frame_generator(30, audio, sample_rate,duration)
    frames = list(frames)
    pred_list = vad_collector(sample_rate, 30,vad, frames)
    # print(len(pred_list))
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
