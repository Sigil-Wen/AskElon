# AskElon

![Elon on the phone winking at you](./assets/elon_musk_winking_phone.png)

We created Ask Elon 417-ASK-ELON, a Twilio number you can call and talk to an AI Elon Musk. Built as part of the 8 hour Toronto Cohere, Replit, & Chroma AI Hackathon using Twilio's Programmable Voice API, Vosk's Transcription model, Ngrok (Hosts local servers to the web), Flask, OpenAI's GPT3.5, and Eleven Labs.

# Setup

### On Device (Near real time)Transcription

We use vosk-model-en-us-0.22, an open source1.8G Accurate generic US English model under Apache 2.0 License.

You can download the model here: https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip and place it in the project root directory

### Ngrok & Webhooks

Ngrok forwards a localhost port to a public web server. To set up Ngrok run ngrok

```
ngrok http 8080
```

With the generated ngrok server, you can update the twilio voice url webhook through the twilio CLI

```
 twilio phone-numbers:update 1417696969 --voice-url https://1957yourserver.ngrok.app/voice
```

### Elon Musk Voice Generation

We use eleven labs, you can generate an API key and create your voice here: https://beta.elevenlabs.io/voice-lab

### Starting Flask & Websockets Server

```
pip install -r requirements.txt

 python server.py
```

# Resources:

Some great resources:

-   https://github.com/twilio/media-streams
-   On Audio Encoding: https://cloud.google.com/speech-to-text/docs/encoding
-   Twilio Media Streams (Web Socket Protocol): https://www.twilio.com/docs/voice/twiml/stream#message-media-to-twilio

Dependencies (Could be optimized)

-   ffmpeg
-   sox
