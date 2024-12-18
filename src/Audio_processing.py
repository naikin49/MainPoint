import speech_recognition as sr

def transcribe_audio(file_path):
    # Создаем объект распознавания
    recognizer = sr.Recognizer()
    
    # Загружаем аудиофайл
    with sr.AudioFile(file_path) as source:
        audio_data = recognizer.record(source)
    
    # Преобразуем аудио в текст
    try:
        text = recognizer.recognize_google(audio_data, language="ru-RU")  # Укажите 'en-US' для английского
        return text
    except sr.UnknownValueError:
        return "Не удалось распознать речь."
    except sr.RequestError as e:
        return f"Ошибка сервиса распознавания речи: {e}"
