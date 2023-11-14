import sqlite3


class DataBase:
    def __init__(self):
        self.connection = sqlite3.connect("./prisma/inventory.db")
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()
