import os
import random
random.seed(40)
import shutil

data_dir = '/home/an46/s_summer2020/Local Recordings/Audio_snr'
train_dir = '/home/an46/s_summer2020/Local Recordings/Train'
test_dir = '/home/an46/s_summer2020/Local Recordings/Test'
sound_files = os.listdir(data_dir)
length = len(sound_files)
train_frac = 0.8
test_frac = 0.2
train_length = int(0.8*length)
test_length = length - train_length

train_numbers = random.sample(range(length), train_length)

for i in range(length):
	if i in train_numbers:
		shutil.copy(os.path.join(data_dir,sound_files[i]), train_dir)
	else:
		shutil.copy(os.path.join(data_dir,sound_files[i]), test_dir)
		
