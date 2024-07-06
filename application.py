import streamlit as st
from src.utils import utils

# Initiate the utils class
utility = utils()

# Set webpage config
st.set_page_config(page_title="Video Summarizer")

# A header and details
st.header("Video Summarizer")
st.write("Paste an audio/video URL on the sidebar and get the summary of the content below.")

summary = ''

# Sidebar for processing the URL
with st.sidebar:
    st.subheader("Paste a URL of the content")
    st.text("A YouTube video or a podcast")
    url = st.text_input('URL link')

    # Create a download button
    if st.button("Process"):
        with st.spinner("Processing..."):
            try:
                # Download the audio from the URL
                st.write("Downloading media...")
                utility.download_media(url=url)

            except Exception as e:
                st.error(f"An error occurred during video download")
                st.stop()

            try:
                # Transcribe the audio
                st.write("Transcribing...")
                utility.transcribe()

            except Exception as e:
                st.error(f"An error occurred during audio transcription")
                st.stop()

            try:
                # Create chunks
                st.write("Preprocessing the transcription...")
                docs = utility.split_transcript()

            except Exception as e:
                st.error(f"An error occurred during text splitting")
                st.stop()

            try:
                # Summarize the doc
                st.write("Generating summary...")
                summary = utility.summarize_text(docs)

            except Exception as e:
                st.error(f"An error occurred during summarization")
                st.stop()

# Display the summary on the main page
st.write(summary)
