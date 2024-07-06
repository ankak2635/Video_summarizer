# Video Summarizer

**Video Summarizer** is a Streamlit web application developed in Python that allows you to efficiently summarize the content of video and audio media. It simplifies the process of summarizing video or audio content by taking a URL as input and providing a concise summary in minutes.

**Experience it first-hand [here](https://ak-videosummarizer.streamlit.app/):**

## Key Libraries Used

The application leverages several key libraries to perform its tasks effectively:

1. **yt_dlp**: Used for downloading the audio component of media content from the provided URL.

2. **OpenAI's Whisper**: Utilized for transcribing the downloaded audio with great accuracy. 

3. **LangChain**: Provides essential components for text manipulation and summarization.

4. **GPT 3.5-turbo**: Used to process the chunked texts and generate summaries.

## Workflow

The workflow of the Video Summarize application is structured as follows:

1. **Streamlit**: The web application is created and hosted using Streamlit, allowing users to interact with the tool in a user-friendly manner.

2. **yt_dlp**: This library is responsible for downloading the audio component of media from the provided URL, enabling users to work with audio content directly.

3. **OpenAI's Whisper**: Whisper is used to transcribe the downloaded audio, delivering highly accurate transcriptions.

4. **LangChain's RecursiveCharacterTextSplitter**: This component is employed to split the transcript into smaller, manageable chunks, making it easier to process and summarize.

5. **LangChain's prompt_template**: It allows you to create custom prompts that guide the language model in summarization.

6. **GPT 3.5-turbo**: This powerful language model processes the chunked texts, transforming them into concise and informative summaries.

7. **LangChain's load_summarize_chain**: This function chains the custom prompt and LLM together, creating a coherent pipeline for summarization.

With this streamlined workflow, Video Summarize simplifies the process of summarizing video and audio content, making it more accessible and efficient for users.

## How to Use Video Summarize

1. Paste a video or audio URL in the provided input field.
2. Click the "Process" button.
3. The application will initiate the summarization process, downloading the audio, transcribing it, splitting the transcript, and generating a concise summary.
4. The summary will be displayed, providing you with the key insights from the media content.

## Feedback and Contributions

I encourage you to provide feedback, report issues, and contribute to the development of Video Summarize. You can do so by opening issues on our GitHub repository and submitting pull requests.

We hope you find Video Summarize useful and look forward to seeing how it can assist you in summarizing media content efficiently.

---

*This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.*
