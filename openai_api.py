from openai import OpenAI

from pathlib import Path
import openai, os
import ipdb 


api_key = os.getenv("OPENAI_API_KEY")


def tts(text, speech_output_path='temp.mp3'):

    OpenAI(api_key=api_key)

    response = openai.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )
    response.stream_to_file(speech_output_path)


def tts_dummy(text, speech_output_path='temp.mp3'):

    tts_dummy_text = "good"

    return speech_output_path


def chat(text):
    client = OpenAI(api_key=api_key)

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "assistent", "content": text},
            {"role": "user", "content": text},
            {"role": "user", "content": text},
            {"role": "user", "content": text}
        ]
    )

    return completion.choices[0].message.content


def summary_dummy(text):
    
    take_data = text
    prompt = "대화내용을 일기형태로 요약해서 작성해줘. 전체 내용을 포괄하는 제목을 지어주고, 나머지 내용은 핵심내용을 요약해서 표현해주고"

    result = "오늘은 아주 멋진 하루를 보냈습니다. 아침에 일어나서 신문을 읽고, 하루 일과를 돌아보고, 정리하는 시간을 가졌습니다."

    return result


def summary(text):
    OpenAI(api_key=api_key)

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "이 대화내용을 일기형태로 요약해서 작성해줘. 전체 내용을 포괄하는 제목을 지어주고, 나머지 내용은 핵심내용을 요약해서 표현해주고, 전체적인 내용을 마지막에 요약정리해서 보여줘."},
            {"role": "assistent", "content": text},
        ]
    )
    return completion.choices[0].message.content


def generate_img(text):
    OpenAI(api_key=api_key)
    
    response = client.images.generate(
        model="dall-e-3",
        prompt=text,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url

    return image_url


def generate_img_dummy(text):

    image_url = 'https://bradaronson.com/wp-content/uploads/2013/10/happy.jpg'

    return image_url



def chat_dummy(text):
    return "good, morning!"


def stt(audio_file):

    OpenAI(api_key=api_key)

    audio_file= open(audio_file, "rb")
    transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )
    return transcript.text


def stt_dummy(audio_file):
    return "hello"

def summary(text: str) -> str:
    return "temp"
