from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

# Load the trained model and vectorizer
loaded_model = joblib.load('mental_health_intent_model.pkl')
loaded_vectorizer = joblib.load('tfidf_vectorizer.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    # Get the text data from the request
    text_data = request.json['text']
    
    # Vectorize the text data
    text_data_vec = loaded_vectorizer.transform([text_data])
    
    # Make predictions using the loaded model
    prediction = loaded_model.predict(text_data_vec)
    
    # Return the prediction as a response
    return jsonify({'prediction': prediction[0]})

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
import joblib

app = Flask(__name__)

# Load and preprocess data
data = pd.read_csv("Mental_Health_FAQ.csv")
data['Questions'] = data['Questions'].str.lower()
data['Questions'] = data['Questions'].str.replace('[^\w\s]', '')
data.dropna(inplace=True)

# Train model and save
X_train, X_test, y_train, y_test = train_test_split(data['Questions'], data['Intent'], test_size=0.2, random_state=42)
vectorizer = TfidfVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
model = LinearSVC()
model.fit(X_train_vec, y_train)
joblib.dump(model, 'mental_health_intent_model.pkl')
joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')


# Predict intent
@app.route('/predict', methods=['POST'])
def predict_intent():
    user_input = request.json['question']
    user_input_vec = vectorizer.transform([user_input.lower()])
    predicted_intent = model.predict(user_input_vec)[0]
    response = data[data['Questions'] == predicted_intent]['Answers'].values[0] if predicted_intent in data['Questions'].values else "I'm sorry, I don't have a response for that question."
    return jsonify({'intent': predicted_intent, 'response': response})


if __name__ == '__main__':
    app.run(debug=True)