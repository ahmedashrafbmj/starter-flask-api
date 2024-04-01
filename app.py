from flask import Flask, render_template, jsonify, request
import vosk
import os
import pyaudio
import threading
import re
import pandas as pd

# current_directory = os.path.dirname(os.path.abspath(__file__))
# text_file_path = os.path.join(current_directory, 'conversation.txt')
# with open('Editor_content.txt') as ed_content:
#     previous_content = ed_content

# with open(text_file_path) as text_file:
#     default_text_to_send = text_file.read()
#     print(default_text_to_send)

app = Flask(__name__)

model_path = r"C:\Users\ABCD\Downloads\CK and Speech rec\CK and Speech rec\vosk-model-small-en-us-0.15"
model = vosk.Model(model_path)
recognizer = vosk.KaldiRecognizer(model, 16000)
recognized_text = ""
recognition_running = False
recognition_thread = None

def callback(in_data, frame_count, time_info, status):
    global recognized_text, recognition_running
    
    if not recognition_running:
        return (in_data, pyaudio.paComplete)
    
    if not status:
        recognizer.AcceptWaveform(in_data)
        result = recognizer.PartialResult()
        recognized_text = str(result)[17:-3]
        print(recognized_text, end='', flush=True)

    return (in_data, pyaudio.paContinue)

def speech_to_text():
    global recognition_running

    p = pyaudio.PyAudio()
    
    try:
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=16000,
                        input=True,
                        frames_per_buffer=4000,
                        stream_callback=callback)
    except IOError as e:
        print(f'Error opening stream: {e}')
    except Exception as e:
        print(f'Error: {e}')

    print('Mic: On')
    
    stream.start_stream()
    print("Say something:")

    while recognition_running:
        pass

    stream.stop_stream()
    stream.close()
    p.terminate()

    result = recognizer.FinalResult()
    db = {"Data": [result]}
    df = pd.DataFrame(db)
    df.to_csv('Data.csv', 'a', index=False)
    with open('conversation.txt', 'w') as file:
        file.write(str(result))

def start_recognition_thread():
    global recognition_thread
    recognition_thread = threading.Thread(target=speech_to_text)
    recognition_thread.start()

@app.route('/')
def index():
    return render_template('index v1.3.html')

@app.route('/save_content', methods=['POST'])
def save_content():
    global previous_content

    data = request.get_json()
    new_content = data.get('content')

    # Check if the content has changed
    if new_content != previous_content:
        # Specify the file path
        file_path = 'Editor_content.txt'

        # Open the file in append mode and write the content
        with open(file_path, 'a') as file:
            file.write(new_content)

        # Update the previous_content variable
        previous_content = new_content

        return jsonify({'message': 'Content saved successfully'})
    else:
        return jsonify({'message': 'Content not changed'})

@app.route('/stop_recognition', methods=['GET'])
def stop_recognition():
    global recognition_running, recognition_thread
    recognition_running = False

    if recognition_thread and recognition_thread.is_alive():
        recognition_thread.join()

    return jsonify({'status': 'Recognition stopped', 'text': recognized_text})

@app.route('/start_recognition', methods=['POST'])
def start_recognition():
    global recognized_text, recognition_running, recognition_thread

    if recognition_thread and recognition_thread.is_alive():
        return jsonify({'status': 'Recognition already started'})

    recognized_text = ""
    recognition_running = True
    start_recognition_thread()

    return jsonify({'status': 'Recognition started'})

@app.route('/get_text', methods=['GET'])
def get_text():
    global recognized_text
    return jsonify({'text': recognized_text})

@app.route('/audio_send_text', methods=['POST'])
def send_recognized_text(): 
    global recognized_text
    return jsonify({'processed_text': recognized_text})



if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
