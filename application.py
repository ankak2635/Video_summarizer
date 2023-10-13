import streamlit as st
from src.utils import utils

def main():
    """
    Main function for the Video Summarizer web application.

    This function sets up a Streamlit web application for summarizing audio/video content.
    Users can paste a URL of a YouTube video or podcast, and the application will download the media,
    transcribe it, preprocess the transcription, and generate a summary.

    Returns:
        None

    Example:
    To run the application, simply execute this script. It will launch a web interface where users can input a URL
    and get a summary of the content.
    """
    # initaite the utils class
    utility = utils()

    # set webpage config
    st.set_page_config(page_title="Video Summarizer")

    # A header and details
    st.header("Video Summarizer")
    st.write("Paste a audio/video URL on the sidebar and get the summary of the content below.")

    summary = ''

    # Sidebar for processing the url
    with st.sidebar:
        st.subheader("Paste a URL of the content")
        st.text("A YouTube video or a podcast")
        url = st.text_input('URL link')

        # create a download button
        if st.button("Process"):
            with st.status("Processing..."):

                # download the audio from the url
                st.write("Downloading media...")
                audio_file = utility.download_media(url=url)

                # transcribe the audio
                st.write("Transcribing...")
                utility.transcribe()

                # create chunks
                st.write("Preprocessing the transcription...")
                docs = utility.split_transcript()

                # summarize the doc
                st.write("Generating summary...")
                summary = utility.summarize_text(docs)
    
    # Display the summary in the main page
    st.write(summary)


# if __name__ =="__main__":
#     main()

