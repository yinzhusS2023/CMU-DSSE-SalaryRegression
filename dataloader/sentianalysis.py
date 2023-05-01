from textblob import TextBlob


class SentimentAnalyzer:
    def __init__(self, text: str):
        self.text = text

    def get_sentiment(self):
        blob = TextBlob(self.text)
        return blob.sentiment.polarity
