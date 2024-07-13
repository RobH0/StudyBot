from youtube_transcript_api import YouTubeTranscriptApi
import ollama
import requests
from bs4 import BeautifulSoup


def get_video_id(url):
    if "youtube.com/watch?v=" in url:
        print("Valid url")
        start_index = url.find('=') + 1
        end_index= start_index+11
        id = url[start_index:end_index]
        print("id " + str(id))
        return id
    else:
        print("Invalid URL. Must be a link to a youtube video.")
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
    client = ollama.Client(host='http://localhost:11434')
    
    prompt_text = f"You are tasked with summarizing a transcript from an educational video to help a student. Please create concise notes that include all key technical terms, acronyms, concepts, commands (with arguments), steps, and definitions from the transcript. Transcript: {transcript}. Use the video title ({video_title}) and the transcript to write an appropriate title for the notes. Format the notes in Markdown, wrapping commands and code in backticks. Exclude any Ad/Advert content. Ensure the video title is referenced within the notes for easy identification by the student. The notes should be concise (but don't oversimplify) and well formated using markdown to make it easier to study from."

    stream = client.generate(model='gemma2', prompt=prompt_text, stream=True)
    print('\n')
    
    notes = ''
    for chunk in stream:
        print(chunk['response'], end='', flush=True)
        notes += chunk['response']
    
    return notes

def save_notes_md(notes, video_title):
    filename = video_title + '.md'
    with open(filename, "w") as file:
        file.write(notes)


if __name__ == "__main__":
    url = str(input("Enter a URL of a Youtube video you want to take notes on: "))
    video_id = get_video_id(url)
    if video_id != False:
        video_title = get_video_title(url)
        if video_title != False:
            text_only_transcript = download_transcript(video_id)
            notes = summarize_into_notes(text_only_transcript, video_title)
            save_notes_md(notes, video_title)
        
    