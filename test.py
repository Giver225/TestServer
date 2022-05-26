import os
import threading
from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
from pyngrok import ngrok
import sqlite3
import json

db = sqlite3.connect('users.db', check_same_thread=False)
c = db.cursor()

os.environ["FLASK_ENV"] = "development"
app = Flask(__name__)
port = 5000

# Setting an auth token allows us to open multiple tunnels at the same time
ngrok.set_auth_token("29hDO6uvjslcvseC6GRyizTET6e_3UqK2AHf8YktmxiD78XtM")
# Open a ngrok tunnel to the HTTP server
public_url = ngrok.connect(port).public_url
print(" * ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, port))
# Update any base URLs to use the public ngrok URL
app.config["BASE_URL"] = public_url

api = Api()

accounts = ["login", "password"]

parser = reqparse.RequestParser()
parser.add_argument("password", type=str)

class Main(Resource):
    def get(self, login):
        if login == "0":
            c.execute("SELECT * FROM accounts")
            result = c.fetchall()
            for i in range(len(result)):
                result[i] = dict(zip(accounts, result[i]))
            return result
        else:
            try:
                c.execute(f"SELECT * FROM accounts WHERE login = '{login}'")
                result = c.fetchall()
                result = list(result[0])
                result = dict(zip(accounts, result))
                return result
            except:
                return 'Incorrect Key'

    def delete(self, login):
        try:
            c.execute(f"DELETE FROM accounts WHERE login = '{login}'")
            db.commit()
            return self.get("0")
        except:
            return 'Incorrect key'

    def post(self, login):
        all_data = self.get("0")
        for i in all_data:
            if i["login"] == login:
                return 'This login already exists'
        args = parser.parse_args()
        c.execute(f"INSERT INTO accounts VALUES ('{login}', '{args['password']}')")
        db.commit()
        return self.get("0")

    def put(self, login):
        self.delete(login)
        args = parser.parse_args()
        c.execute(f"INSERT INTO accounts VALUES ('{login}', '{args['password']}')")
        db.commit()
        return self.get("0")


# Define Flask routes
@app.route("/")
def index():
    c.execute("SELECT * FROM accounts")
    return c.fetchone()


api.add_resource(Main, "/api/accounts/<string:login>")
api.init_app(app)

# Start the Flask server in a new thread
threading.Thread(target=app.run, kwargs={"use_reloader": False}).start()
