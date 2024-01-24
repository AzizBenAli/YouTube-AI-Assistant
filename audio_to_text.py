from pytube import YouTube
import pytube
import os
import pywhisper
from youtube_transcript_api import YouTubeTranscriptApi
import streamlit as st
import time 

def transcribe_video_to_text1(url):
 try:
  yt = YouTube(url)
  video = yt.streams.filter(only_audio=True).first()
  out_file = video.download(output_path="Youtube",filename="audio.mp3")
  directory_path = r'c:\Users\benal\Langchain'
  audio_path = os.path.join(directory_path, out_file)
  os.startfile(audio_path)
  model = pywhisper.load_model("base")
  result = model.transcribe(audio_path,language='en',temperature=0)
  video_title = yt.title
  output_file_path = fr"c:\\Users\\benal\\Langchain\\Youtube\\video.txt"
  transcribed_text=result['text']
  with open(output_file_path, 'w', encoding='utf-8') as output_file:
    output_file.write(transcribed_text)
  return transcribed_text
 except pytube.exceptions.RegexMatchError:
        pass



def transcribe_video_to_text(url):
 try:
  yt = YouTube(url)
  video_title = yt.title
  id=url.split("=")[-1]
  srt1 = YouTubeTranscriptApi.get_transcript(id)
  transcript_text=""
  for i in srt1:
    transcript_text=transcript_text+" "+i['text']
  output_file_path=fr'c:\Users\benal\Langchain\youtube\video.txt'
  with open(output_file_path, 'w', encoding='utf-8') as output_file:
   output_file.write(transcript_text)
  return transcript_text
 except pytube.exceptions.RegexMatchError:
        pass
 except Exception as e:
    st.error('This Video has no Transcript. Please try another video', icon="🚨")
    time.sleep(5)
    st.rerun()

if __name__ == "__main__":
  video_url="https://www.youtube.com/watch?v=your_video_id"
  transcribe_video_to_text(video_url)
