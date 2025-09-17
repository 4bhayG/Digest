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
            transcript_data = YouTubeTranscriptApi().fetch(video_id)
            transcript = " ".join(entry.text for entry in transcript_data)
            return transcript
        except Exception as e:
            raise RuntimeError(f"Error fetching transcript: {e}")

    def split_transcript(self, transcript: str, max_words: int = 1000):
        words = transcript.split()
        for i in range(0, len(words), max_words):
            yield " ".join(words[i:i+max_words])

    def summarize_chunk(self, chunk: str) -> str:
        prompt = (
            "Summarize the following YouTube transcript chunk in 5-8 detailed bullet points. "
            "Each point should capture a key idea, fact, or event, and include important context or examples if present. "
            "Do not add information not present in the text. "
            "Keep the total summary under 150 words.\n\n"
            f"Transcript chunk:\n{chunk}"
        )
        response = self.model.generate_content(prompt)
        return response.text.strip()

    def summarize_video(self, video_url: str) -> str:
        transcript = self.extract_transcript(video_url)
        word_count = len(transcript.split())
        # If transcript is small, summarize directly with a 250-word limit
        if word_count < 1500:
            prompt = (
                "Summarize the following YouTube transcript in 5-10 detailed bullet points. "
                "Each point should capture a key idea, fact, or event, and include important context or examples if present. "
                "Do not add information not present in the text. "
                "Keep the total summary under 250 words.\n\n"
                f"Transcript:\n{transcript}"
            )
            response = self.model.generate_content(prompt)
            return response.text.strip()
        # Otherwise, use map-reduce with a 400-word limit
        chunk_summaries = [self.summarize_chunk(chunk) for chunk in self.split_transcript(transcript)]
        reduce_prompt = (
            "Given the following chunk summaries from a YouTube video, combine them into a single summary of 10-15 detailed bullet points. "
            "Each point should be informative, non-repetitive, and include important context or examples from the video. "
            "Do not add new information or opinions. "
            "Keep the total summary under 400 words.\n\n"
            f"Chunk summaries:\n{' '.join(chunk_summaries)}"
        )
        final_response = self.model.generate_content(reduce_prompt)
        return final_response.text.strip()
