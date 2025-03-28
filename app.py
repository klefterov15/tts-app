from flask import Flask, request, render_template, send_file
import os
import docx
import PyPDF2
import requests
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

# Replace with your actual ElevenLabs API key
ELEVEN_LABS_API_KEY = os.getenv("ELEVEN_LABS_API_KEY")

# Choose a Bulgarian voice from ElevenLabs (update if needed)
VOICE_ID = "kzrsjZhHCumKqmkJl486"  # Example voice ID, replace with an actual Bulgarian voice ID

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'your_secret_key_here'  # Replace with a secure key

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('document')
        if not file:
            return "No file uploaded.", 400

        # Save the uploaded file
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            # Extract text from the document
            extracted_text = extract_text(filepath)
        except Exception as e:
            return f"Error extracting text: {e}", 500

        if not extracted_text.strip():
            return "No text could be extracted from the file.", 400

        try:
            # Convert text to speech using ElevenLabs
            audio_content = text_to_speech(extracted_text)
        except Exception as e:
            return f"Error generating audio: {e}", 500

        # Remove the uploaded file after processing
        os.remove(filepath)

        # Return the generated MP3 file
        return send_file(
            BytesIO(audio_content),
            mimetype='audio/mpeg',
            as_attachment=True,
            download_name='output.mp3'
        )

    return render_template('index.html')

def extract_text(filepath):
    """Extract text from DOCX or PDF files."""
    _, extension = os.path.splitext(filepath)
    extension = extension.lower()

    if extension == '.docx':
        return extract_text_from_docx(filepath)
    elif extension == '.pdf':
        return extract_text_from_pdf(filepath)
    else:
        raise ValueError("Unsupported file type. Please upload a DOCX or PDF file.")

def extract_text_from_docx(docx_path):
    """Extract text from a DOCX file."""
    doc = docx.Document(docx_path)
    full_text = [para.text for para in doc.paragraphs]
    return "\n".join(full_text)

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    text = []
    with open(pdf_path, 'rb') as f:
        pdf_reader = PyPDF2.PdfReader(f)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
    return "\n".join(text)

def text_to_speech(text):
    """Convert text to speech using ElevenLabs API."""
    api_url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "Content-Type": "application/json",
        "xi-api-key": ELEVEN_LABS_API_KEY
    }
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",  # Bulgarian is supported under multilingual
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    response = requests.post(api_url, headers=headers, json=data)
    response.raise_for_status()

    # The response contains binary MP3 audio
    return response.content

if __name__ == "__main__":
    app.run(debug=True)
    
    
    # 