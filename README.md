# Text-to-Speech App (Bulgarian Support via ElevenLabs)

This Flask web app allows you to upload a DOCX or PDF file, extract its text, and convert it to audio using ElevenLabs' Bulgarian text-to-speech API.

## Features
- Upload .docx or .pdf
- Bulgarian AI voiceover
- Generates downloadable .mp3 files

## Setup

```bash
git clone https://github.com/yourusername/tts-app.git
cd tts-app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Add your ElevenLabs API key
echo "ELEVEN_LABS_API_KEY=your_api_key_here" > .env
