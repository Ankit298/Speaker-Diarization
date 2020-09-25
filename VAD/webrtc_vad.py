import os
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
# import PyByteArray

def read_wave(path):
    """Reads a .wav file.
    Takes the path, and returns (PCM audio data, sample rate).
    """
    wf = wave.open(path,'rb')
    num_channels = wf.getnchannels()
    # print(num_channels)
    sample_width = wf.getsampwidth()
    sample_rate = wf.getframerate()
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

def ground_truth(frame_duration_ms,frames,path):
    gt_df = pd.read_csv(path)
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
    data_dir = 'E:/Summer2020/Local Recordings/Youtube Videos/Extracted audios/Mono'
    annotation_dir = 'E:/Summer2020/Local Recordings/Youtube Videos/Extracted audios/Annotations'
    sound_files = os.listdir(data_dir)
    result_lists = ['result_list0','result_list1','result_list2','result_list3']
    result_dataframes = ['result_df0','result_df1','result_df2','result_df3']
    for aggression in [0,1,2,3]:
        result_lists[aggression] = []
        for file in sound_files:
            # file_path = os.path.join(data_dir,file)
            # annotation_path = os.path.join(annotation_dir,file.split('_')[0] + '_annotated.csv')
            file_path = 'E:/Summer2020/Local Recordings/AudioBand/Mono/AudioBand9b.wav'
            annotation_path = 'E:/Summer2020/Local Recordings/AudioBand/Annotations/AudioBand9b.csv'
            audio, sample_rate, duration = read_wave(file_path)
            vad = webrtcvad.Vad(aggression)
            frames = frame_generator(30, audio, sample_rate,duration)
            frames = list(frames)
            pred_list = vad_collector(sample_rate, 30,vad, frames)
            gt_list = ground_truth(30, frames,annotation_path)
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
            # print(file + ':')
            print('Accuracy: ' + str(acc))
            print('Equal Error Rate: ' + str(eer))
            result_lists[aggression].append([file,acc,eer,speech_percentage,mislabelled_silence])
            break
            # print(gt_list[0:100])
            # print(pred_list[0:100])
        break
        result_dataframes[aggression] = pd.DataFrame(result_lists[aggression],columns = ['Recording','Accuracy(%)','EER(%)','Speech Percentage','Mislabelled Silence(%)'])
        result_dataframes[aggression].to_csv('E:/Summer2020/Results/webrtc vad/webrtc' + str(aggression) + '_youtube.csv')
        # print(result_dataframes[aggression])


def play_mistake_stretches(frame_duration_ms,data_path,annotation_path,return_path,aggression):
    audio, sample_rate, duration = read_wave(data_path)
    frames = frame_generator(30, audio, sample_rate,duration)
    frames = list(frames)
    vad = webrtcvad.Vad(aggression)
    pred_list = vad_collector(sample_rate, frame_duration_ms,vad, frames)
    gt_list = ground_truth(30, frames,annotation_path)
    n = int(sample_rate * (frame_duration_ms / 1000.0) * 2)
    mistake_sequence = bytearray()
    offset = 0
    for i in range(len(pred_list)):
        if pred_list[i] != gt_list[i]:
            mistake_sequence += audio[offset:offset + n]
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
    

def store_mistake_stretches():
  data_dir = 'E:/Summer2020/Local Recordings/Youtube Videos/Extracted audios/Mono'
  annotation_dir = 'E:/Summer2020/Local Recordings/Youtube Videos/Extracted audios/Annotations'
  result_dir1 = 'E:/Summer2020/Error Analysis/Youtube'
  sound_files = os.listdir(data_dir)
  for aggression in range(4):
    result_dir = os.path.join(result_dir1,str(aggression))
    for file in sound_files:
        data_path = os.path.join(data_dir,file)
        annotation_path = os.path.join(annotation_dir,file.split('_')[0] + '_annotated.csv')
        result_path = os.path.join(result_dir,file)
        play_mistake_stretches(30,data_path,annotation_path,result_path,aggression)




main()
# store_mistake_stretches()
