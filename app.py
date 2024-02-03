from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import requests

RASA_API_URL = 'http://localhost:5005/webhooks/rest/webhook'
app = Flask(__name__,static_url_path='/static')
CORS(app) 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        user_message = request.json['message']
        print(user_message)
        
        # Use requests.post to make the HTTP POST request
        rasa_response = requests.post(RASA_API_URL, json={'message': user_message})
        rasa_response_json = rasa_response.json()

        # Assuming rasa_response_json is a list with text as one of its elements
        bot_response = rasa_response_json[0]['text'] if rasa_response_json else 'Sorry, I don\'t understand that.'
        return jsonify({'response': bot_response})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
