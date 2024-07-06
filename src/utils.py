import yt_dlp
import whisper 
import textwrap
import torch
import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

load_dotenv()

class utils():
    def __init__(self):
        pass
        

    # download only audio from YouTube and transcribe
    def download_media(self, url):
        """
            This function takes a audio/video URL (downloads only audio from the media) and downloads it. 
            
            Args:
                url (str): The URL of the media to be downloaded and transcribed.

            Raises:
                Exception: If any errors occur during the audio download or transcribing process, an error message is printed.
                
        """
        
        try:

            # delete any pre-existing audio and transcript
            audio_file = 'audio.mp3'
            transcript_file = 'text.txt'

            if os.path.exists(audio_file):
                os.remove(audio_file)
            if os.path.exists(transcript_file):
                os.remove(transcript_file)
                
            # Set the options for audio download
            filename = 'audio.mp3'
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': filename,
                'quiet': True,
            }

            # Download the audio using yt_dlp
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                audio_file = ydl.download([url])

            return audio_file

            
        except yt_dlp.utils.DownloadError as de:
            raise Exception(f"An error occurred during video download: {de}")
        

    # transcribe the video
    def transcribe(self):
        """
        Transcribe audio content using the Whisper library.

        This function takes an audio file as input and transcribes its content using the Whisper library, specifically the 'tiny' model.

        Args:
            audio_file (str): The audio file to be transcribed.

        Returns:
            dict: A dictionary containing the transcription results, including the transcribed text and additional information.

        Raises:
            Exception: If any unexpected errors occur, an error message is printed.

        """

        try:
            device = "cuda:0" if torch.cuda.is_available() else "cpu"

            # Transcribe the audio content using the 'tiny' Whisper model
            model = whisper.load_model('tiny')
            model.to(device)
            transcription = model.transcribe('./audio.mp3')

            # save as text file
            with open ('text.txt', 'w') as file:  
                file.write(transcription['text'])

        except Exception as e:
            raise Exception(f"An error occurred during audio transcription: {e}")



    def split_transcript(self):
        """
        Split and segment a text document into smaller chunks for further processing.

        This function takes a text document, divides it into smaller segments, and creates a list of document objects.
        It is typically used in a larger workflow, such as transcribing a video and then segmenting the transcription into manageable portions for summarization.

        Returns:
            List[Document]: A list of document objects, each containing a portion of the text document.

        Raises:
            Exception: If any errors occur during text splitting, an error message is printed.
            """
        try:
            # create an instance of text splitter
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, chunk_overlap =50, separators=[' ', ',', '\n']
                )
            
            with open('text.txt') as f:
                text = f.read()

             # split the text
            splitted_text = text_splitter.split_text(text)
            docs = [Document(page_content=t) for t in splitted_text]
            
            return docs

        except Exception as e:
            raise Exception(f"An error occurred during text splitting: {e}")



    def summarize_text(self, docs):
        """
    Summarizes the provided text documents using OpenAI's GPT-3.5-turbo model.

    This function takes a list of text documents, constructs a custom prompt to request
    a concise summary, and processes the request through a summarization chain using the
    GPT-3.5-turbo model. The resulting summary is then formatted for readability.

    Args:
        docs (list of str): A list of text documents to be summarized.

    Returns:
        str: A formatted string containing the concise summary of the input text documents.

    Raises:
        Exception: If any unexpected errors occur during the summarization process, 
                   an error message is printed.
        """

        try:
            # Define the prompt template
            prompt_template = """Write a concise summary of the following:

            {text}

            CONCISE SUMMARY:"""

            custom_prompt = PromptTemplate(template=prompt_template, input_variables=['text'])

            llm = ChatOpenAI(temperature=0, model='gpt-3.5-turbo')

            # Prepare the chain
            chain = load_summarize_chain(
                llm=llm,
                chain_type='stuff',
                prompt=custom_prompt
            )

            # Get the summary
            response = chain.invoke(docs)
            output_summary = response["output_text"]

            # Format text
            wrapped_text = textwrap.fill(output_summary,
                                        width=100,
                                        break_long_words=False,
                                        replace_whitespace=False)

            return wrapped_text

        except Exception as e:
            raise Exception(f"An error occurred during summarization: {e}")


# if __name__ == '__main__':
#     # url = 'https://www.youtube.com/watch?v=bxuYDT-BWaI'
#     obj = utils()
#     doc = obj.split_transcript()
#     summ = obj.summarize_text(doc)
#     print(summ)
    
  
    