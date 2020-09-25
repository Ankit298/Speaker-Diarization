import wave
import os
from pydub import AudioSegment
#data_dir = '/home/an46/tmp_pyannote/Codes/Seq01-1P-S0M1.wav'
file1 = '/home/an46/tmp_pyannote/Codes/Seq01-1P-S0M1.wav'
#return_dir = '/home/an46/tmp_pyannote/Codes/Seq01-1P-S0M1.wav''
return_path = '/home/an46/tmp_pyannote/Codes/Seq01-1P-S0M1.wav'
#sound_files = os.listdir(data_d
#path = os.path.join(data_dir,file)
#write_path = os.path.join(return_dir,file)
mysound = AudioSegment.from_wav(file1)
mysound = mysound.set_channels(1)
mysound.export(return_path, format="wav")

