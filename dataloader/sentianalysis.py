import nltk
from textblob import TextBlob

# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('brown')


class SentimentAnalyzer:
    def __init__(self, text: str):
        self.text = text

    def get_sentiment(self):
        blob = TextBlob(self.text)
        return blob.sentiment.polarity
