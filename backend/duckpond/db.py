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
        if self.name == "" and not only_populated_fields:
            return False, "name cannot be empty"
        
        if self.votes < 0:
            return False, "votes cannot be negative"

        if self.image_url is not None:
            try:
                urllib.parse.urlparse(self.image_url)
            except Exception:
                return False, "invalid URL"

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

    def _setup(self):
        cursor = self.conn.cursor()

        cursor.execute('''
          CREATE TABLE IF NOT EXISTS entries
          ([ID] INTEGER PRIMARY KEY, [title] TEXT, [latitude] FLOAT, [longitude] FLOAT, [votes] INTEGER, [image_url], STRING)
          ''')

        cursor.commit()

    def getAllEntries(self):
        arrayEntries = []
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM entries')

        result = cursor.fetchall()

        for x in result:
            entry = Entry(x[0], x[1], x[2], x[3], x[4], x[5])
            arrayEntries.append(entry)
        return arrayEntries

    def getEntry(self, ID):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM entries WHERE ID = ?', ID)

        result = cursor.fetchall()

        return result

    def addEntry(self, Entry):
        title = Entry.name
        latitude = Entry.location_lat
        longitude = Entry.location_long
        votes = Entry.votes
        image_url = Entry.image_url
        insertArray = [title, latitude, longitude, votes, image_url]

        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO entries (title, latitude, longitude, votes, image_url) VALUES (?, ?, ?, ?, ?);', insertArray)
        cursor.commit()

    def deleteEntry(self, ID):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM entries WHERE ID = ?', ID)
        cursor.commit()

    def updateEntry(self, Entry):
        ID = Entry.id
        title = Entry.name
        latitude = Entry.location_lat
        longitude = Entry.location_long
        votes = Entry.votes
        image_url = Entry.image_url
        updateArray = [ID, title, latitude, longitude, votes, image_url]

        cursor = self.conn.cursor()
        cursor.execute('UPDATE entries SET title = ?, latitude = ?, longitude = ?, votes = ?, image_url = ?;', updateArray)
        cursor.commit()