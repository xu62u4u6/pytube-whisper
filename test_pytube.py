from pytube import YouTube
import openai
import configparser
config = configparser.ConfigParser()
config.read('config.ini')
openai.api_key = config["openai"]["key"]

url = "https://www.youtube.com/watch?v=_lD8JyAbwEo&t=1s"
yt = YouTube(url)
print(yt.title)
filename = f'{yt.title}.mp3'
yt.streams.filter(only_audio=True).first().download(filename=filename)

audio_file= open(filename, "rb")
transcript = openai.Audio.transcribe("whisper-1", audio_file)
print(transcript)

messages=[{"role": "system", "content": "translate to Chinese"}, 
        {"role": "user", "content": transcript["text"]}
]


res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=messages)

reply = res.choices[0].message.content
print(reply)