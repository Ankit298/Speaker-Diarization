# import os
# import soundfile as sf 
# import resampy
# import matplotlib.pyplot as plt
# # data_dir = 'E:/Summer2020/Local Recordings/Youtube Videos/Extracted audios/Wave Files'
# # downsampled_dir = 'E:/Summer2020/Local Recordings/Youtube Videos/Extracted audios/Down Sampled'
# # sound_files = os.listdir(data_dir)
# # for file in sound_files:
# # 	sound_file = os.path.join(data_dir,file)
# # 	resample_rate = 16000
# # 	signal,sr = sf.read(sound_file)
# # 	signal_resamp = resampy.resample(signal.T,sr,resample_rate)
# # 	return_path = os.path.join(downsampled_dir,file.split('.')[0]+'_down'+'.wav')
# # 	sf.write(return_path,signal_resamp.T,resample_rate)


# return_path = 'E:/Summer2020/Local Recordings/AudioBand/Down Sampled/AudioBand1a_down.wav'
# resample_rate = 16000
# sound_file = 'E:/Summer2020/Local Recordings/AudioBand/Extracted/AudioBand1a.wav'
# signal,sr = sf.read(sound_file)
# print(sr)
# # signal_resamp = resampy.resample(signal.T,sr,resample_rate)
# # sf.write(return_path,signal_resamp.T,resample_rate)

# # import wave
# # wf = wave.open('E:/Summer2020/audioband_down.wav')
# # sample_rate = wf.getframerate()
# # print(sample_rate)cv2.imshow("Original Image", img)


import cv2
import numpy as np
img = cv2.imread('Roshini.jpeg')
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
img_contours = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]
img_contours = sorted(img_contours, key=cv2.contourArea)

for i in img_contours:

	if cv2.contourArea(i) > 100:

		break

	mask = np.zeros(img.shape[:2], np.uint8)
	cv2.drawContours(mask, [i],-1, 255, -1)
	new_img = cv2.bitwise_and(img, img, mask=mask)
	cv2.imshow("Image with background removed", new_img)

	cv2.waitKey(0)

# 3: 7:50 - 10:50  4: 3:34:30 - 3:39:30  4: 5:36:00 - 5:39:00  4: 5:40:20 - 5:42:20  4: 5:43:50 - 5:46:50  4: 6:06:00 - 6:08:30  4: 6:42:25 - 