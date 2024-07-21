
from flask import Flask, request, render_template, send_file, Response
from gtts import gTTS
from googletrans import Translator
import os

app = Flask(__name__)

# Mapping of language codes for gTTS compatibility
LANGUAGE_CODES = {
    'en': 'en',
    'hi': 'hi',
    'es': 'es',
    'fr': 'fr',
    'de': 'de',
    'ja': 'ja',
    'or': 'or',  # Odia
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    text = request.form['text']
    target_language = request.form['language']
    speed = request.form.get('speed', 'normal')  # Get speed selection or default to 'normal'

    # Translate text
    translator = Translator()
    translated = translator.translate(text, dest=target_language)
    translated_text = translated.text

    # Use gTTS for text to speech
    gtts_language = LANGUAGE_CODES.get(target_language)
    
    if not gtts_language:
        return 'Error: Language not supported'

    tts = gTTS(translated_text, lang=gtts_language, slow=(speed == 'slow'))
    output_path = os.path.join('static', 'output.mp3')

    if not os.path.exists('static'):
        os.makedirs('static')

    tts.save(output_path)

    # Read the generated audio file
    with open(output_path, 'rb') as f:
        audio_data = f.read()

    # Return audio file data as a response
    return Response(audio_data, mimetype='audio/mpeg')

if __name__ == '__main__':
    app.run(debug=True)
