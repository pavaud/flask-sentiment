from flask import Flask, request
from pydantic import BaseModel
from flask_pydantic import validate
from werkzeug.exceptions import Unauthorized
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import random

class User(BaseModel):
    name:str

app = Flask(__name__)

# USER FUNCTIONS
def get_user(username):
    """ get infos for the given username """

    df = pd.read_csv('credentials.csv')
    user = df[df['username'] == username]

    if user.empty:
        return None
    else:
        return user.values.tolist()[0]


def is_valid_user(username,password):
    """ check user authentication """

    df = pd.read_csv('credentials.csv')
    user = df[(df['username'] == username) & (df['password'] == int(password))]

    return not user.empty


# ENDPOINTS
@app.route("/status")
def status():
    return str(1)


@app.route("/welcome")
@validate()
def intro(query: User):
    if get_user(query.name) is not None:
        greet = "Hello {}, welcome to the sentiment analysis API".format(query.name)
        return greet
    else:
        raise Unauthorized("The user {} is not in the database".format(query.name))


@app.route("/permissions",methods=["GET"])
@validate()
def permissions():
    username = request.headers.get("username")
    password = request.headers.get("password")

    if is_valid_user(username,password):
        user = get_user(username)
        return f"User {user[0]} has the following rights: v1={user[2]}  v2={user[3]}"
    else:
        raise Unauthorized("The username or password is wrong")



@app.route("/v1/sentiment",methods=["POST"])
def sentiment_v1():

    auth = request.authorization
    data = request.get_json()

    if auth:
        username = auth.username
        password = auth.password
        sentence = data['sentence']

        if is_valid_user(username,password):
            user = get_user(username)
            v1 = user[2]

            if v1 == 1:
                score = random.uniform(-1, 1)

                return {"user": username,
                        "sentence" : sentence,
                        "score" : score}
            else:
                return Unauthorized(f"V1 : Access denied for user {username}") 
        else:
            return Unauthorized("Wrong username or password") 

    else:
        return Unauthorized("Missing username and password")


@app.route("/v2/sentiment",methods=["POST"])
def sentiment_v2():
    auth = request.authorization
    data = request.get_json()

    if auth:
        username = auth.username
        password = auth.password
        sentence = data['sentence']

        if is_valid_user(username,password):
            user = get_user(username)
            v2 = user[3]

            if v2 == 1:
                analyzer = SentimentIntensityAnalyzer()
                score = analyzer.polarity_scores(sentence)

                return {"user": username,
                        "sentence" : sentence,
                        "score" : score}
            else:
                return Unauthorized(f"V1 : Access denied for user {username}") 
        else:
            return Unauthorized("Wrong username or password") 

    else:
        return Unauthorized("Missing username and password")



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)