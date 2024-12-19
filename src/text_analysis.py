from transformers import pipeline


def analyze_text_with_bert(text, bert_classifier):
    """
    Анализ текста с использованием модели BERT.
    """
    result = bert_classifier(text)
    return result
