import pyodbc
from dotenv import load_dotenv
import os

class DB:

    def __init__(self):
        load_dotenv(os.path.dirname(os.path.abspath(__file__)) + '\\config.env')

        self.Server_name = os.getenv("Server_name")
        self.DB_name = os.getenv("DB_Name")
        self.DB_user_name = os.getenv("DB_user_name")
        self.DB_user_password = os.getenv("DB_user_password")

        connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.Server_name};DATABASE={self.DB_name};UID={self.DB_user_name};PWD={self.DB_user_password};TrustServerCertificate=yes;'
        self.conn = pyodbc.connect(connection_string)
        self.cursor = self.conn.cursor()
   
    def Record_Add(self, file_name, file_path, is_poss, score, full_text, main_text, tg_id):
        with open(file_path+file_name, "rb") as file:
            file_data = file.read()

        try:
            query = "exec Record_Add ?, ?, ?, ?, ?, ?, ?"
            self.cursor.execute(query, (pyodbc.Binary(file_data), file_name, is_poss, score, full_text, main_text, tg_id))
            self.conn.commit()
            return 'Сообщение было сохранено в базе данных'
        except pyodbc.DatabaseError as e:
            return str(e)
        except ValueError:
            return str(ValueError)



