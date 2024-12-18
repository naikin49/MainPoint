import pandas as pd
import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from ldap3 import Server, Connection, ALL, NTLM
from pydub import AudioSegment
from Audio_processing import transcribe_audio
from nlp_ask import ask_ollama
from text_analysis import analyze_text_with_bert
from transformers import pipeline

class Telegram:
    def __init__(self):
        load_dotenv(os.path.dirname(os.path.abspath(__file__)) + '\\config.env')
        Telegram_Token = os.getenv("Telegram_Token")

        self.VOICE_DIR = 'C:\\Users\\Nail\\Desktop\\Telegram bot\\Second_bot\\VOICE'
        self.bert_classifier = pipeline("sentiment-analysis")


        application = ApplicationBuilder().token(Telegram_Token).build()        

        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(MessageHandler(filters.VOICE, self.handle_voice))

        application.run_polling()



    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Добрый день! Отправьте мне голосовое сообщение, я его обработаю.")

    async def handle_voice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик голосовых сообщений"""
        voice = update.message.voice

        # Скачивание голосового сообщения
        file = await context.bot.get_file(voice.file_id)
        ogg_path = os.path.join(self.VOICE_DIR, f"voice_{update.message.message_id}.ogg")
        wav_path = os.path.join(self.VOICE_DIR, f"voice_{update.message.message_id}.wav")
        await file.download_to_drive(ogg_path)

        # Конвертация в формат WAV
        audio = AudioSegment.from_file(ogg_path, format="ogg")
        audio.export(wav_path, format="wav")
        audio_ans = transcribe_audio(wav_path)
        nlp_ans = ask_ollama(audio_ans)
        bert_ans = analyze_text_with_bert(nlp_ans, self.bert_classifier)
        print(bert_ans)

        # Ответ пользователю
        await update.message.reply_text('audio_ans: ' + audio_ans + ' \nnlp_ans: ' + nlp_ans)
        


telegram = Telegram()
        


        