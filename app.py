import os
import streamlit as st
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI

# Load API key from .env
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)

# Prompt
prompt = """You are a YouTube video summarizer. You will be taking the transcript text and summarizing the entire video and providing important summary in points in 200-250 words. The transcript text is appended here: """

# Extract transcript from video
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("v=")[1]
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id=video_id)
        transcript = " ".join(text["text"] for text in transcript_list)
        return transcript
    except Exception as e:
        raise e

# Generate summary using OpenAI GPT-4o
def generate_openai_content(transcript_text, prompt):
    response = client.chat.completions.create(
        model="gpt-4o",  # You can change this to gpt-3.5-turbo to reduce cost
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": transcript_text}
        ]
    )
    return response.choices[0].message.content

# Streamlit UI
st.title("🎥 YouTube Video to Notes Converter")
youtube_link = st.text_input("Enter YouTube video URL:")

if youtube_link:
    try:
        video_id = youtube_link.split("v=")[1]
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)
    except:
        st.error("Invalid YouTube link format. Please include 'v=' in the URL.")

if st.button("Get Detail Notes"):
    try:
        with st.spinner("Extracting and summarizing..."):
            transcript_text = extract_transcript_details(youtube_video_url=youtube_link)
            if transcript_text:
                summary = generate_openai_content(transcript_text=transcript_text, prompt=prompt)
                st.markdown("## 📝 Detail Notes:")
                st.write(summary)
    except Exception as e:
        st.error(f"Error: {e}")
