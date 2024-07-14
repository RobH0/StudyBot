from youtube_transcript_api import YouTubeTranscriptApi
import ollama
import requests
from bs4 import BeautifulSoup


def get_video_id(url):
    if "youtube.com/watch?v=" in url:
        print("\nValid URL")
        start_index = url.find('=') + 1
        end_index= start_index + 11
        id = url[start_index:end_index]
        return id
    else:
        print("Invalid URL. URL must link to a youtube video.")
        return False

def get_video_title(url):
    response = requests.get(url)

    if response.status_code != 200:
        print('Failed to retrieve webpage')
        return False
    
    parsed_html = BeautifulSoup(response.content, 'html.parser')
    video_title = parsed_html.title.string.replace(' - YouTube', '')

    return video_title

def download_transcript(video_id):
    video_transcript = YouTubeTranscriptApi.get_transcript(video_id)
    text_only_transcript = ''
    for line in video_transcript:
        text_only_transcript += ' ' + line['text']

    return text_only_transcript

def summarize_into_notes(transcript, video_title):
    try:
        ollama_host = 'http://localhost:11434' # Change if you are running Ollama on a remote machine or if it's running on a non-default port.
    
        client = ollama.Client(host=ollama_host)

        model_name = 'gemma2' # Change if you are using a different model.
        prompt_text = f"You are tasked with summarizing a transcript from an educational video to help a student. Please create concise notes that include all key technical terms, acronyms, concepts, commands (with arguments), steps, and definitions from the transcript. Transcript: {transcript}. Use the video title ({video_title}) and the transcript to write an appropriate title for the notes. Format the notes in Markdown, wrapping commands and code in backticks. Exclude any Ad/Advert content. Ensure the video title is referenced within the notes for easy identification by the student. The notes should be concise (but don't oversimplify) and well formated using markdown to make it easier to study from."

        print("\nStarting notes generation...\n")
        stream = client.generate(model=model_name, prompt=prompt_text, stream=True)

        notes = ''
        for chunk in stream:
            print(chunk['response'], end='', flush=True)
            notes += chunk['response']
        return notes
    except:
        print('Notes generation request failed.\nMake sure your ollama server is running.\n')
        return False

def save_notes_md(notes, video_title):
    filename = video_title + '.md'
    with open(filename, "w") as file:
        file.write(notes)


if __name__ == "__main__":

    print("""   
  ______                _       ______             
 / _____) _            | |     (____  \\        _   
( (____ _| |_ _   _  __| |_   _ ____)  ) ___ _| |_ 
 \\____ (_   _) | | |/ _  | | | |  __  ( / _ (_   _)
 _____) )| |_| |_| ( (_| | |_| | |__)  ) |_| || |_ 
(______/  \\__)____/ \\____|\\__  |______/ \\___/  \\__)
                         (____/                    

          """)
    url = str(input("Enter a URL of a Youtube video you want to take notes on: "))
    filename = str(input("What do you want the generated notes file to be called? "))
    video_id = get_video_id(url)
    if video_id != False:
        video_title = get_video_title(url)
        if video_title != False:
            print('\nVideo Info:')
            print(' - Title: ' + video_title)
            print(' - ID: ' + video_id)
            text_only_transcript = download_transcript(video_id)
            notes = summarize_into_notes(text_only_transcript, video_title)
            if notes != False:
                save_notes_md(notes, filename)
        
    