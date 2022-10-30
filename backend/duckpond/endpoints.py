from curses import raw
import os
from typing import *
import uuid
import flask
import hashlib

import db
import paths


def _hash_password(password: str, salt: Optional[str] = None) -> Tuple[str, str]:
    if salt is None:
        salt = os.urandom(32).hex()

    hasher = hashlib.sha256()
    hasher.update((password + salt).encode())

    return hasher.hexdigest(), salt


class Endpoints:
    db: db.DB

    def __init__(self, app: flask.Flask, database: db.DB):
        self.db = database

        app.add_url_rule(paths.ENTRIES, view_func=self.list_entries, methods=["GET"])
        app.add_url_rule(paths.GET_ENTRY, view_func=self.get_entry, methods=["GET"])
        app.add_url_rule(
            paths.UPDATE_ENTRY, view_func=self.update_entry, methods=["PUT"]
        )
        app.add_url_rule(
            paths.DELETE_ENTRY, view_func=self.delete_entry, methods=["DELETE"]
        )
        app.add_url_rule(
            paths.CREATE_ENTRY, view_func=self.create_entry, methods=["POST"]
        )

        app.add_url_rule(
            paths.CREATE_USER, view_func=self.create_user, methods=["POST"]
        )
        app.add_url_rule(
            paths.DELETE_USER, view_func=self.delete_user, methods=["DELETE"]
        )
        app.add_url_rule(
            paths.LOGIN, view_func=self.login, methods=["POST"]
        )

    def list_entries(self):
        entries = self.db.getAllEntries()

        for i in range(len(entries)):
            entries[i] = entries[i].as_dict()

        return flask.jsonify(entries)

    def get_entry(self, entry_id: str):
        entry = self.db.getEntry(entry_id)
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
                str(uuid.uuid4()),
                body.get("name"),
                float(coordinates.get("lat")),
                float(coordinates.get("long")),
                body.get("votes", 0),
                body.get("imageURL"),
            )
        except ValueError:
            return flask.abort(400, "invalid coordinate format")
        
        validation_result, error_text = new_entry.validate()

        if not validation_result:
            return flask.abort(400, error_text)
 
        return new_entry

    def update_entry(self, entry_id: str):
        res = self._get_entry_from_request()

        if type(res) != db.Entry:
            return res

        entry = res
        entry.id = entry_id

        self.db.updateEntry(entry)

        return "", 204        


    def create_entry(self):
        res = self._get_entry_from_request()

        if type(res) != db.Entry:
            return flask.abot(res[1], res[0])

        new_entry = res

        self.db.addEntry(new_entry)

        return flask.jsonify({"id": new_entry.id})

    def delete_entry(self, entry_id: str):
        self.db.deleteEntry(entry_id)
        return "", 204

    def create_user(self):
        body = flask.request.get_json()
        if body is None:
            return flask.abort(400, "no JSON body")

        raw_password = body.get("password")
        if raw_password is None:
            return flask.abort(400, "missing password")

        password_hash, salt = _hash_password(raw_password)

        new_user = db.User(
            str(uuid.uuid4()),
            body.get("username"),
            salt,
            password_hash,
        )

        self.db.addUser(new_user)

        return flask.jsonify({
            "id": new_user.id,
        })

    def delete_user(self, user_id: str):
        self.db.deleteUser(user_id)
        return "", 204

    def login(self):
        body = flask.request.get_json()
        if body is None:
            return flask.abort(400, "no JSON body")

        username = body.get("username")
        password = body.get("password")

        if username is None or password is None:
            return flask.abort(400, "missing username or password")

        user = self.db.getUserByUsername(username)
        
        hashed_password, _ = _hash_password(password, salt=user.password_salt)

        if user.password_hash != hashed_password:
            return flask.abort(401, "invalid password")

        # TODO: issue session

        return
