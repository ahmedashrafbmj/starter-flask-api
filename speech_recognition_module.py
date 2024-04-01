# speech_to_text_module.py

import vosk
import pyaudio
import time

model = vosk.Model(r"E:\Musab\Task 14 Speech to text\vosk-model-small-en-us-0.15")
recognizer = vosk.KaldiRecognizer(model, 16000)
recognized_text = ""
recognition_running = False

def callback(in_data, frame_count, time_info, status):
    global recognized_text, recognition_running

    if not recognition_running:
        return (in_data, pyaudio.paComplete)

    if status:
        print(status)
    else:
        recognizer.AcceptWaveform(in_data)
        result = recognizer.PartialResult()
        recognized_text = str(result)[17:-3]
        print(recognized_text, end='', flush=True)

    return (in_data, pyaudio.paContinue)

# start recognition
def start_recognition():
    global recognition_running
    recognition_running = True

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
        return {'status': 'Error starting recognition', 'text': recognized_text}

    print('Mic: On')

    stream.start_stream()
    print("Say something:")

    recognition_running = True

    while recognition_running:
        pass  # Continue streaming until recognition_running is False

    stream.stop_stream()
    stream.close()
    p.terminate()

    result = recognizer.FinalResult()
    print(result)
    with open('conversation.txt', 'w') as file:
        file.write(str(result))

    return {'status': 'Recognition stopped', 'text': recognized_text}

# stop recognition
def stop_recognition():
    global recognition_running
    recognition_running = False
    return {'status': 'Recognition stopped', 'text': recognized_text}

# def get_text():
#     global recognized_text
#     return {'text': recognized_text}

# def send_text(received_data):
#     # Get the text from the AJAX request
#     text_to_send = received_data.get('text', '')

#     # Send the text back to the frontend without processing
#     return {'processed_text': text_to_send}
