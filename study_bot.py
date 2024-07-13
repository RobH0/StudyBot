from youtube_transcript_api import YouTubeTranscriptApi
import ollama

def get_video_id():
    url = str(input("Enter a URL of a Youtube video you want to take notes on: "))
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

def download_transcript(video_id):
    video_transcript = YouTubeTranscriptApi.get_transcript(video_id)
    text_only_transcript = ''
    for line in video_transcript:
        text_only_transcript += ' ' + line['text']

    return text_only_transcript

def summarize_into_notes(transcript):
    client = ollama.Client(host='http://localhost:11434')
    #stream = client.chat(model='gemma2', messages=[{'role': 'user', 'content': 'hello are you there'}], stream=True)
    prompt_text = 'You are tasked with helping a student by summarizing a transcript from an educational video. Please summarize the following transcript into concise notes while not leaving out any key technical terms, acronyms, or definitions: ' + transcript
    stream = client.generate(model='gemma2', prompt=prompt_text, stream=True)
    print('\n')
    for chunk in stream:
        print(chunk['response'], end='', flush=True)

if __name__ == "__main__":
    video_id = get_video_id()
    if video_id != False:
        text_only_transcript = download_transcript(video_id)
        summarize_into_notes(text_only_transcript)
    