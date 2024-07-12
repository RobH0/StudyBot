from youtube_transcript_api import YouTubeTranscriptApi
import json


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

if __name__ == "__main__":
    video_id = get_video_id()
    if video_id != False:
        text_only_transcript = download_transcript(video_id)
        print(text_only_transcript)
    