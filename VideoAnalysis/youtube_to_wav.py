from pytube import YouTube
from moviepy.editor import *

# download a file with only audio, to save space
# if the final goal is to convert to mp3
#youtube_link = 'https://www.youtube.com/watch?v=VAn8t80lclM'
youtube_link = 'https://www.youtube.com/watch?v=R-3dfURb2hA'
w = YouTube(youtube_link).streams.first()
w.download(output_path="/home/krishna/datas/video_analysis")


#run the below command frm the place where mp4 is placed
ffmpeg -i What_is_Kubernetes.mp4 -vn What_is_Kubernetes.mp3

# convert to wav file.  
ffmpeg -i What_is_Kubernetes.mp3 -vn -acodec pcm_s16le -ac 1 -ar 16000 -f wav What_is_Kubernetes.wav