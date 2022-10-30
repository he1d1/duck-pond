from typing import *
import uuid
import flask

import db
import paths


class Endpoints:
    db: db.DB

    def __init__(self, app: flask.Flask, database: db.DB):
        self.db = database

        app.add_url_rule(paths.ENTRIES, view_func=self.list_entries, methods=["GET"])
        app.add_url_rule(paths.GET_ENTRY, view_func=self.get_entry, methods=["GET"])
        app.add_url_rule(
            paths.UPDATE_ENTRY, view_func=self.update_entry, methods=["PATCH"]
        )
        app.add_url_rule(
            paths.CREATE_ENTRY, view_func=self.create_entry, methods=["POST"]
        )

    def list_entries(self):
        entries = self.db.getAllEntries()

        for i in range(len(entries)):
            entries[i] = entries[i].as_dict()

        return flask.jsonify(entries)

    def get_entry(self, entry_id: str):
        entry = self.get_entry(entry_id)
        return flask.jsonify(entry.as_dict())

    def _get_entry_from_request(self) -> Union[Tuple[str, int], db.Entry]:
        body = flask.request.get_json()
        if body is None:
            return flask.abort(400, "no JSON body")

        coordinates = body.get("location", None)
        if coordinates is None:
            return flask.abort(400, "missing location")

        try:
            new_entry = db.Entry(
                uuid.uuid4(),
                body.get("name"),
                float(coordinates.get("lat")),
                float(coordinates.get("long")),
                0,
                body.get("imageURL"),
            )
        except ValueError:
            return flask.abort(400, "invalid coordinate format")

        validation_result, error_text = new_entry.validate()

        if not validation_result:
            return flask.abort(400, error_text)
        
        return new_entry

    def update_entry(self):
        return "", 204

    def create_entry(self):
        res = self._get_entry_from_request()

        if type(res) != db.Entry:
            return res

        new_entry = res

        self.db.addEntry(new_entry)

        return flask.jsonify({"id": new_entry.id})
