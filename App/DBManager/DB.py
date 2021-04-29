import mysql.connector

class Database:
    def __init__(self):
        file_ini = open("App/DBManager/config.ini", "r")
        self.db_info = {}
        for line in file_ini:
            data = line.split("=")
            self.db_info[str(data[0])] = str(data[1])
        
        self.conn = mysql.connector.connect(**self.db_info)
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users (username VARCHAR(50), nome VARCHAR(50), cognome VARCHAR(50), password VARCHAR(50), PRIMARY KEY (username))")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS companies (name VARCHAR(50), market VARCHAR(50), total_investment DOUBLE, funding_rounds INT, \
                            founded_at DATE, first_funding_at DATE, last_funding_at DATE, PRIMARY KEY (name))")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS interested (username VARCHAR(50), name VARCHAR(50), FOREIGN KEY (username) REFERENCES users(username), \
                            FOREIGN KEY (name) REFERENCES companies(name))")

    def read_user(self, sel, attr, val):
        self.cursor.execute("SELECT {sel} FROM users WHERE {attr} = '%s'".format(sel=sel, attr=attr) % (val))
        return self.cursor.fetchall()
    
    def insert_user(self, username, nome, cognome, password):
        self.cursor.execute("INSERT INTO users (username, nome, cognome, password) VALUES (%s, %s, %s, %s)", (username, nome, cognome, password))
        self.conn.commit()

    def __del__(self):
        self.conn.close()