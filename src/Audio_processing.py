import speech_recognition as sr

def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    
    with sr.AudioFile(file_path) as source:
        audio_data = recognizer.record(source)
    
    try:
        text = recognizer.recognize_google(audio_data, language="ru-RU")  
        return text
    except sr.UnknownValueError:
        return "Не удалось распознать речь."
    except sr.RequestError as e:
        return f"Ошибка сервиса распознавания речи: {e}"
