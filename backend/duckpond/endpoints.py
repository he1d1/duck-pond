from re import A
from typing import *
import urllib
import uuid
import flask
from dataclasses import dataclass

import db
import paths


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

        a = Entry("203fc6a0-9587-41a4-9862-e1b72039b98b", "Birmingham Duck Pond", -1.2345, 33.4567, 0, None)
        b = Entry("b140e048-ea2c-4827-b670-ef41ba48c56d", "Northwich Duck Pond", -3.2345, 25.4567, 0, None)

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
