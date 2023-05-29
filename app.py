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
        
### Products ###
# route for products page
@app.route("/products", methods=["GET", "POST"])
def products():
    if request.method == "GET":
        # display Product data
        query = "SELECT product_id AS 'ID', product_description AS 'Description', product_price AS 'Price' FROM Products;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render products page
        return render_template("products.j2", data=data)
    
# route for adding a Product
@app.route("/add_products", methods=["GET", "POST"])
def add_products():
    if request.method == "GET":
        # user presses Add New Product button in products page
        return render_template("add_products.j2")
    
    if request.method == "POST":
        # user presses Add Product button
        if request.form.get("Add_Product"):
            product_description = request.form["product_description"]
            product_price = request.form["product_price"]

            # insert new Product into database
            query = "INSERT INTO Products (product_description, product_price) VALUES (%s, %s);"
            cur = mysql.connection.cursor()
            cur.execute(query, (product_description, product_price))
            mysql.connection.commit()

            # redirect back to products page
            return redirect("/products")
        
# route for deleting a Product
@app.route("/delete_products/<int:product_id>", methods=["GET", "POST"])
def delete_products(product_id):
    if request.method == "GET":
        query = "SELECT product_id AS 'ID', product_description AS 'Description', product_price AS 'Price' FROM Products WHERE product_id = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query, (product_id,))
        data = cur.fetchall()

        return render_template("delete_products.j2", data=data)

    if request.method == "POST":
        # user presses Delete button
        if request.form.get("Delete_Product"):
            query = "DELETE FROM Products WHERE product_id = %s;"
            cur = mysql.connection.cursor()
            cur.execute(query, (product_id,))
            mysql.connection.commit()

            # redirect back to products page
            return redirect("/products")
        
# route for updating a Product
@app.route("/update_products/<int:product_id>", methods=["GET", "POST"])
def update_products(product_id):
    if request.method == "GET":
        query = "SELECT product_id AS 'ID', product_description AS 'Description', product_price AS 'Price' FROM Products WHERE product_id = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query, (product_id,))
        data = cur.fetchall()

        return render_template("update_products.j2", data=data)
    
    if request.method == "POST":
        # user presses Update button
        if request.form.get("Update_Product"):
            product_description = request.form["product_description"]
            product_price = request.form["product_price"]

            query = "UPDATE Products SET product_description = %s, product_price = %s WHERE product_id = %s;"
            cur = mysql.connection.cursor()
            cur.execute(query, (product_description, product_price, product_id))
            mysql.connection.commit()

            return redirect("/products")

### Stores ###
# route for stores page
@app.route("/stores", methods=["GET", "POST"])
def stores():
    if request.method == "GET":
        # display Store data
        query = "SELECT store_id AS 'ID', store_number AS 'Store Number', store_phone AS 'Phone', store_email AS 'Email' FROM Stores;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render stores page
        return render_template("stores.j2", data=data)
    
# route for adding a Store
@app.route("/add_stores", methods=["GET", "POST"])
def add_stores():
    if request.method == "GET":
        # user presses Add New Store button in stores page
        return render_template("add_stores.j2")
    
    if request.method == "POST":
        # user presses Add Store button
        if request.form.get("Add_Store"):
            store_number = request.form["store_number"]
            store_phone = request.form["store_phone"]
            store_email = request.form["store_email"]

            # insert new Store into database
            query = "INSERT INTO Stores (store_number, store_phone, store_email) VALUES (%s, %s, %s);"
            cur = mysql.connection.cursor()
            cur.execute(query, (store_number, store_phone, store_email))
            mysql.connection.commit()

            # redirect back to stores page
            return redirect("/stores")
        
# route for deleting a Store
@app.route("/delete_stores/<int:store_id>", methods=["GET", "POST"])
def delete_stores(store_id):
    if request.method == "GET":
        query = "SELECT store_id AS 'ID', store_number AS 'Store Number', store_phone AS 'Phone', store_email AS 'Email' FROM Stores WHERE store_id = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query, (store_id,))
        data = cur.fetchall()

        return render_template("delete_stores.j2", data=data)

    if request.method == "POST":
        # user presses Delete button
        if request.form.get("Delete_Store"):
            query = "DELETE FROM Stores WHERE store_id = %s;"
            cur = mysql.connection.cursor()
            cur.execute(query, (store_id,))
            mysql.connection.commit()

            # redirect back to stores page
            return redirect("/stores")
        
# route for updating a Store
@app.route("/update_stores/<int:store_id>", methods=["GET", "POST"])
def update_stores(store_id):
    if request.method == "GET":
        query = "SELECT store_id AS 'ID', store_number AS 'Store Number', store_phone AS 'Phone', store_email AS 'Email' FROM Stores WHERE store_id = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query, (store_id,))
        data = cur.fetchall()

        return render_template("update_stores.j2", data=data)
    
    if request.method == "POST":
        # user presses Update button
        if request.form.get("Update_Store"):
            store_number = request.form["store_number"]
            store_phone = request.form["store_phone"]
            store_email = request.form["store_email"]

            query = "UPDATE Stores SET store_number = %s, store_phone = %s, store_email = %s WHERE store_id = %s;"
            cur = mysql.connection.cursor()
            cur.execute(query, (store_number, store_phone, store_email, store_id))
            mysql.connection.commit()

            return redirect("/stores")
        
