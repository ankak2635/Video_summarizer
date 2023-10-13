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
    def download_audio(self, url):
        """
            This function takes a video URL, downloads only audio of the video, and transcribes it content to text.
            
            Args:
                url (str): The URL of the video to be downloaded and transcribed.

            Raises:
                Exception: If any errors occur during the video download or transcription process, an error message is printed.
                
        """
        try:
            # Set the options for audio download
            filename = 'audio_1.mp3'
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': filename,
                'quiet': True,
            }
            
            # Download the audio using yt_dlp
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info(url, download=True)

            # Transcribe the audio content
            model = whisper.load_model('base')
            transcription = model.transcribe('audio.mp3')

            # Save the transcript as a text file
            with open('text.txt', 'w') as file:
                file.write(transcription['text'])

        except Exception as e:
            print(f"An error occurred during video download or transcription: {e}")

    
    def _split_transcript(self):
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

            # read the text document
            with open('text.txt') as file:
                text = file.read()

            # split the text
            splitted_text = text_splitter.split_text(text)
            docs = [Document(page_content=t) for t in splitted_text[:4]]
            return docs

        except Exception as e:
            print(f"An error occurred during text splitting: {e}")


    # summarize the transcript
    def summarize_text(self):
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
            # get the doc from split_transcript function
            docs= self._split_transcript()

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







if __name__ == '__main__':
    url = 'https://www.youtube.com/watch?v=mBjPyte2ZZo'
    obj = utils()
    obj.download_audio(url=url)
  
    