from flask import Flask, render_template, request, send_file
import io
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

    # Use in-memory buffer to store the generated audio
    audio_buffer = io.BytesIO()
    engine.save_to_file(text, audio_buffer)
    engine.runAndWait()

    # Set the buffer position to the beginning
    audio_buffer.seek(0)

    # Return the generated audio file as a response without saving it to the server
    return send_file(
        audio_buffer,
        as_attachment=True,
        download_name='generated_audio.mp3',
        mimetype='audio/mpeg'
    )

if __name__ == '__main__':
    #host on port 5001
    app.run(debug=True, port=5001)
