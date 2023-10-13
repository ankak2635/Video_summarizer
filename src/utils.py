import yt_dlp
import whisper 
import textwrap

from langchain import OpenAI
from  langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document



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
            print(f"An error occurred during video download: {de}")
        

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
            # Transcribe the audio content using the 'tiny' Whisper model
            model = whisper.load_model('tiny')
            transcription = model.transcribe('audio.mp3')

            # save as text file
            with open ('text.txt', 'w') as file:  
                file.write(transcription['text'])

        except Exception as e:
            print(f"An error occurred during audio transcription: {e}")



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
            print(f"An error occurred during text splitting: {e}")


    # summarize the transcript
    def summarize_text(self,docs):
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

            # load the openai model
            llm=OpenAI(model='text-davinci-003', temperature=0)

            # define the prompt template
            prompt_template = """Write a concise summary of the following:

            {text}

            CONSCISE SUMMARY:"""

            custom_prompt = PromptTemplate(template=prompt_template, input_variables=['text'])

            chain = load_summarize_chain(
                llm=llm,
                chain_type='stuff',
                prompt = custom_prompt
            )

            # get the summary
            output_summary = chain.run(docs)

            # format text
            wrapped_text = textwrap.fill(output_summary, 
                             width=100,
                             break_long_words=False,
                             replace_whitespace=False)
        
            return wrapped_text


        except Exception as e:
            print(f"An error occurred during summarization: {e}")



# if __name__ == '__main__':
#     # url = 'https://www.youtube.com/watch?v=mBjPyte2ZZo'
#     obj = utils()
#     res = obj.summarize_text()
#     print(res)
  
    