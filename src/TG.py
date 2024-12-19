import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from pydub import AudioSegment
from Audio_processing import transcribe_audio
from nlp_ask import ask_ollama
from text_analysis import analyze_text_with_bert
from transformers import pipeline
from DB import DB
import pyodbc

class Telegram:
    def __init__(self):
        self.db_flag = False
        try:
            self.db = DB()
            self.db_flag = True
        except ValueError:
            print('Ошибка работы с sql: ' + str(ValueError))
        except pyodbc.Error as e:
            print('Не удалось подключиться к SQL серверу')
        except:
            print('Ошибка в БД')

        load_dotenv(os.path.dirname(os.path.abspath(__file__)) + '\\config.env')
        Telegram_Token = os.getenv("Telegram_Token")

        self.VOICE_DIR = os.path.dirname(os.path.abspath(__file__))  + '\\VOICE'

        if not os.path.exists(self.VOICE_DIR ):
            os.makedirs(self.VOICE_DIR )        
            
        self.bert_classifier = pipeline("sentiment-analysis")


        application = ApplicationBuilder().token(Telegram_Token).build()        

        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(MessageHandler(filters.VOICE, self.handle_voice))

        application.run_polling()



    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Добрый день! Отправьте мне голосовое сообщение, я его обработаю.")

    async def handle_voice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        telegram_id = str(update.effective_user.id)
        """Обработчик голосовых сообщений"""
        voice = update.message.voice

        file = await context.bot.get_file(voice.file_id)
        ogg_path = os.path.join(self.VOICE_DIR, f"voice_{update.message.message_id}.ogg")
        wav_path = os.path.join(self.VOICE_DIR, f"voice_{update.message.message_id}.wav")
        await file.download_to_drive(ogg_path)

        audio = AudioSegment.from_file(ogg_path, format="ogg")
        audio.export(wav_path, format="wav")
        audio_ans = transcribe_audio(wav_path)
        nlp_ans = ask_ollama(audio_ans)
        bert_ans = analyze_text_with_bert(nlp_ans, self.bert_classifier)

        db_ans =''
        if self.db_flag:
            try:
                db_ans = self.db.Record_Add(f"voice_{update.message.message_id}.wav", self.VOICE_DIR+'\\', bert_ans[0]['label'] == 'POSITIVE', bert_ans[0]['score'], audio_ans, nlp_ans, telegram_id)
            except:
                db_ans = 'Не удалось связаться с БД.'
        else:
            db_ans ='Не удалось подключиться к SQL серверу'

        try:
            if os.path.exists(ogg_path):
                os.remove(ogg_path)
        except:
            pass
        try:
            if os.path.exists(wav_path):
                os.remove(wav_path)
        except:
            pass

        await update.message.reply_text('Речь: ' + audio_ans + ' \n\nОтвет от блока nlp: ' + nlp_ans + ' \n\nОтвет от Bert: ' + bert_ans[0]['label'] + ' score= ' + str(bert_ans[0]['score']) + '\n\nОтвет от БД: ' + db_ans)
        




        