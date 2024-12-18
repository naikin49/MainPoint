from transformers import pipeline
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def analyze_text_with_bert(text, bert_classifier):
    """
    Анализ текста с использованием модели BERT.
    """
    result = bert_classifier(text)
    return result
