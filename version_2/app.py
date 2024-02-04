from flask import Flask, render_template, request, send_file
import os
import pyttsx3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_audio', methods=['POST'])
def generate_audio():
    text = request.form.get('input_text')
    voice_preference = int(request.form.get('voice'))

    # Generate audio using pyttsx3
    engine = pyttsx3.init()

    # Change voice based on user preference
    voices = engine.getProperty('voices')
    selected_voice = voices[voice_preference].id
    engine.setProperty('voice', selected_voice)

    # Set other properties
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 0.9)

    # Save generated audio to file
    engine.save_to_file(text, 'generated_audio.mp3')
    engine.runAndWait()

    # Return the generated audio file as a response
    return send_file('generated_audio.mp3', as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