### Store Products ###
# route for store_products page
@app.route("/store_products", methods=["GET"])
def store_products():
    if request.method == "GET":
        # display Store Product data
        query = "SELECT store_product_id AS 'ID', Stores.store_number AS 'Store Number', Products.product_description AS 'Product', number_in_stock AS 'In Stock' \
                 FROM StoreProducts \
                 INNER JOIN Stores ON Stores.store_id = StoreProducts.store_id \
                 INNER JOIN Products ON Products.product_id = StoreProducts.product_id;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render store_products page
        return render_template("store_products.j2", data=data)
    
# route for adding a Store Product
@app.route("/add_store_products", methods=["GET", "POST"])
def add_store_products():
    if request.method == "GET":
        # query to grab store id/number data for dropdown
        query = "SELECT store_id, store_number FROM Stores;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        store_data = cur.fetchall()

        # query to grab product id/description data for dropdown
        query2 = "SELECT product_id, product_description FROM Products;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        product_data = cur.fetchall()

        # user presses Add New Store Product button in store_products page
        return render_template("add_store_products.j2", stores=store_data, products=product_data)
    
    if request.method == "POST":
        # user presses Add Store Product button
        if request.form.get("Add_Store_Product"):
            store_id = request.form["store_number"]
            product_id = request.form["product_description"]
            number_in_stock = request.form["number_in_stock"]

            # insert new Store Product into database
            query = "INSERT INTO StoreProducts (store_id, product_id, number_in_stock) VALUES (%s, %s, %s);"
            cur = mysql.connection.cursor()
            cur.execute(query, ( store_id, product_id, number_in_stock))
            mysql.connection.commit()

            # redirect back to store_products page
            return redirect("/store_products")

# route for deleting a Store Product
@app.route("/delete_store_products/<int:store_product_id>", methods=["GET", "POST"])
def delete_store_products(store_product_id):
    if request.method == "GET":
        query = "SELECT store_product_id AS 'ID', Stores.store_number AS 'Store Number', Products.product_description AS 'Product', number_in_stock AS 'In Stock' \
                 FROM StoreProducts \
                 INNER JOIN Stores ON Stores.store_id = StoreProducts.store_id \
                 INNER JOIN Products ON Products.product_id = StoreProducts.product_id \
                 WHERE store_product_id = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query, (store_product_id,))
        data = cur.fetchall()

        return render_template("delete_store_products.j2", data=data)

    if request.method == "POST":
        # user presses Delete button
        if request.form.get("Delete_Store_Product"):
            query = "DELETE FROM StoreProducts WHERE store_product_id = %s;"
            cur = mysql.connection.cursor()
            cur.execute(query, (store_product_id,))
            mysql.connection.commit()

            # redirect back to store_products page
            return redirect("/store_products")

# route for updating a Store Product
@app.route("/update_store_products/<int:store_product_id>", methods=["GET", "POST"])
def update_store_products(store_product_id):
    if request.method == "GET":
        query = "SELECT store_product_id AS 'ID', Stores.store_number AS 'Store Number', Products.product_description AS 'Product', number_in_stock AS 'In Stock' \
                 FROM StoreProducts \
                 INNER JOIN Stores ON Stores.store_id = StoreProducts.store_id \
                 INNER JOIN Products ON Products.product_id = StoreProducts.product_id \
                 WHERE store_product_id = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query, (store_product_id,))
        data = cur.fetchall()

        # query to grab store id/number data for dropdown
        query2 = "SELECT store_id, store_number FROM Stores;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        store_data = cur.fetchall()

        # query to grab product id/description data for dropdown
        query3 = "SELECT product_id, product_description FROM Products;"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        product_data = cur.fetchall()

        return render_template("update_store_products.j2", data=data, stores=store_data, products=product_data)
    
    if request.method == "POST":
        # user presses Update button
        if request.form.get("Update_Store_Product"):
            store_id = request.form["store_number"]
            product_id = request.form["product_description"]
            number_in_stock = request.form["number_in_stock"]

            query = "UPDATE StoreProducts SET store_id = %s, product_id = %s, number_in_stock = %s WHERE store_product_id = %s;"
            cur = mysql.connection.cursor()
            cur.execute(query, (store_id, product_id, number_in_stock, store_product_id))
            mysql.connection.commit()

            return redirect("/store_products")
        
