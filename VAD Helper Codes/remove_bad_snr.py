import os
import shutil

data_dir = '/home/an46/s_summer2020/Local Recordings/Train'
sound_files = os.listdir(data_dir)
result_dir = '/home/an46/s_summer2020/Local Recordings/temp_audio_watch'
for file in sound_files:
	if file[0] == 'A':
		shutil.move(os.path.join(data_dir,file),result_dir)
