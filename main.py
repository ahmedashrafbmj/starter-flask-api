import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report

import joblib

from string import punctuation
import re
import numpy as np # linear algebra
import pandas as pd 


nRowsRead = 1000 # specify 'None' if want to read whole file
path = r"F:\ChatBot\MentalHealth\Mental_Health_FAQ.csv"
data = pd.read_csv(path, delimiter=',', nrows = nRowsRead)
data.dataframeName = 'Mental_Health_FAQ.csv'
nRow, nCol = data.shape
print(f'There are {nRow} rows and {nCol} columns') 
# Preprocess the data
data['Questions'] = data['Questions'].str.lower()
# Remove unnecessary characters
data['Questions'] = data['Questions'].str.replace('[^\w\s]', '')
# Handle missing values if any
data.dropna(inplace=True)
# Exploratory Data Analysis
intent_counts = data['Questions'].value_counts()
# Visualize intent distribution
fig = px.bar(x=intent_counts.index, y=intent_counts.values, labels={'x': 'Intents', 'y': 'Count'})
# fig.show()

data['Intent'] = data['Questions']
questions_response_counts = data.groupby('Intent').size().reset_index(name='Count')
# Calculate average number of questions per intent
avg_questions = data.groupby('Intent').size().mean()

# Visualize average pattern count per intent
fig = px.bar(x=questions_response_counts['Intent'], y=questions_response_counts['Count'],
             labels={'x': 'Intents', 'y': 'Average Questions Count'})
# fig.show()

# Intent Prediction Model
# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(data['Questions'], data['Intent'], test_size=0.2, random_state=42)
# Vectorize the text data
vectorizer = TfidfVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train the model
model = LinearSVC()
model.fit(X_train_vec, y_train)
joblib.dump(model, 'mental_health_intent_model.pkl')

# Save the vectorizer as well
joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')

print("Model and vectorizer saved successfully.")
# Evaluate the model
y_pred = model.predict(X_test_vec)
report = classification_report(y_test, y_pred)
print(report)

# Visualize model performance
metrics = ['precision', 'recall', 'f1-score', 'support']
scores = classification_report(y_test, y_pred, output_dict=True)['weighted avg']

fig = px.bar(x=metrics, y=[scores[metric] for metric in metrics], labels={'x': 'Metrics', 'y': 'Score'})
# fig.show()
# Prediction Model Deployment

# Example chatbot implementation
print("Welcome to the Mental Health FAQ Chatbot!")
print("Ask a question or enter 'quit' to exit.")

while True:
    user_input = input("User: ")
    
    if user_input.lower() == 'quit':
        print("Chatbot: Goodbye!")
        break
    # Vectorize user input
    user_input_vec = vectorizer.transform([user_input.lower()])
    # Predict the intent
    predicted_intent = model.predict(user_input_vec)[0]
    # Implement response generation mechanism based on predicted intent
    response = data[data['Questions'] == predicted_intent]['Answers'].values[0] if predicted_intent in data['Questions'].values else "I'm sorry, I don't have a response for that question."
    
    print("Chatbot: " + response)