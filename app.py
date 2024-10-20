from dotenv import load_dotenv
import streamlit as st
load_dotenv() ##load all the nevironment variables
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

print(os.getenv("GOOGLE_API_KEY"))
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt="""You are Yotube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here:  """
def extract_transcript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("v=")[1]
        print(video_id)
        
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e
    
    
def generate_gemini_content(transcript_text,prompt):

    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)
    return response.text

# youtube_link = input("enter the youtube video link: ")
# transcript_text=extract_transcript_details(youtube_link)

# # print(transcript_text)
# summary=generate_gemini_content(transcript_text,prompt)
# print(summary)
st.title("YouTube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id = youtube_link.split("v=")[1]
    print(video_id)
    st.image(f"https://i.ytimg.com/vi/{video_id.split("&")[0]}/hqdefault.jpg", use_column_width=True)

if st.button("Get Detailed Notes"):
    transcript_text=extract_transcript_details(youtube_link)

    if transcript_text:
        summary=generate_gemini_content(transcript_text,prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)