import os
from dotenv import load_dotenv
from google import generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

class YouTubeSummarizer:
    def __init__(self, load_env=True):
        if load_env:
            load_dotenv()
        self.api_key = os.getenv("GoogleApiKey")
        if not self.api_key:
            raise ValueError("GoogleApiKey not found in environment variables.")
        genai.configure(api_key=self.api_key)

        self.prompt = (
            "You are a youtube video summarizer and you will be taking the transcript "
            "text and summarizing the entire video and provide important summary in points "
            "within 200 words. The transcript is as follows: "
        )
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def extract_transcript(self, video_url: str) -> str:
        try:
            query_params = parse_qs(urlparse(video_url).query)
            video_id = query_params.get("v", [""])[0]
            transcript_data = YouTubeTranscriptApi.get_transcript(video_id=video_id)
            transcript = " ".join(entry["text"] for entry in transcript_data)
            return transcript
        except Exception as e:
            raise RuntimeError(f"Error fetching transcript: {e}")

    def summarize_video(self, video_url: str) -> str:
        transcript = self.extract_transcript(video_url)
        response = self.model.generate_content(self.prompt + transcript)
        return response.text
