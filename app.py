# Citation for the following:
# Date: 5/22/23
# Adapted from: Flask Starter App by osu-cs340-ecampus
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app

from flask import Flask, flash, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os

app = Flask(__name__)

app.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
app.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
app.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

SECRET_KEY = os.environ.get("SECRET_KEY")
app.secret_key = str.encode(str(SECRET_KEY))

PORT = os.environ.get("PORT")

mysql = MySQL(app)

# Routes
@app.route("/")
def Home():
    return redirect("/customers")

### Customers ###
# route for customers page
@app.route("/customers", methods=["GET", "POST"])
def customers():
    if request.method == "GET":
        # display Customer data
        query = "SELECT customer_id AS 'ID', customer_name AS 'Name', customer_phone AS 'Phone', customer_email AS 'Email' FROM Customers;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render customers page
        return render_template("customers.j2", data=data)
    
    if request.method == "POST":
        # search for a Customer by name/phone/email
        if request.form.get("Search_Customer"):
            customer_search = request.form["customer_search"]
            search_by = request.form["search_by"]

            query = f"SELECT customer_id AS 'ID', customer_name AS 'Name', customer_phone AS 'Phone', customer_email AS 'Email' FROM Customers WHERE {search_by} = '{customer_search}';"
            cur = mysql.connection.cursor()
            cur.execute(query)
            data = cur.fetchall()

            try:
                data[0]
            except:
                if customer_search == '':
                    flash("No results found for empty string.")
                else:
                    flash(f"No Customers found with {search_by} of {customer_search}.")
            
            # render search_customers page
            return render_template("search_customers.j2", data=data)
    
# route for adding a Customer
@app.route("/add_customers", methods=["GET", "POST"])
def add_customers():
    if request.method == "GET":
        # user presses Add New Customer button in customers page
        return render_template("add_customers.j2")
    
    if request.method == "POST":
        # user presses Add Customer button
        if request.form.get("Add_Customer"):
            customer_name = request.form["customer_name"]
            customer_phone = request.form["customer_phone"]
            customer_email = request.form["customer_email"]

            # insert new Customer into database
            query = "INSERT INTO Customers (customer_name, customer_phone, customer_email) VALUES (%s, %s, %s);"
            cur = mysql.connection.cursor()
            cur.execute(query, (customer_name, customer_phone, customer_email))
            mysql.connection.commit()

            # redirect back to customers page
            return redirect("/customers")
    
# route for deleting a Customer
@app.route("/delete_customers/<int:customer_id>", methods=["GET", "POST"])
def delete_customers(customer_id):
    if request.method == "GET":
        query = "SELECT customer_id AS 'ID', customer_name AS 'Name', customer_phone AS 'Phone', customer_email AS 'Email' FROM Customers WHERE customer_id = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query, (customer_id,))
        data = cur.fetchall()

        return render_template("delete_customers.j2", data=data)

    if request.method == "POST":
        # user presses Delete button
        if request.form.get("Delete_Customer"):
            query = "DELETE FROM Customers WHERE customer_id = %s;"
            cur = mysql.connection.cursor()
            cur.execute(query, (customer_id,))
            mysql.connection.commit()

            # redirect back to customers page
            return redirect("/customers")

# route for updating a Customer
@app.route("/update_customers/<int:customer_id>", methods=["GET", "POST"])
def update_customers(customer_id):
    if request.method == "GET":
        query = "SELECT customer_id AS 'ID', customer_name AS 'Name', customer_phone AS 'Phone', customer_email AS 'Email' FROM Customers WHERE customer_id = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query, (customer_id,))
        data = cur.fetchall()

        return render_template("update_customers.j2", data=data)
    
    if request.method == "POST":
        # user presses Update button
        if request.form.get("Update_Customer"):
            customer_name = request.form["customer_name"]
            customer_phone = request.form["customer_phone"]
            customer_email = request.form["customer_email"]

            query = "UPDATE Customers SET customer_name = %s, customer_phone = %s, customer_email = %s WHERE customer_id = %s;"
            cur = mysql.connection.cursor()
            cur.execute(query, (customer_name, customer_phone, customer_email, customer_id))
            mysql.connection.commit()

            return redirect("/customers")

# Listener
if __name__ == "__main__":
    # Start the app on port 3000, it will be different once hosted
    app.run(port=PORT, debug=True)
