import sqlite3
from dataclasses import dataclass
from typing import *
import urllib

@dataclass
class Entry:
    id: str
    name: str
    location_lat: float
    location_long: float
    votes: int
    image_url: Optional[str]

    def validate(self, only_populated_fields=False) -> Tuple[bool, str]:
        if (self.name == "" or self.name is None) and not only_populated_fields:
            return False, "name cannot be empty"
        
        if self.votes < 0:
            return False, "votes cannot be negative"

        if self.image_url is not None:
            try:
                urllib.parse.urlparse(self.image_url)
            except Exception:
                return False, "invalid URL"

        if self.location_lat is None or self.location_long is None:
            return False, "missing locations"

        return True, ""

    def as_dict(self) -> Dict:
        res = {}

        res["id"] = self.id
        res["name"] = self.name
        res["location"] = {
            "lat": self.location_lat,
            "long": self.location_long,
        }
        res["votes"] = self.votes

        if self.image_url is not None:
            res["imageURL"] = self.image_url

        return res


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