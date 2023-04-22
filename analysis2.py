import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from nltk.sentiment import SentimentIntensityAnalyzer

# Initialize the NLTK sentiment analyzer
# nltk.download('vader_lexicon')  # Download the lexicon used by the sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

SERVICE_ACCOUNT_KEY = "pechack-4826f-firebase-adminsdk-g4c7l-30abaa67e4.json"
cred = credentials.Certificate(SERVICE_ACCOUNT_KEY)
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://pechack-4826f-default-rtdb.firebaseio.com" 
})

# Get a reference to the Firebase database node that contains the feedback messages
ref = db.reference('/')

# Retrieve the data from Firebase
data = ref.get()
print(data.keys())
print(data['pechack'])
import pdb
for i in data['pechack']:
    # print(data['pechack'][i])

    # print("subject:",data['pechack'][i].get('subject'))
    # print("\n")
    fname = data['pechack'][i].get('fname')
    lname = data['pechack'][i].get('fname')
    subject = data['pechack'][i].get('subject','happy very good pleasure')
    sentiment = analyzer.polarity_scores(subject)
    print(f"Feedback Message: {subject}")
    print(f"Sentiment: {sentiment}\n")

    # for j in i.items():
        # print(j)
    # print(type(i))
        # print(j)
    # pdb.set_trace(if)
    #print(i['subject'])

# print(data)
# # Analyze the sentiment of each feedback message
# for feedback_id, feedback_data in data.items():
#     print("ok")
#     text = feedback_data.get('subject')
#     if text:
#         sentiment = analyzer.polarity_scores(text)
#         print(f"Feedback ID: {feedback_id}")
#         print(f"Feedback Message: {text}")
#         print(f"Sentiment: {sentiment}\n")