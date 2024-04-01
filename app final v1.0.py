# recognized speech to ck editor
from flask import Flask, render_template, request, jsonify
import os
from speech_recognition_module import start_recognition, stop_recognition

# Get the directory of the current script
current_directory = os.path.dirname(os.path.abspath(__file__))
text_file_path = os.path.join(current_directory, 'conversation.txt')
audio_text = ""

with open(text_file_path) as text_file:
    default_text_to_send = text_file.read()
    print(default_text_to_send)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_text', methods=['POST'])
def send_text():
    # Get the text from the AJAX request
    received_data = request.form
    text_to_send = received_data.get('text', default_text_to_send)

    # Send the text back to the frontend without processing
    return jsonify({'processed_text': text_to_send})

@app.route('/recognize_audio', methods=['POST'])
def recognize_audio():
    audio_text = start_recognition()
    return jsonify({'audio_text': audio_text})

@app.route('/stop_audio_recognition', methods=['GET'])
def stop_audio_recognition():
    result = stop_recognition()
    return result

# @app.route('/send_text', methods=['POST'])
# def send_text():
#     # Get the text from the AJAX request
#     received_data = request.form
#     text_to_send = received_data.get('text', default_text_to_send)

#     # Send the text back to the frontend without processing
#     return jsonify({'processed_text': text_to_send})

# @app.route('/send_recognized_text', methods=['POST'])
# def send_text():
#     # Get the text from the AJAX request
#     received_data = request.form
#     text_to_send = received_data.get('text',audio_text)

#     # Send the text back to the frontend without processing
#     return jsonify({'processed_text': text_to_send})

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
