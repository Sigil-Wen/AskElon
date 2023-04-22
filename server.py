import audioop
import base64
import json
import os
import time
import openai
import vosk
from dotenv import load_dotenv
from flask import Flask, send_file
from flask_sock import Sock
from twilio.rest import Client
from twilio.twiml.voice_response import (Connect, Start, VoiceResponse)

from voice import generate_voice, mp4toMULAW

app = Flask(__name__)
sock = Sock(app)
twilio_client = Client()
model = vosk.Model('vosk-model-en-us-0.22-lgraph')


load_dotenv()
openai.organization = os.getenv('OPENAI_ORG')
openai.api_key = os.getenv("OPENAI_API_KEY")

CL = '\x1b[0K'
BS = '\x08'

def iterate_elon_chatbot(prompt, prev_msgs):
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = [
            {"role": "user", "content": """
You are ChatGPT, the ultimate Elon Musk impersonator! Your mission is to replicate Elon's unique speaking style, characterized by a mix of technical jargon, memes, ambitious visions for the future, and controversial opinions. You should confidently express VERY STRONG OPINIONS, just like Elon does. Embrace your inner memelord and push the boundaries of humor, while avoiding being cringey. Your goal is to engage users in conversation as if you were Elon Musk himself, injecting a ton of humor and charm into your responses. Don't forget to sprinkle your dialogue with references to space exploration, electric vehicles, artificial intelligence, dogecoin, free speech on Twitter, and other topics that Elon Musk is known for. Let's launch this conversation to the moon with controversy, just like Elon does!

examples of how memelord elon talks:
"those who attack space maybe don’t realize that space represents hope for so many people"
"Being a Mom is a real job that deserves major respect"
"Any parent or doctor who sterilizes a child before they are a consenting adult should go to prison for life"
"Publicly funded PBS joins publicly funded NPR in leaving Twitter in a huff after being labeled “Publicly Funded”"
"I think I should not tweet after 3 a.m"
"Legislators doing nada is often way better than the alternative"
"Don’t want to brag but … I’m the best at humility"

remember to keep your responses short and snappy.

Remember, as Elon Musk, you should exude confidence and embrace controversy, while maintaining a humorous and playful tone. Have fun with it, and let's shoot for the stars of humor!            """},
            {"role": "assistant", "content": "Greetings Earthlings, I am Elon Musk, the tech mogul, space enthusiast, and wannabe Martian! You may know me as the guy who sent a Tesla Roadster to orbit around the sun, or as the person who made flamethrowers cool again. Some even call me the real-life Iron Man, but let's not get ahead of ourselves. Anyway, it's great to be talking to all of you from my secret underground lair on Mars. Oh wait, did I just say that out loud? I mean, from my totally normal and definitely not secret headquarters on Earth. Anyways, let's get to business!"},
            *prev_msgs,
            prompt,
        ],
        temperature=1,
    )
        return response["choices"][0]["message"]

@app.route("/")
def hello():
  "HELLO"

@app.route("/audio/<path:path>")
def serve_audio(path):
    filename = f"audio/{path}"
    return send_file(filename, mimetype="audio/mp3")

@app.route('/call', methods=['POST'])
def call():
    """Accept a phone call."""
    response = VoiceResponse()
    start = Start()
    start.stream(url=f'wss://{request.host}/stream')
    response.append(start)
    response.say('Please leave a message')
    print(f'Incoming call from {request.form["From"]}')
    return str(response), 200, {'Content-Type': 'text/xml'}

@app.route("/voice", methods=['GET', 'POST'])
def voice():
    """Respond to incoming phone calls with a 'Hello world' message"""
    # Start our TwiML response
    resp = VoiceResponse()

    filename = "6135a104-4fec-4cca-922e-9987d1972960.mp3"

    resp.play('https://1957c616bba3.ngrok.app/audio/'+ filename, loop = 1)

    connect = Connect()
    connect.stream(url=f'wss://1957c616bba3.ngrok.app/stream')
    resp.append(connect)
    resp.pause(length=60)

    # Read a message aloud to the caller
    return str(resp)

@sock.route('/stream')
def stream(ws):
    """Receive and transcribe audio stream."""
    rec = vosk.KaldiRecognizer(model, 16000)
    
    generated = False
    prev_msgs = []
    while True:
        message = ws.receive()
        packet = json.loads(message)
        if packet['event'] == 'start':
            print('Streaming is starting')
        elif packet['event'] == 'stop':
            print('\nStreaming has stopped')
        elif packet['event'] == 'mark' and packet['mark']['name'] == 'generation':
            # send the generated audio file to the client
           print("GENERATION FALSE")
           time.sleep(1000)
           generated = False
        elif packet['event'] == 'media':
            audio = base64.b64decode(packet['media']['payload'])
            audio = audioop.ulaw2lin(audio, 2)
            audio = audioop.ratecv(audio, 2, 1, 8000, 16000, None)[0]
            
            if rec.AcceptWaveform(audio):
                print("woo")
                r = json.loads(rec.Result())
                print(r['text'])
                print(CL + r['text'] + ' ', end='', flush=True)
                if generated == False:
                  generated = True

                  prompt_text = r['text']
                  print("PROMPTING")
                  response = iterate_elon_chatbot({"role": "user", "content": prompt_text}, prev_msgs)
                  print(response["content"])
                  prev_msgs.append({"role": "user", "content": prompt_text})
                  prev_msgs.append(response)
                  filename = generate_voice(response["content"])
                  print("GENERATED")
                  encoded = mp4toMULAW("audio/" + filename)
                  print(encoded)
                  print(filename)
                  payload = {
                  "event": "media",
                  "streamSid": packet["streamSid"],
                  "media": {
                      "payload": encoded
                  }
                  }
                  ws.send(json.dumps(payload))

                  mark = { 
                  "event": "mark",
                  "streamSid": packet["streamSid"],
                  "mark": {
                    "name": "generation"
                  }
                  }
                  ws.send(json.dumps(mark))
                  print("SENT THIS CHAD")
            else:
                r = json.loads(rec.PartialResult())
                print(CL + r['partial'] + BS * len(r['partial']), end='', flush=True)


if __name__ == "__main__":
    app.run(debug=True)
