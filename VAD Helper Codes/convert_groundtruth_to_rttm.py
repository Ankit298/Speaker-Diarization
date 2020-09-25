
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 16:03:12 2020

@author: lbishal
"""


import soundfile as sf


# groundtruth_dir = r'D:/Rice/Elec599/jebsens_recording/Diarization/longer_recording/chunked/GroundTruth'
# audio_dir       = r'D:/Rice/Elec599/jebsens_recording/Diarization/longer_recording/chunked/Audio'
# outfile         = r'D:/Rice/Elec599/jebsens_recording/Diarization/longer_recording/chunked/jebsens_longterm_20200319_chunked.rttm'

# with open(outfile, 'w') as f:
#     for each_file in os.listdir(groundtruth_dir):
#         basename = os.path.splitext(each_file)[0]
#         groundtruth_file = os.path.join(groundtruth_dir,each_file)
#         groundtruth_np = pd.read_csv(groundtruth_file,index_col=0).values
#         audio_file     = os.path.join(audio_dir, basename+'.wav')
#         signal, fs = sf.read(audio_file)
    
#         seg_count = 0
            
#         speech_on = 0
#         for i in range(len(groundtruth_np)):
#             if (groundtruth_np[i] == 1 and speech_on == 0):
#                 speech_on = 1
#                 speech_time_start = i/fs
#             if (groundtruth_np[i] == 0 and speech_on == 1):
#                 speech_on = 0
#                 speech_time_end = i/fs
#                 duration = speech_time_end - speech_time_start
#                 seg_count += 1
#                 f.write('SPEAKER {0} 1 {1} {2} <NA> <NA> speech <NA> <NA>\n'.format(basename,
#                                      speech_time_start,duration))
#         if speech_on == 1:
#             speech_time_end = i/fs
#             duration = speech_time_end - speech_time_start
#             seg_count += 1
#             f.write('SPEAKER {0} 1 {1} {2} <NA> <NA> speech <NA> <NA>\n'.format(basename,
#                                      speech_time_start,duration))
import os
import pandas as pd
import numpy as np 
audio_dir = '/home/an46/s_summer2020/Local Recordings/Train'
groundtruth_dir = '/home/an46/s_summer2020/Local Recordings/Train_Annotations'
outfile = '/home/an46/tmp_pyannote/combined_rttm.rttm'
f = open(outfile,'w')
audio_files = os.listdir(audio_dir)
for file in audio_files:
    file_name = file.split('.')[0]
    if file_name[0] != 'S':
        annotation_path = os.path.join(groundtruth_dir,file_name + '.csv')
        annotation_df = pd.read_csv(annotation_path)
        for i in range(annotation_df.shape[0]):
            if annotation_df.iloc[i,3] > 0:
                speech_start = annotation_df.iloc[i,1]
                speech_end = annotation_df.iloc[i,2]
                speech_duration = speech_end - speech_start
                f.write('SPEAKER {0} 1 {1} {2} <NA> <NA> speech <NA> <NA>\n'.format(file_name,speech_start,speech_duration))
    else:
        each_file = file_name.split('_')[0] + '_lr.csv'
        basename = os.path.splitext(each_file)[0]
        groundtruth_file = os.path.join(groundtruth_dir,each_file)
        groundtruth_np = pd.read_csv(groundtruth_file,index_col=0).values
        audio_file     = os.path.join(audio_dir, file)
        signal, fs = sf.read(audio_file)
    
        seg_count = 0
            
        speech_on = 0
        for i in range(len(groundtruth_np)):
            if (groundtruth_np[i] > 0 and speech_on == 0):
                speech_on = 1
                speech_time_start = i/fs
            if (groundtruth_np[i] == 0 and speech_on == 1):
                speech_on = 0
                speech_time_end = i/fs
                duration = speech_time_end - speech_time_start
                seg_count += 1
                f.write('SPEAKER {0} 1 {1} {2} <NA> <NA> speech <NA> <NA>\n'.format(file_name,
                                     speech_time_start,duration))
        if speech_on == 1:
            speech_time_end = i/fs
            duration = speech_time_end - speech_time_start
            seg_count += 1
            f.write('SPEAKER {0} 1 {1} {2} <NA> <NA> speech <NA> <NA>\n'.format(file_name,
                                     speech_time_start,duration))


