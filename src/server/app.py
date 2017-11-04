#!/usr/bin/env python
# coding=utf-8

from flask import Flask, request, json, make_response
import requests
app = Flask(__name__)

@app.route("/start_rent")
def start_rent():
    r = requests.get("http://168.1.144.159:31090/api/RentHouse")
    res = {'message': r.text}
    return json.dumps(res) 

@app.route("/open_lock")
def open_lock():
    r = requests.get("http://168.1.144.159:31090/api/Renter")
    # if the first time, start timing
    result = json.loads(r.text)
    res = {'message': result}
    return json.dumps(res) 

@app.route("/close_lock")
def close_lock():
    r = requests.post("")
    res = {'message': r.text}
    return json.dumps(res)

if __name__ == "__main__":
    app.run()
