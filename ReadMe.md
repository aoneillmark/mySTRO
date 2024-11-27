PLACEHOLDER

Todoapp

How to use this repo
If you have a look at the commit history, you'll notice I have arranged all the
commits in order for you to follow the development of the Todo app step by step.

Stack

Python 3.10
Good Ol' Javascript

W3CSS for simple styling

SQLite for in memory data storage


Pre
Make sure you have Python3 on your machine.

Running the app
To run the app:

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip && pip install -r requirements.txt
flask create_all # Create database and tables inside it
flask populate   # Populate tables with some initial data
flask run        # Spin the server


You can now browse to http://localhost:5000 and see the app live.