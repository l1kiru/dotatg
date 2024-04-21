host = "127.0.0.1"
user = "postgres"
password = "admin"
db_name = "dotabase"
port = 5432 

class DBsettings():
    def __init__(self,host,user,password,db_name,port):
        self.host = host
        self.user = user
        self.password = password
        self.db_name = db_name
        self.port = port

    def DatabaseUrl(self):
        return f"postgresql+psycopg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"