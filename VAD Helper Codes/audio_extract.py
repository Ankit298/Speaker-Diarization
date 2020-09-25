import wave
wf = wave.open('E:/Summer2020/Local Recordings/AudioBand/Long Files/New6.wav','rb')
n_channels = wf.getnchannels()
print("The number of channels is: " + str(n_channels))
sample_width = wf.getsampwidth()
sample_rate = wf.getframerate()
print("The Sample Rate is: " + str(sample_rate))
no_of_samples = wf.getnframes()
pcm = wf.readframes(no_of_samples)
# 0 - 2, 4:20 - 6:50, 51:50 - 54:50, 54:50 - 58:50, 2:36:20 - 2:39:20, 6:05:20 - 6:08:20, 
t1 = 1610
t2 = 1730
# t3 = 3350
# t4 = 3620
offset1 = int((t1*sample_rate)*sample_width)
offset2 = int((t2*sample_rate)*sample_width)
# offset3 = int((t3*sample_rate)*sample_width)
# offset4 = int((t4*sample_rate)*sample_width)
audio = pcm[offset1:offset2]
# audio1 = pcm[offset3:offset4]
# merged_audio = audio + audio1
wf_write = wave.open('E:/Summer2020/Local Recordings/AudioBand/Mono/AudioBand10a.wav','wb')
wf_write.setsampwidth(sample_width)
wf_write.setframerate(sample_rate)
wf_write.setnchannels(n_channels)
wf_write.writeframes(audio)
