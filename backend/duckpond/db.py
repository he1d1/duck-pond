import sqlite3

class DB:
    conn: sqlite3.Connection

    def __init__(self, filename: str):
        self.conn = sqlite3.connect(filename)

    def _setup(self, filename: str):
        cursor = self.conn.cursor()

        cursor.execute('''
          CREATE TABLE IF NOT EXISTS entries
          ([ID] INTEGER PRIMARY KEY, [title] TEXT, [latitude] FLOAT, [longitude] FLOAT, [votes] INTEGER, [image_url], STRING)
          ''')

        cursor.commit()

    def getEntries(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM entries')

        myresult = cursor.fetchall()

        for x in myresult:
            print(x)

    def addEntry(self, title, latitude, longitude, votes, image_url):
        insertArray = [title, latitude, longitude, votes, image_url]
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO entries (title, latitude, longitude, votes, image_url) VALUES (?, ?, ?, ?, ?);', insertArray)
        cursor.commit()

    def deleteEntry(self, ID):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM entries WHERE ID = ?', ID)
        cursor.commit()

    def updateEntry(self, ID, title, latitude, longitude, votes, image_url):
        updateArray = [ID, title, latitude, longitude, votes, image_url]
        cursor = self.conn.cursor()
        cursor.execute('UPDATE entries SET title = ?, latitude = ?, longitude = ?, votes = ?, image_url = ?;', updateArray)
        cursor.commit()