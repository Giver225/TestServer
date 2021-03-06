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

accounts = ["login", "password", "name", "status", "phone", "male", "date_of_birth", "email"]
entry_list = ["doctor", "patient", "time"]
parser = reqparse.RequestParser()
parser.add_argument("login", type=str)
parser.add_argument("password", type=str)
parser.add_argument("name", type=str)
parser.add_argument("status", type=str)
parser.add_argument("phone", type=str)
parser.add_argument("male", type=str)
parser.add_argument("date_of_birth", type=str)
parser.add_argument("email", type=str)


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
        args = parser.parse_args()
        for i in all_data:
            if i["login"] == args['login']:
                return 'This login already exists'

        c.execute(f"INSERT INTO accounts VALUES ('{args['login']}', '{args['password']}', '{args['name']}', '{args['status']}', '{args['phone']}', '{args['male']}', '{args['date_of_birth']}', '{args['email']}')")
        db.commit()
        return self.get(args['login'])

    def put(self, login):
        self.delete(login)
        args = parser.parse_args()
        c.execute(f"INSERT INTO accounts VALUES ('{args['login']}', '{args['password']}', '{args['name']}', '{args['status']}', '{args['phone']}', '{args['male']}', '{args['date_of_birth']}', '{args['email']}')")
        db.commit()
        return self.get(args['login'])


class Entry(Resource):
    def get(self, login):
        if login == "0":
            c.execute("SELECT * FROM entry")
            result = c.fetchall()
            for i in range(len(result)):
                result[i] = dict(zip(entry_list, result[i]))
            return result
        else:
            try:
                c.execute(f"SELECT * FROM entry WHERE patient = '{login}' OR doctor = '{login}'")
                result = c.fetchall()
                if len(result) > 1:
                    for i in range(len(result)):
                        result[i] = dict(zip(entry_list, result[i]))
                    return result
                result = list(result[0])
                result = dict(zip(entry_list, result))
                return result
            except:
                return 'Incorrect Key'

    def delete(self, login):
        try:
            c.execute(f"DELETE FROM entry WHERE patient = '{login}'")
            db.commit()
            return self.get("0")
        except:
            return 'Incorrect key'

    def post(self, login):
        parser = reqparse.RequestParser()
        parser.add_argument("doctor", type=str)
        parser.add_argument("patient", type=str)
        parser.add_argument("time", type=str)
        args = parser.parse_args()
        c.execute(f"INSERT INTO entry VALUES ('{args['doctor']}', '{args['patient']}', '{args['time']}')")
        db.commit()
        return self.get(args['patient'])

    def put(self, login):
        args = parser.parse_args()
        c.execute(f"INSERT INTO entry VALUES ('{args['doctor']}', '{args['patient']}', '{args['time']}')")
        db.commit()
        return self.get(args['patient'])


# Define Flask routes
@app.route("/")
def index():
    c.execute("SELECT * FROM accounts")
    return c.fetchone()


api.add_resource(Main, "/api/accounts/<string:login>")
api.add_resource(Entry, "/api/entry/<string:login>")
api.init_app(app)

# Start the Flask server in a new thread
threading.Thread(target=app.run, kwargs={"use_reloader": False}).start()
