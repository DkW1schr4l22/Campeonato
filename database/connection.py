import sqlite3

class DatabaseConnection:
    def __init__(self, path):
        self.path = path
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.path)
        return self.conn

    def get_cursor(self):
        return self.conn.cursor()

    def close(self):
        if self.conn:
            self.conn.close()