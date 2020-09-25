import os
import random
random.seed(97)
import shutil

no_of_directories = 2
data_dir1 = "/home/an46/s_summer2020/Local Recordings/AudioBand/Mono"
data_dir2 = "/home/an46/s_summer2020/Local Recordings/watch_recordings/Mono"
train_dir = "/home/an46/s_summer2020/Local Recordings/Train"
test_dir = "/home/an46/s_summer2020/Local Recordings/Test"
annotation_dir1 = "/home/an46/s_summer2020/Local Recordings/AudioBand/Annotations"
annotation_dir2 = "/home/an46/s_summer2020/Local Recordings/watch_recordings/Annotations"
train_annotation_dir = "/home/an46/s_summer2020/Local Recordings/Train_Annotations"
test_annotation_dir = "/home/an46/s_summer2020/Local Recordings/Test_Annotations"
sound_files1 = os.listdir(data_dir1)
sound_files2 = os.listdir(data_dir2)
length_dir1 = len(sound_files1)
length_dir2 = len(sound_files2)
total_length = length_dir1 + length_dir2
print(total_length)
train_frac = 0.8
test_frac = 0.2
train_size = int(train_frac * total_length)
test_size = total_length - train_size
test_size1 = int(test_size / no_of_directories)
test_size2 = test_size - test_size1
train_size1 = length_dir1 - (test_size1)
print(train_size1)
train_size2 = length_dir2 - (test_size2)
print(train_size2)

train1_numbers = random.sample(range(length_dir1), train_size1)
print(train1_numbers)
train2_numbers = random.sample(range(length_dir2),train_size2)
print(train2_numbers)

for i in range(length_dir1):
	if i in train1_numbers:
		shutil.copy(os.path.join(data_dir1,sound_files1[i]), train_dir)
		shutil.copy(os.path.join(annotation_dir1,sound_files1[i].split('.')[0] + '.csv'),train_annotation_dir)
	else:
		shutil.copy(os.path.join(data_dir1,sound_files1[i]), test_dir)
		shutil.copy(os.path.join(annotation_dir1,sound_files1[i].split('.')[0] + '.csv'),test_annotation_dir)

for i in range(length_dir2):
	if i in train2_numbers:
		shutil.copy(os.path.join(data_dir2,sound_files2[i]), train_dir)
		shutil.copy(os.path.join(annotation_dir2,sound_files2[i].split('.')[0] + '.csv'),train_annotation_dir)
	else:
		shutil.copy(os.path.join(data_dir2,sound_files2[i]), test_dir)
		shutil.copy(os.path.join(annotation_dir2,sound_files2[i].split('.')[0] + '.csv'),test_annotation_dir)
