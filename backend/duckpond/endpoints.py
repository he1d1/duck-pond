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
        app.add_url_rule(paths.UPDATE_ENTRY, view_func=self.update_entry, methods=["PATCH"])
        app.add_url_rule(paths.CREATE_ENTRY, view_func=self.create_entry, methods=["POST"])

    def list_entries(self):
       # TODO: populate from databaase 

        a = db.Entry("203fc6a0-9587-41a4-9862-e1b72039b98b", "Birmingham Duck Pond", -1.2345, 33.4567, 0, None)
        b = db.Entry("b140e048-ea2c-4827-b670-ef41ba48c56d", "Northwich Duck Pond", -3.2345, 25.4567, 0, None)

        return flask.jsonify([a.as_dict(), b.as_dict()])

    def get_entry(self, entry_id: str):
        # TODO: Fetch from database

        return flask.jsonify({
            "id": entry_id,
            "TODO": "TODO"
        })

    def update_entry(self):
        return "", 204

    def create_entry(self):
        body = flask.request.get_json()
        if body is None:
            return "no JSON body", 400

        coordinates = body.get("location", None)
        if coordinates is None:
            return "missing location", 400

        new_entry = db.Entry(
            uuid.uuid4(),
            body.get("name"),
            coordinates.get("lat"),
            coordinates.get("long"),
            0,
            body.get("imageURL"))

        validation_result, error_text = new_entry.validate()

        if not validation_result:
            return flask.abort(400, error_text)

        # TODO: store in database
        # TODO: Form responses

        return flask.jsonify({
            "id": uuid.uuidv4()
        })
