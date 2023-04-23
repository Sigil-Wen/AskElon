import requests
import zipfile
import io

# Set the URL of the zip file
model_url = "https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip"

# Download the zip file
response = requests.get(model_url)
if response.status_code == 200:
    # Extract the contents of the zip file to the current directory
    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
        zip_ref.extractall()