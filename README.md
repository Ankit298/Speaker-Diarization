# Speaker Diarization for unconstrained audio streams

## Introduction:

This project is a work in progress to build a speaker diarization pipeline for unconstrained audio streams collected by an audio band. Speaker diarization is the proces of partitioning an input audio stream into segments of who spoke when. The pipeline consists of 3 steps: Voice Activity Detection, Speaker Change Detection and Speaker Embedding. The codes in the this repository is implementing the first step of the speaker diarization pipeline: Voice activity detection. Our work on voice activity detection builds on top of [pyannote-audio](https://github.com/pyannote/pyannote-audio) for implementing it on unconstrained audio from audiobands. Current work includes transfer learning with our own data and building novel loss functions and speech enhancement techniques.

## Installation and Dependencies:

Installation instructions and dependencies has to be followed as mentioned in [pyannote-audio](https://github.com/pyannote/pyannote-audio).

## Data Collection:

Audio Data was collected from 3 sources: Audio Band recordings, Watch recordings, and Youtube videos. For the first two sources, an audio band or a smart watch was strapped to person's hand and they are asked to proceed with their day to day activities. This was done to simulate a free-living environment because that is our ultimate use-case. Sequences of audio conversations are later collected to build the dataset. A total of 2.5 hours of audio data was collected and annotated.

# Directories:

# Codes

Initially, two voice activity existing frameworks - Pyannote VAD and WebRTC VAD was tested on all 3 sources of collected data. The audio processing pipeline for webRTC VAD is in webrtc_vad.py and the pipeline to implement the Pyannote VAD framework is in pyannote_vad.py. All other files are complementary files for data pre-processing (extracting audio, resampling, creating annotation files etc). Details on each of these complementary files can be found in the comments of the respective files.

# Error Analysis

Error analysis was performed to see where exactly the existing frameworks were failing. Frames of audio which were improperly classified were combined together to form error recordings for every audio sequence. Error recordings of each 3 audio sources can be found in the Error Analysis folder.

# Local Recordings

Contains the audio sequences collected from the audio band, smart watch, and youtube videos. Corresponding annotations is also present in this folder.

