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
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users (username VARCHAR(100), nome VARCHAR(100), cognome VARCHAR(100), password VARCHAR(100), PRIMARY KEY (username))")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS companies (name VARCHAR(100), market VARCHAR(100), total_investment DOUBLE, funding_rounds INT, \
                            founded_at DATE, first_funding_at DATE, last_funding_at DATE, PRIMARY KEY (name))")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS interested (username VARCHAR(100), name VARCHAR(100), FOREIGN KEY (username) REFERENCES users(username), \
                            FOREIGN KEY (name) REFERENCES companies(name))")

    def read_user(self, sel, attr, val):
        self.cursor.execute("SELECT {sel} FROM users WHERE {attr} = '%s'".format(sel=sel, attr=attr) % (val))
        return self.cursor.fetchall()
    
    def insert_user(self, username, nome, cognome, password):
        self.cursor.execute("INSERT INTO users (username, nome, cognome, password) VALUES (%s, %s, %s, %s)", (username, nome, cognome, password))
        self.conn.commit()

    def update_user(self, actualusername, username, nome, cognome, password):
        self.cursor.execute("UPDATE users SET username = %s, nome = %s, cognome = %s, password = %s WHERE username = %s", (username, nome, cognome, password, actualusername))
        self.conn.commit()

    def read_company(self, sel, attr, val):
        self.cursor.execute("SELECT {sel} FROM company WHERE {attr} = '%s'".format(sel=sel, attr=attr) % (val))
        return self.cursor.fetchall()
    
    def insert_company(self, name, market, total_investment, funding_rounds, founded_at, first_funding_at, last_funding_at):
        self.cursor.execute("INSERT INTO companies (name, market, total_investment, funding_rounds, founded_at, first_funding_at, last_funding_at) \
                            VALUES (%s, %s, %s, %s, %s, %s, %s)", (name, market, total_investment, funding_rounds, founded_at, first_funding_at, last_funding_at))
        self.conn.commit()

    def delete_company(self, name):
        self.cursor.execute("DELETE FROM companies WHERE name = '%s'".format(name))
        self.conn.commit()

    def close(self):
        self.conn.close()