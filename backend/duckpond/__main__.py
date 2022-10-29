import flask

__version__ = '0.1.0'


def main():
    app = flask.Flask(__name__)
    app.add_url_rule("/", view_func=index)

    app.run(port=8080, debug=True, host="127.0.0.1")


def index():
    return "<h2>Hello world!</h2>"


if __name__ == "__main__":
    main()