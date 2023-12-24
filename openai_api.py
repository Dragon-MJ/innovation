from openai import OpenAI

from pathlib import Path
import openai
import ipdb 


def tts(text, speech_output_path='temp.mp3'):
    response = openai.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )
    response.stream_to_file(speech_output_path)


def tts_dummy(text):
    pass


def chat(text):
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": text}
        ]
    )

    return completion.choices[0].message.content


def chat_dummy(text):
    return "hello, world!"


def stt(audio_file):

    client = OpenAI()

    audio_file= open(audio_file, "rb")
    transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )
    return transcript.text

def stt_dummy(audio_file):
    return "hello"


# audio_path = "output.mp3"
# text = stt(audio_path)
# text = chat(text)
# tts(text)