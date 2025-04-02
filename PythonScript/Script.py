from dotenv import load_dotenv
load_dotenv()  # Load all env variable
import os
from google import generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse , parse_qs

genai.configure(api_key=os.getenv("GoogleApiKey"))

print(os.getenv("GoogleApiKey"))

prompt = "You are a youtube video summarizer and you will be taking the transcript text ans summarizing the entire vedio and provide important summary in points within 200 word. The transcript is as follows : "

## Getting transcript of video
def extract_transcript(video_url):
    try:
        query_params = parse_qs(urlparse(video_url).query)
        video_id = query_params.get("v", [""])[0]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id=video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " "  +  i["text"]

        return transcript

    except Exception as e:
        raise e

def content_gemeini(transcript_text):
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt + transcript_text)
    return response.text


data = input("Enter Video Url: ");

print(content_gemeini(extract_transcript(data)))
    



