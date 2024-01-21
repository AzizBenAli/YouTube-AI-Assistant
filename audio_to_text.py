from pytube import YouTube
import os
import pywhisper
from youtube_transcript_api import YouTubeTranscriptApi

def transcribe_video_to_text1(url):
    try:
        # Download YouTube video audio stream
        yt = YouTube(url)
        video = yt.streams.filter(only_audio=True).first()
        out_file = video.download(output_path="Youtube", filename="audio.mp3")
        directory_path = r'c:\Users\benal\Langchain'
        audio_path = os.path.join(directory_path, out_file)
        
        # Transcribe audio using pywhisper
        os.startfile(audio_path)
        model = pywhisper.load_model("base")
        result = model.transcribe(audio_path, language='en', temperature=0)
        video_title = yt.title
        
        # Save transcribed text to file
        output_file_path = f"c:\\Users\\benal\\Langchain\\Youtube\\{video_title}.txt"
        transcribed_text = result['text']
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(transcribed_text)
        return transcribed_text
    except pytube.exceptions.RegexMatchError:
        pass

def transcribe_video_to_text(url):
    try:
        # Get video details using YouTube API
        yt = YouTube(url)
        video_title = yt.title
        video_id = url.split("=")[-1]
        
        # Get transcript using YouTubeTranscriptApi
        srt1 = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = ""
        for i in srt1:
            transcript_text = transcript_text + " " + i['text']
        
        # Save transcribed text to file
        output_file_path = fr'c:\Users\benal\Langchain\youtube\{video_title}.txt'
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(transcript_text)
        return transcript_text
    except pytube.exceptions.RegexMatchError:
        pass

if __name__ == "__main__":
    # Replace "your_video_id" with the actual video ID or link
    video_url = "https://www.youtube.com/watch?v=your_video_id"

    # Transcribe using the first function
    transcribe_video_to_text1(video_url)

    # Transcribe using the second function
    transcribe_video_to_text(video_url)
