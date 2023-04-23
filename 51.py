import os
import re
import pandas as pd
import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import matplotlib.pyplot as plt
from transformers import DistilBertTokenizerFast, TFDistilBertForSequenceClassification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import tensorflow as tf

# Initialization
firebase_credentials_path = 'pechack-4826f-firebase-adminsdk-g4c7l-30abaa67e4.json'
sentiment140_dataset_path = 'training.1600000.processed.noemoticon.csv'
tokenizer_path = 'tokenizer'
model_path = 'sentiment_model'

def initialize_firebase():
    cred = credentials.Certificate(firebase_credentials_path)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://pechack-4826f-default-rtdb.firebaseio.com'
    })

def get_feedback_from_firebase():
    feedback_ref = db.reference('feedback')
    feedback_data = feedback_ref.get()
    return feedback_data

def clean_tweet(tweet):
    tweet = re.sub(r'http\S+|www\S+|https\S+', '', tweet, flags=re.MULTILINE)
    tweet = re.sub(r'\@\w+|\#', '', tweet)
    tweet = tweet.lower()
    return tweet


def preprocess_sentiment140_dataset(file_path):
    data = pd.read_csv(file_path, encoding='latin1', header=None)
    data = data[[0, 5]]
    data.columns = ['sentiment', 'text']
    data['sentiment'] = data['sentiment'].replace(4, 1)
    data['text'] = data['text'].apply(clean_tweet)
    return data


def train_sentiment_model(data, model_output_path, tokenizer_output_path):
    tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')
    model = TFDistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased', num_labels=2)

    X = data['text'].to_list()
    y = data['sentiment'].to_list()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    train_encodings = tokenizer(X_train, truncation=True, padding=True)
    test_encodings = tokenizer(X_test, truncation=True, padding=True)

    train_dataset = tf.data.Dataset.from_tensor_slices((
        dict(train_encodings),
        y_train
    )).shuffle(1000).batch(16)

    test_dataset = tf.data.Dataset.from_tensor_slices((
        dict(test_encodings),
        y_test
    )).batch(16)

    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=5e-5),
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    history = model.fit(train_dataset, epochs=3, validation_data=test_dataset)

    model.save_pretrained(model_output_path)
    tokenizer.save_pretrained(tokenizer_output_path)

    return model, tokenizer


def analyze_feedback(feedback_data, model, tokenizer):
    feedback_texts = [clean_tweet(fb) for fb in feedback_data.values()]
    input_encodings = tokenizer(feedback_texts, truncation=True, padding=True)
    input_data = tf.data.Dataset.from_tensor_slices(dict(input_encodings)).batch(16)

    predictions = model.predict(input_data)
    sentiment_scores = np.argmax(predictions.logits, axis=-1)
    return sentiment_scores


def visualize_sentiment_scores(sentiment_scores):
    positive_count = np.sum(sentiment_scores)
    negative_count = len(sentiment_scores) - positive_count
    plt.bar(['Positive', 'Negative'], [positive_count, negative_count])
    plt.title('Real-Time Feedback Sentiment Analysis')
    plt.xlabel('Sentiment')
    plt.ylabel('Count')
    plt.show()
def main():
    initialize_firebase()
# Preprocess and train the sentiment model
    sentiment_data = preprocess_sentiment140_dataset(sentiment140_dataset_path)
    model, tokenizer = train_sentiment_model(sentiment_data, model_path, tokenizer_path)

# Get real-time feedback from Firebase
    feedback_data = get_feedback_from_firebase()

    # Analyze feedback
    sentiment_scores = analyze_feedback(feedback_data, model, tokenizer)

    # Visualize sentiment scores
    visualize_sentiment_scores(sentiment_scores)
if __name__ == '__main__':
    main()