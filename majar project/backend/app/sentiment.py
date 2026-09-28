"""VADER sentiment classification."""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

_analyzer = SentimentIntensityAnalyzer()


def analyze_review(text):
    score = round(_analyzer.polarity_scores(text)["compound"], 3)
    sentiment = "Positive" if score >= 0.05 else "Negative" if score <= -0.05 else "Neutral"
    return {"sentiment": sentiment, "score": score, "polarity": score}
