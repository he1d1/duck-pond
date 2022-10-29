import flask
from flask_cors import CORS, cross_origin

import db
import endpoints


__version__ = '0.1.0'


def main():
    app = flask.Flask(__name__)

    CORS(app)

    database = db.DB("duckpond.db")
    _ = endpoints.Endpoints(app, database)

    app.run(port=8080, debug=True, host="127.0.0.1")


if __name__ == "__main__":
    main()
