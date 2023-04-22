import requests
import uuid
import base64
import subprocess
from pydub import AudioSegment
import os
import audioop
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv('ELEVENLABS_API_KEY')
voice_id = os.getenv('ELEVENLABS_VOICE_ID')


def generate_voice(text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }

    data = {
        "text": text,
        "voice_settings": {
            "stability": 0.75,
            "similarity_boost": 0.75
        }
    }

    response = requests.post(url, headers=headers, json=data)
    file_name = str(uuid.uuid4()) + ".mp3"

    if response.ok:

        with open("audio/"+  file_name, "wb") as f:
            f.write(response.content)
    else:
        print(f"Error generating voice: {response.status_code} {response.text}")
    return file_name

def mp4toMULAW(filename):
  # Set the FFMPEG_PATH environment variable

  
  os.environ["FFMPEG_PATH"] = "/usr/local/bin/ffmpeg"
  subprocess.run(['ffmpeg', '-i', filename, 'audio_file.wav'])

  # Load the WAV file
  with open('audio_file.wav', 'rb') as wav_file:
    audio_data = wav_file.read()  
  
  # Convert the audio data to 8-bit mulaw format with a sample rate of 8000
  # Convert the audio data to 16-bit PCM format with a sample rate of 8000
  audio_data = audioop.ratecv(audio_data, 2, 1, 44100, 8000, None)[0]
  audio_data = audioop.lin2ulaw(audio_data, 2)

  # Pad the audio data to ensure a whole number of frames
  num_frames = len(audio_data) // 160
  audio_data += b'\x00' * (160 - len(audio_data) % 160)

  # Base64 encode the audio data
  audio_data_b64 = base64.b64encode(audio_data).decode('utf-8')
  os.remove('audio_file.wav')

  # # Load the MP4 file
  # audio = AudioSegment.from_file(filename)

  # # Convert the audio to Raw mulaw/8000 format
  # raw_audio = audio.set_frame_rate(8000).set_channels(1).raw_data

  # # Encode the Raw mulaw/8000 audio in Base64
  # base64_audio = base64.b64encode(raw_audio).decode('utf-8')

  # Print the encoded audio string
  return audio_data_b64

# lesgo = mp4toMULAW("audio/1ee6c685-b5ac-49c4-9293-100dee8c1037.mp3")
# print("LESGO")
# print(lesgo)