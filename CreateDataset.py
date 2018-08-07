from Helper import sum_time, convert_delta , sub_time, find_places, create_dataset

#########
#########
########
video_dif_list = ['01:28','28:59','55:51','1:24:31','1:45:47','2:11:36','2:38:32']
video_len = ['27:33','26:55','28:43','21:19','25:51','27:00','29:11']
video_list = ['MVI_8191.MOV','MVI_8192.MOV','MVI_8193.MOV','MVI_8194.MOV','MVI_8195.MOV','MVI_8196.MOV','MVI_8197.MOV']
video_list = ['titanic/SL/' + video for video in video_list]
for i in range(1,len(video_dif_list)):
    sub_time(video_dif_list[i],video_dif_list[i-1])
    print((convert_delta(video_len[i-1])))
    print('----------------------------------')
video_dif_list_delta = []
for t in video_dif_list:
    video_dif_list_delta.append(convert_delta(t))
print(sum_time(video_len))
#######
#######
#######
target_film = 'titanic'
subs_file = target_film + '/substitle.srt'
sl_video_path = target_film + '\SL'

p = find_places(None, video_dif_list_delta, video_list, subs_file)
create_dataset(p, 'train', target_film)
