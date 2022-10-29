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

@dataclass
class User:
    id: str
    username: str
    password_salt: str
    password_hash: str

    def validate(self, only_populated_fields=False) -> Tuple[bool, str]:
        if (self.username == "" or self.username is None) and not only_populated_fields:
            return False, "name cannot be empty"

        return True, ""
    
    def as_dict(self) -> Dict:
        res = {}

        res["id"] = self.id
        res["username"] = self.username
        res["password_salt"] = self.password_salt
        res["password_hash"] = self.password_hash

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
        cursor.execute('''
          CREATE TABLE IF NOT EXISTS users
          ([ID] INTEGER PRIMARY KEY, [username] TEXT, [password_salt] TEXT, [password_hash] TEXT)
          ''')
        cursor.execute('''
          CREATE TABLE IF NOT EXISTS places_visited
          ([ID] INTEGER PRIMARY KEY, [userID] INTEGER, [entryID] INTEGER)
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
        entry = Entry(result[0], result[1], result[2], result[3], result[4], result[5])

        return entry

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
    
    def getUser(self, ID):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE ID = ?', ID)

        result = cursor.fetchall()
        user = User(result[0], result[1], result[2], result[3])

        return user

    def addUser(self, User):
        username = User.name
        password_salt = User.password_salt
        password_hash = User.password_hash
        insertArray = [username, password_salt, password_hash]

        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO user (username, password_salt, password_hash) VALUES (?, ?, ?);', insertArray)
        cursor.commit()

    def deleteUser(self, ID):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM users WHERE ID = ?', ID)
        cursor.commit()

    def getUserLocations(self, ID):
        array_locations = []
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM places_visited WHERE userID = ?', ID)

        result = cursor.fetchall()

        for x in result:
            array_locations.append(x[2])
        return array_locations
        #should return a list of IDs of places the user has visited