### Orders/OrderDetails ###
# route for orders page
@app.route("/orders", methods=["GET"])
def orders():
    if request.method == "GET":
        # display Order data
        query = "SELECT order_id AS 'ID', order_date AS 'Date', Customers.customer_name AS 'Customer', Stores.store_number AS 'Store Number', order_notes AS 'Notes' \
                 FROM Orders \
                 LEFT JOIN Customers ON Customers.customer_id = Orders.customer_id \
                 LEFT JOIN Stores ON Stores.store_id = Orders.store_id;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        order_data = cur.fetchall()

        # display Order Detail data
        query2 = "SELECT order_detail_id AS 'ID', order_id AS 'Order ID', Products.product_description AS 'Product', order_quantity AS 'Quantity', line_total AS 'Line Total' \
                  FROM OrderDetails \
                  INNER JOIN Products \
                  ON Products.product_id = OrderDetails.product_id;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        order_detail_data = cur.fetchall()

        # render orders page
        return render_template("orders.j2", order_data=order_data, order_detail_data=order_detail_data)
    
# route for adding an Order
@app.route("/add_orders", methods=["GET", "POST"])
def add_orders():
    if request.method == "GET":
        # query to grab customer id/name data for dropdown
        query = "SELECT customer_id, customer_name FROM Customers;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        customer_data = cur.fetchall()

        # query to grab store id/number data for dropdown
        query2 = "SELECT store_id, store_number FROM Stores;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        store_data = cur.fetchall()

        # user presses Add New Order button in orders page
        return render_template("add_orders.j2", customers=customer_data, stores=store_data)
    
    if request.method == "POST":
        # user presses Add Order button
        if request.form.get("Add_Order"):
            order_date = request.form["order_date"]
            customer_id = request.form["customer_name"]
            store_id = request.form["store_number"]
            order_notes = request.form["order_notes"]

            # insert new Order into database
            query = "INSERT INTO Orders (order_date, customer_id, store_id, order_notes) VALUES (%s, %s, %s, %s);"
            cur = mysql.connection.cursor()
            cur.execute(query, (order_date, customer_id, store_id, order_notes))
            mysql.connection.commit()

            # redirect back to orders page
            return redirect("/orders")
        
# route for adding an OrderDetail
@app.route("/add_order_details", methods=["GET", "POST"])
def add_order_details():
    if request.method == "GET":
        # query to grab order id data for dropdown
        query = "SELECT order_id, CONCAT(order_id, ' | ', order_date, ' | ', Customers.customer_name, ' | ', Stores.store_number) AS 'Order' \
                 FROM Orders \
                 INNER JOIN Customers ON Customers.customer_id = Orders.customer_id \
                 INNER JOIN Stores ON Stores.store_id = Orders.store_id;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        order_data = cur.fetchall()

        # query to grab order id data if customer is NULL for dropdown
        query2 = "SELECT order_id, CONCAT(order_id, ' | ', order_date, ' | ', 'None', ' | ', Stores.store_number) AS 'Order' \
                  FROM Orders \
                  INNER JOIN Stores ON Stores.store_id = Orders.store_id \
                  WHERE Orders.customer_id is NULL;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        null_order_data = cur.fetchall()

        # query to grab product id/description data for dropdown
        query3 = "SELECT product_id, product_description FROM Products;"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        product_data = cur.fetchall()

        # user presses Add New Order Detail button in orders page
        return render_template("add_order_details.j2", orders=order_data, products=product_data, null_orders=null_order_data)
    
    if request.method == "POST":
        # user presses Add Order Detail button
        if request.form.get("Add_Order_Detail"):
            order_id = request.form["order_id"]
            product_id = request.form["product_description"]
            order_quantity = request.form["order_quantity"]
            line_total = request.form["line_total"]

            # insert new Order Detail into database
            query = "INSERT INTO OrderDetails (order_id, product_id, order_quantity, line_total) VALUES (%s, %s, %s, %s);"
            cur = mysql.connection.cursor()
            cur.execute(query, (order_id, product_id, order_quantity, line_total))
            mysql.connection.commit()

            # redirect back to orders page
            return redirect("/orders")

# route for deleting an Order
@app.route("/delete_orders/<int:order_id>", methods=["GET", "POST"])
def delete_orders(order_id):
    if request.method == "GET":
        query = "SELECT order_id AS 'ID', order_date AS 'Date', Customers.customer_name AS 'Customer', Stores.store_number AS 'Store Number', order_notes AS 'Notes' \
                 FROM Orders \
                 LEFT JOIN Customers ON Customers.customer_id = Orders.customer_id \
                 LEFT JOIN Stores ON Stores.store_id = Orders.store_id \
                 WHERE order_id = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query, (order_id,))
        data = cur.fetchall()

        return render_template("delete_orders.j2", data=data)

    if request.method == "POST":
        # user presses Delete button
        if request.form.get("Delete_Order"):
            query = "DELETE FROM Orders WHERE order_id = %s;"
            cur = mysql.connection.cursor()
            cur.execute(query, (order_id,))
            mysql.connection.commit()

            # redirect back to orders page
            return redirect("/orders")

# Listener
if __name__ == "__main__":
    app.run(port=PORT, debug=True)
