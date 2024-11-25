from flask import Flask, render_template, request

app = Flask(__name__, template_folder='src/templates')

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/library")
def library():
    return render_template("library.html")

if __name__ == "__main__":
    app.run(debug=True)