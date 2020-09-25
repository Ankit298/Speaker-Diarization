import pandas as pd 
from textgrid import *

# Youtube correction
# textgrid_names_yt = ['shop1audio_annotated','shop2audio_annotated','shop3audio_annotated','sport1audio_annotated','vlog1audio_annotated']
# for val in textgrid_names_yt:
#     tgrid = read_textgrid('E:/Summer2020/Local Recordings/Youtube Videos/Extracted audios/Annotations/' + val + '.TextGrid')
#     df = pd.DataFrame(tgrid)
#     df = df.drop(['tier'],axis = 1)
#     # print(df)
#     l = []
#     i = 0
#     while i < df.shape[0]:
#         if i == 0 and df.iloc[i,2] == "":
#             df.iloc[i + 1,0] = 0
#             l.append(0)
#             j = i + 1
#         elif df.iloc[i,2] == "":
#             temp = df.iloc[i - 1,1]
#             j = i
#             while df.iloc[j,2] == "":
#                 l.append(j)
#                 j += 1
#             df.iloc[j,0] = temp
#         else:
#             j = i + 1
#         i = j
#     df = df.drop(l)
#     df.to_csv('E:/Summer2020/Local Recordings/Youtube Videos/Extracted audios/Annotations/' + val + '.csv')

# Watch correction
# textgrid_names_watch = ['memo10_annotated','memo12_annotated','memo14_annotated','memo15_annotated']
# for val in textgrid_names_watch:
#     tgrid = read_textgrid('E:/Summer2020/Local Recordings/watch_recordings/Annotations/' + val + '.TextGrid')
#     df = pd.DataFrame(tgrid)
#     df = df.drop(['tier'],axis = 1)
#     # print(df)
#     l = []
#     i = 0
#     while i < df.shape[0]:
#         if i == 0 and df.iloc[i,2] == "":
#             df.iloc[i + 1,0] = 0
#             l.append(0)
#             j = i + 1
#         elif df.iloc[i,2] == "":
#             temp = df.iloc[i - 1,1]
#             j = i
#             while df.iloc[j,2] == "":
#                 l.append(j)
#                 j += 1
#             df.iloc[j,0] = temp
#         else:
#             j = i + 1
#         i = j
#     df = df.drop(l)
#     df.to_csv('E:/Summer2020/Local Recordings/watch_recordings/Annotations/' + val + '.csv')


# General
tgrid = read_textgrid('E:/Summer2020/Local Recordings/AudioBand/Annotations/AudioBand10a.TextGrid')
df = pd.DataFrame(tgrid)
df = df.drop(['tier'],axis = 1)
df.to_csv('E:/Summer2020/Local Recordings/AudioBand/Annotations/AudioBand10a.csv')












# textgrid_names_yt = ['shop1audio_annotated','shop2audio_annotated','shop3audio_annotated','sport1audio_annotated','vlog1audio_annotated']
# for val in textgrid_names_yt:
#     tgrid = read_textgrid('E:/Summer2020/Local Recordings/Youtube Videos/Extracted audios/Annotations/' + val + '.TextGrid')
#     df = pd.DataFrame(tgrid)
#     df = df.drop(['tier'],axis = 1)
#     l = []
#     i = 0
#     while i < df.shape[0]:
#         if df.iloc[i,2] == "":
#             temp = df.iloc[i - 1,1]
#             j = i
#             while df.iloc[j,2] == "":
#                 l.append(j)
#                 j += 1
#             df.iloc[j,0] = temp
#     df = df.drop(l)
#     df.to_csv('E:/Summer2020/Local Recordings/Youtube Videos/Extracted audios/Annotations/' + val + '.csv')

            
