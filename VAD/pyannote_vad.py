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
    while timestamp < duration:
        yield audio[offset:offset + n]
        timestamp += frame_duration
        offset += n

def ground_truth(frame_duration_ms,frames,path):
    gt_df = gt_df = pd.read_csv(path)
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

def ground_truth_snr(frame_duration_ms,annotation_path):
    gt_df = pd.read_csv(annotation_path)
    gt_list = []
    i = 0
    while i < gt_df.shape[0]:
        tmp_array = np.array(gt_df.iloc[i:i + 480,1],dtype = int)
        gt_list.append(np.bincount(tmp_array).argmax())
        i = i + 480
    for j in range(len(gt_list)):
      if gt_list[j] > 0:
        gt_list[j] = 1
    return gt_list
    
def predict(frame_duration_ms,frames,path):
    OWN_FILE = {'audio': path}
    pipeline = torch.hub.load('pyannote/pyannote-audio', 'sad_dihard', pipeline=True)
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
    data_dir = '/home/an46/fall20/Local Recordings/Test'
    annotation_dir = '/home/an46/fall20/Local Recordings/Test_Annotations'
    #file = 'bollywood1_down.wav'
    sound_files = os.listdir(data_dir)
    print(sound_files)
    result_list = []
    eer_audioband_tl = []
    eer_watch_tl = []
    avg_eer = 0
    for file in sound_files:
      data_path = os.path.join(data_dir,file)
      if file[0] != 'S':
        annotation_path = os.path.join(annotation_dir,file.split('.')[0] + '.csv')
      else:
        annotation_path = os.path.join(annotation_dir,file.split('_')[0] + '_lr.csv')
      audio, sample_rate, duration = read_wave(data_path)
      frames = frame_generator(30, audio, sample_rate,duration)
      frames = list(frames)
      pred_list = predict(30,frames,data_path)
      print(len(pred_list))
      if file[0] != 'S':
        gt_list = ground_truth(30, frames,annotation_path)
      else:
        gt_list = ground_truth_snr(30,annotation_path)
      print(len(gt_list))
      gt_length = len(gt_list)
      gt_array = np.array(gt_list)
      speech_frames = np.count_nonzero(gt_array == 1)
      speech_percentage = (speech_frames/gt_length)*100
      pred_array = np.array(pred_list)
      frames_mislabelled = 0
      silence_frames_mislabelled = 0
      for i in range(len(pred_list)):
        if pred_list[i] != gt_list[i]:
          if gt_list[i] == 0: silence_frames_mislabelled += 1
          frames_mislabelled += 1
      mislabelled_silence = (silence_frames_mislabelled/frames_mislabelled)*100
      fpr, tpr, thresholds = metrics.roc_curve(gt_array,pred_array, pos_label=1)
      eer = brentq(lambda x : 1. - x - interp1d(fpr, tpr)(x), 0., 1.)*100
      acc = np.sum(gt_array == pred_array)/len(gt_list)*100
      result_list.append([file,acc,eer,speech_percentage,mislabelled_silence])
      avg_eer += eer
      print(file)
      print(acc)
      print(eer)
      if file[0:9] == 'AudioBand':
        eer_audioband_tl.append(eer)
      else:
        eer_watch_tl.append(eer)
      # print(gt_list[0:100])
      # print(pred_list[0:100])}
    avg_eer = avg_eer/len(sound_files)
    print("Average EER is: " + str(avg_eer))
    result_df = pd.DataFrame(result_list,columns = ['Recording','Accuracy(%)','EER(%)','Speech Percentage','Mislabelled Silence(%)'])
    result_df.to_csv('/home/an46/tmp_pyannote/Results/24.csv')


def play_mistake_stretches(frame_duration_ms,data_path,annotation_path,return_path):
    audio, sample_rate, duration = read_wave(data_path)
    frames = frame_generator(30, audio, sample_rate,duration)
    frames = list(frames)
    print(len(frames))
    #vad = webrtcvad.Vad(0)
    pred_list = predict(frame_duration_ms,frames,data_path)
    gt_list = ground_truth(30, frames,annotation_path)
    print(len(pred_list))
    n = int(sample_rate * (frame_duration_ms / 1000.0) * 2)
    # print(n)
    array_size = int(n*(duration / (frame_duration_ms / 1000.0)))
    mistake_sequence = bytearray()
    mistake_list_gt = []
    mistake_list_pred = []
    silence_frames_mislabelled = 0
    # mistake_sequence = PyByteArray_Resize(mistake_sequence,array_size)
    offset = 0
    for i in range(len(pred_list)):
        if pred_list[i] != gt_list[i]:
            if gt_list[i] == 0: silence_frames_mislabelled += 1
            mistake_sequence += audio[offset:offset + n]
            mistake_list_gt.append(gt_list[i])
            mistake_list_pred.append(pred_list[i])
            offset += n
        else:
            offset += n

    wf_read = wave.open(data_path,'rb')
    n_channels = wf_read.getnchannels()
    sample_width = wf_read.getsampwidth()
    no_of_samples = wf_read.getnframes()
    wf_write = wave.open(return_path,'wb')
    wf_write.setsampwidth(sample_width)
    wf_write.setframerate(sample_rate)
    wf_write.setnchannels(n_channels)
    wf_write.setnframes(no_of_samples)
    wf_write.writeframes(mistake_sequence)
    # print(mistake_list_gt[:50])
    # print(mistake_list_pred[:50])
    print(silence_frames_mislabelled)
    print(len(mistake_list_gt))
    print(len(mistake_sequence))

def store_mistake_stretches():
  data_dir = '/content/drive/My Drive/Extracted audios/Watch Recordings'
  annotation_dir = '/content/drive/My Drive/Extracted audios/Annotations/Watch/CSV'
  result_dir = '/content/drive/My Drive/Extracted audios/Error Analysis/Watch'
  sound_files = os.listdir(data_dir)
  for file in sound_files:
    file1 = 'Memo4.wav'
    data_path = os.path.join(data_dir,file1)
    annotation_path = os.path.join(annotation_dir,'memo4_annotated.csv')
    result_path = os.path.join(result_dir,'new' + file1)
    play_mistake_stretches(30,data_path,annotation_path,result_path)
    break

main()


