from youtube_transcript_api import YouTubeTranscriptApi
import json

video_transcript = YouTubeTranscriptApi.get_transcript("1ENiVwk8idM")
text_only_transcript = ''
for line in video_transcript:
    text_only_transcript += ' ' + line['text']


text_only_transcript = text_only_transcript.replace("\n", "")
print(text_only_transcript)