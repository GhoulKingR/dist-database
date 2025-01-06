from flask import Flask

app = Flask(__name__)
# This one will probably be a client-side web app

if __name__ == "__main__":
    app.run(port=8082, debug=True)