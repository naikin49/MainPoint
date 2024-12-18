import pyodbc
import pandas as pd
from dotenv import load_dotenv
import os

class DB:

    def __init__(self):
        load_dotenv(os.path.dirname(os.path.abspath(__file__)) + '\\config.env')

        self.Server_name = os.getenv("Server_name")
        self.DB_name = os.getenv("DB_Name")

        connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.Server_name};DATABASE={self.DB_name};Trusted_Connection=yes;'
        self.conn = pyodbc.connect(connection_string)
        self.cursor = self.conn.cursor()
   
    def Add(self, file_name, file_path, is_poss, score, full_text, main_text):
        with open(file_path+file_name, "rb") as file:
            file_data = file.read()

        try:
            query = "exec Add ?, ?, ?, ?, ?"
            self.cursor.execute(query, (pyodbc.Binary(file_data), is_poss, score, full_text, main_text))
            self.conn.commit()
            return 0
        except:
            return 1

#db = DB()
#s = db.User_name_from_Telegram('123123')
#print(s)
#print(10*'-')
#print(s['user_name'][0])



