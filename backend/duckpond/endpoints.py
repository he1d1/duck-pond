from re import A
from typing import *
import urllib
import uuid
import flask
from dataclasses import dataclass

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

        # TODO: validate inputs

        # TODO: store in database

        return flask.jsonify({
            "id": uuid.uuidv4()
        })
