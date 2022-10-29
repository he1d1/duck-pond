import flask

import db

class Endpoints:
    db: db.DB

    def __init__(self, app: flask.Flask, database: db.DB):
        self.db = database

        app.add_url_rule("/", view_func=self.index)

    def index(self):
        return "<h2>Hello world</h2>"