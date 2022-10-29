import flask

import db
import paths

class Endpoints:
    db: db.DB

    def __init__(self, app: flask.Flask, database: db.DB):
        self.db = database

        app.add_url_rule(paths.ENTRIES, view_func=self.list_entries, methods=["GET"])
        app.add_url_rule(paths.GET_ENTRY, view_func=self.get_entry, methods=["GET"])

    def list_entries(self):
        # TODO: populate from databaase

        return flask.jsonify([{
            "id": "203fc6a0-9587-41a4-9862-e1b72039b98b",
            "name": "Birmingham Duck Pond",
            "location": {
                "lat": -1.2345,
                "long": 33.4567
            },
            "imageURL": "https://example.com/image.png"
        }, {
            "id": "b140e048-ea2c-4827-b670-ef41ba48c56d",
            "name": "Northwich Duck Pond",
            "location": {
                "lat": -3.2345,
                "long": 25.4567
            },
            "imageURL": "https://example.com/image.png"
        }])

    def get_entry(self, id: str):
        return flask.jsonify({
            "id": id,
            "TODO": "TODO"
        })