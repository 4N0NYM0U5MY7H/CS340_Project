"""Flask Starter App by osu-cs340-ecampus.
https://github.com/osu-cs340-ecampus/flask-starter-app"""

from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os

app = Flask(__name__)

app.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
app.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
app.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

PORT = os.environ.get("PORT")

mysql = MySQL(app)


# Routes
@app.route("/")
def root():
    query = "SELECT * FROM diagnostic;"
    query1 = "DROP TABLE IF EXISTS diagnostic;"
    query2 = "CREATE TABLE diagnostic(id INT PRIMARY KEY AUTO_INCREMENT, text VARCHAR(255) NOT NULL);"
    query3 = 'INSERT INTO diagnostic (text) VALUES ("MySQL is working!")'
    query4 = "SELECT * FROM diagnostic;"
    cur = mysql.connection.cursor()
    cur.execute(query1)
    cur.execute(query2)
    cur.execute(query3)
    cur.execute(query4)
    results = cur.fetchall()

    return "<h1>MySQL Results" + str(results[0])


# Listener
if __name__ == "__main__":
    # Start the app on port 3000, it will be different once hosted
    app.run(port=PORT, debug=True)
