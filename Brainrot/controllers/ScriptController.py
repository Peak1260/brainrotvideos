import os
import random
from openai import OpenAI
from dotenv import load_dotenv
import whisper_timestamped as whisper
import requests

load_dotenv()

class ScriptController:
    def __init__(self):
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
        self.client = OpenAI(api_key=self.OPENAI_API_KEY)


    def generate_script(self, system_content, user_content, model, script_path):
        try:
            completion = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_content},
                    {"role": "user", "content": user_content}
                ]
            )
            with open(script_path, 'w') as script_file:
                script_file.write(completion.choices[0].message.content)
                
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Error generating script: {e}")
            return None
        
    
    def generate_audio(self, text, provider, audio_path):
        if provider == "openai":
            response = self.client.audio.speech.create(
                model="tts-1-hd",
                voice="onyx",
                input=text,
            )
            response.stream_to_file(audio_path)

        elif provider == "elevenlabs":
            CHUNK_SIZE = 1024
            url = "https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB"

            headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.ELEVENLABS_API_KEY
            }

            data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
            }

            response = requests.post(url, json=data, headers=headers)
            with open(audio_path, 'wb') as audio_file:
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    if chunk:
                        audio_file.write(chunk)
        