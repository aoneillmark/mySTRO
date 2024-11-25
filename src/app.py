from flask import Flask, render_template, request
# import requests

app = Flask(__name__)

@app.route("/")
def hello_world():
    # return "Hello World!"
    return render_template("index.html")

@app.route("/library")
def library():
    return render_template("library.html")