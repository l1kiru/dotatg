import os
from dotenv import load_dotenv

load_dotenv()
host = os.getenv('HOST')
user = "postgres"
password = os.getenv('PASSWORD')
db_name = os.getenv('DB_NAME')
port = os.getenv('PORT')

class DBsettings():
    def __init__(self,host,user,password,db_name,port):
        self.host = host
        self.user = user
        self.password = password
        self.db_name = db_name
        self.port = port

    def DatabaseUrl(self):
        return f"postgresql+psycopg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"