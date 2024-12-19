import subprocess
import os

def run_ollama_and_script():
    try:
        # Запускаем Ollama через командную строку
        print("Запускаем Ollama...")
        ollama_command = ["ollama", "run", "llama3.1:8B"]
        ollama_process = subprocess.Popen(ollama_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Запускаем main.py в той же директории, что и скрипт
        script_dir = os.path.dirname(os.path.abspath(__file__))
        main_script_path = os.path.join(script_dir, "main.py")

        if not os.path.exists(main_script_path):
            print(f"Файл main.py не найден в директории: {script_dir}")
            return

        print("Запускаем main.py...")
        subprocess.run(["python", main_script_path])

        # Ждем завершения процесса Ollama
        stdout, stderr = ollama_process.communicate()
        if ollama_process.returncode == 0:
            print("Ollama завершен успешно:")
            print(stdout.decode())
        else:
            print("Ошибка при запуске Ollama:")
            print(stderr.decode())

    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    run_ollama_and_script()
