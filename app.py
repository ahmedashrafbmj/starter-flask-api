
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS from flask_cors
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
import joblib

app = Flask(__name__)
CORS(app)  # Add CORS support to your Flask app

# Load and preprocess data
data = pd.read_csv("Mental_Health_FAQ.csv", encoding='latin1')
data['Questions'] = data['Questions'].str.lower()
data['Questions'] = data['Questions'].str.replace('[^\w\s]', '')
data.dropna(inplace=True)

# Train model and save
vectorizer = TfidfVectorizer()
X_train_vec = vectorizer.fit_transform(data['Questions'])
model = LinearSVC()
model.fit(X_train_vec, data['Answers'])
joblib.dump(model, 'mental_health_intent_model.pkl')
joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')


# Predict intent
@app.route('/predict', methods=['POST'])
def predict_intent():
    user_input = request.json['question']
    user_input_vec = vectorizer.transform([user_input.lower()])
    predicted_intent = model.predict(user_input_vec)[0]
    response = predicted_intent  # Return the predicted intent for now, you may modify this to return the actual answer
    return jsonify({'response': response})


if __name__ == '__main__':
    app.run(debug=True)
