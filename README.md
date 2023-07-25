
# Sentiment analysis API

The API will manage request with sentences to predict their positive/negative nature. 

Access to the API is granted through file [credentials.csv](credentials.csv) which contains all the permission for each user depending on model `v1` and `v2`. 
- `0` : granted 
- `1` : denied 

# API Endpoints:

| Endpoints | Type | Description |
|----------|---|---------|
| `/status` |`GET`| returns 1 if API is working correctly |
| `/welcome`|`GET` | returns a greetings message with the `username` indicated in the query|
| `/permissions`|`POST` | returns list of user permissions |
| `/v1/sentiment`|`POST` | return the score for the sentence given in parameters for model in `version 1`|
| `/v2/sentiment`|`POST` | return the score for the sentence given in parameters for model in `version 2`|

# Files
The API is made from the following files:

- [credentials.csv](credentials.csv) : list of user credentials and their permissions
- [requirements.txt](requirements.txt) : list of packages to install for the API to run
- [app.py](app.py) : main api with all the routes

# Setup
Install the required packages :
```bash
pip install -r requirements.txt
```
To start the API you can either:
- Run with Flask server:
    ```bash
    export FLASK_APP=app.py
    flask run --host=0.0.0.0 --port=5000
    ```
- Run with python:
    ```bash
    python app.py
    ```

# Results

## `/status`

```bash
curl -X GET http://localhost:5000/status
```
```html
1
```

## `/welcome`

**no user**
```bash
curl -X GET http://localhost:5000/welcome
```
```json
{
    "validation_error":{
        "query_params":[{
            "loc":["name"],
            "msg":"field required",
            "type":"value_error.missing"}]
        }
}
```

**wrong user**
```bash
curl -X GET http://localhost:5000/welcome/foo
```
```html
<!doctype html>
<html lang=en>
<title>401 Unauthorized</title>
<h1>Unauthorized</h1>
<p>The user is not in the database</p>
```

**valid user**
```bash
curl -X GET http://localhost:5000/welcome/Montana
```
```html
Hello Montana, welcome to the sentiment analysis API
```

## `/permissions`


**wrong user**
```bash
curl -X GET http://localhost:5000/permissions -H "username:foo" -H "password:bar"
```
```html
<!doctype html>
<html lang=en>
<title>401 Unauthorized</title>
<h1>Unauthorized</h1>
<p>The username or password is wrong</p>
```

**wrong password**
```bash
curl -X GET http://localhost:5000/permissions -H "username:Montana" -H "password:154"
```
```html
<!doctype html>
<html lang=en>
<title>401 Unauthorized</title>
<h1>Unauthorized</h1>
<p>The username or password is wrong</p>
```

**valid user**
```bash
curl -X GET http://localhost:5000/permissions -H "username:Montana" -H "password:3134"
```
```html
User Montana has the following rights: v1=0  v2=0
```

## `/v1/sentiment`

**no authentication**
```bash
curl -X POST http://localhost:5000/v1/sentiment -d '{"sentence":"life is good"}' -H 'Content-Type: application/json'
```
```html
<!doctype html>
<html lang=en>
<title>401 Unauthorized</title>
<h1>Unauthorized</h1>
<p>Missing username and password</p>
```

**wrong password**
```bash
curl -X POST http://localhost:5000/v1/sentiment --user 'Megan:67' -d '{"sentence":"life is good"}' -H 'Content-Type: application/json'
```
```html
<!doctype html>
<html lang=en>
<title>401 Unauthorized</title>
<h1>Unauthorized</h1>
<p>Wrong username or password</p>
```

**valid user without v1 access rights**
```bash
curl -X POST http://localhost:5000/v1/sentiment --user 'Montana:3134' -d '{"sentence":"life is good"}' -H 'Content-Type: application/json'
```
```html
<!doctype html>
<html lang=en>
<title>401 Unauthorized</title>
<h1>Unauthorized</h1>
<p>V1 : Access denied for user Montana</p>
```

**valid user with v1 access rights**
```bash
curl -X POST http://localhost:5000/v1/sentiment --user 'Megan:6837' -d '{"sentence":"life is good"}' -H 'Content-Type: application/json'
```
```json
{
  "score": -0.11577594605269548,
  "sentence": "life is good",
  "user": "Megan"
}
```

## `/v2/sentiment`

**no authentication**
```bash
curl -X POST http://localhost:5000/v2/sentiment -d '{"sentence":"life is good"}' -H 'Content-Type: application/json'
```
```html
<!doctype html>
<html lang=en>
<title>401 Unauthorized</title>
<h1>Unauthorized</h1>
<p>Missing username and password</p>
```

**wrong password**
```bash
curl -X POST http://localhost:5000/v2/sentiment --user 'Quintessa:159' -d '{"sentence":"life is good"}' -H 'Content-Type: application/json'
```
```html
<!doctype html>
<html lang=en>
<title>401 Unauthorized</title>
<h1>Unauthorized</h1>
<p>Wrong username or password</p>
```

**valid user without v2 access rights**
```bash
curl -X POST http://localhost:5000/v2/sentiment --user 'Montana:3134' -d '{"sentence":"life is good"}' -H 'Content-Type: application/json'
```
```html
<!doctype html>
<html lang=en>
<title>401 Unauthorized</title>
<h1>Unauthorized</h1>
<p>V1 : Access denied for user Montana</p>
```

**valid user with v2 access rights (positive sentence)**
```bash
curl -X POST http://localhost:5000/v2/sentiment --user 'Quintessa:8790' -d '{"sentence":"life is good"}' -H 'Content-Type: application/json'
```
```json
{
  "score": {
    "compound": 0.4404,
    "neg": 0.0,
    "neu": 0.408,
    "pos": 0.592
  },
  "sentence": "life is good",
  "user": "Quintessa"
}
```

**valid user with v2 access rights (negative sentence)**
```bash
curl -X POST http://localhost:5000/v2/sentiment --user 'Quintessa:8790' -d '{"sentence":"life is bad"}' -H 'Content-Type: application/json'
```
```json
{
  "score": {
    "compound": -0.5423,
    "neg": 0.636,
    "neu": 0.364,
    "pos": 0.0
  },
  "sentence": "life is bad",
  "user": "Quintessa"
}
```