import os
data_dir = '/home/an46/fall20/Local Recordings/Train'
result_path = '/home/an46/fall20/Train.lst'
sound_files = os.listdir(data_dir)
f = open(result_path,'w')
for file in sound_files:
	f.write(file.split('.')[0] + '\n')

data_dir_test = '/home/an46/fall20/Local Recordings/Test'
result_path = '/home/an46/fall20/Test.lst'
sound_files = os.listdir(data_dir_test)
f = open(result_path,'w')
for file in sound_files:
        f.write(file.split('.')[0] + '\n')

