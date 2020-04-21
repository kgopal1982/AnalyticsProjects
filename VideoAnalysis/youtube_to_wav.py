from pytube import YouTube
from moviepy.editor import *

# download a file with only audio, to save space
# if the final goal is to convert to mp3
youtube_link = 'https://www.youtube.com/watch?v=siyBp8Csugk'
w = YouTube(youtube_link).streams.first()
w.download(output_path="/home/krishna/datas/video_analysis")


#run the below command frm the place where mp4 is placed
ffmpeg -i obama_farewell_speech.mp4 -vn obama_farewell_speech.mp3

# convert to wav file.  
ffmpeg -i obama_farewell_speech.mp3 -vn -acodec pcm_s16le -ac 1 -ar 16000 -f wav obama_farewell_speech.wav