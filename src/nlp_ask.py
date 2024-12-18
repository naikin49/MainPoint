import requests
import json

# Базовый URL Ollama API
OLLAMA_API_URL = "http://localhost:11434"

def send_prompt_to_ollama_streaming(model_name, prompt):
    """
    Отправка запроса к Ollama и обработка потокового ответа.

    :param model_name: Название модели (например, "llama3.1")
    :param prompt: Текст запроса
    :return: Полный ответ модели
    """
    url = f"{OLLAMA_API_URL}/api/generate"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "model": model_name,
        "prompt": prompt
    }
    
    try:
        # Открываем потоковое соединение
        response = requests.post(url, json=payload, headers=headers, stream=True)
        response.raise_for_status()
        
        # Сбор полного текста ответа
        full_response = ""
        for line in response.iter_lines():
            if line:
                try:
                    # Парсим каждую строку как JSON
                    json_line = json.loads(line)
                    # Извлекаем содержимое из поля "response"
                    full_response += json_line.get("response", "")
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
        
        return full_response

    except requests.exceptions.RequestException as e:
        return f"Error while communicating with Ollama API: {e}"

def ask_ollama(prompt_in):
    model = "llama3.1"
    #system_prompt = "Ты помошник, который по сообщениям помогает узнать настроение говорящего. В ответ ты должен дать 1 - радость, 2 - злость, 3 - огорчение, 4 - нейтральность, 0 - в случае ошибки. Кроме этих чисел ты ничего говорить не должен. Вот, что отправил пользователь: "
    system_prompt = "Твоя задача помочь персоналу клиенского сервиса из введенного пользоватем текста вычленить главную мысль. Ты должен понять, что хотел сказать пользователь. КРОМЕ ГЛАВНОЙ МЫСЛИ ПОЛЬЗОВАТЕЛЯ НИЧЕГО НЕ ПИШИ. Тест пользователя: "
    prompt = system_prompt + prompt_in
    return send_prompt_to_ollama_streaming(model, prompt)

