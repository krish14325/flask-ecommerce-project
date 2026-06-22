from flask import Flask , render_template , session , url_for , redirect , request , flash
import mysql.connector as connector
conn = connector.connect(
    host = "localhost",
    user = "root",
    password = "3333#",
    database = "electronics_store"
)

app = Flask(__name__)
app.secret_key = "krishna@123"

@app.route("/",methods=["GET","POST"])
def register():
    if request.method == "POST":
        Name = request.form["name"]
        Email = request.form["email"]
        Password = request.form["password"]
        Confirm = request.form["Confirm"]
        if not Name.strip():
            flash("Please Enter Name","Error")
            return render_template("register.html")
        if not Email.strip():
            flash("Please Enter Email","Error")
            return render_template("register.html")
        if not Password.strip():
            flash("Please Enter Password","Error")
            return render_template("register.html")
        if not Confirm.strip():
            flash("Please Confirm Password","Error")
            return render_template("register.html")
        if Password != Confirm:
            flash("Password Does Not Match","Error")
            return render_template("register.html")
        query = """
            SELECT * FROM USERS
            WHERE EMAIL = %s
            """
        values = (Email,)
        cur = conn.cursor()
        cur.execute(query,values)
        found = cur.fetchone()
        if not found:
            query = """
                INSERT INTO USERS
                (NAME , EMAIL , PASSWORD)
                VALUES
                (%s,%s,%s)
                """
            values = (Name , Email , Password)
            cur = conn.cursor()
            cur.execute(query,values)
            conn.commit()
            flash ("User Registered Sucessfully" , "Success")
            return redirect(url_for("login"))
        flash ("E-mail Already Registered" , "Error")
        return render_template("register.html")
    return render_template("register.html")

@app.route("/login" , methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if not email.strip():
            flash("Enter Email","Error")
            return render_template("login.html")
        if not password.strip():
            flash("Enter Password","Error")
            return render_template("login.html")
        query = """
                SELECT * FROM USERS
                WHERE EMAIL = %s AND PASSWORD = %s
                """
        values = (email , password)
        cur = conn.cursor()
        cur.execute(query,values)
        data = cur.fetchone()
        if not data:
            flash("User Not Found" , "Error")
            return render_template("login.html")
        session["user_id"] = data[0]
        flash("Login Sucessfully" , "Success")
        return redirect(url_for("home"))
    return render_template("login.html")

@app.route("/home",methods=["GET","POST"])
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))
    query = """
            SELECT * FROM 
            PRODUCTS
            """
    cur = conn.cursor()
    cur.execute(query)
    data = cur.fetchall()
    if not data:
        flash("No Products Found")
        return render_template("dashboard.html")
    return render_template("dashboard.html" , products=data)

@app.route("/product/<int:product_id>",methods=["GET" , "POST"])
def product(product_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    user = session["user_id"]
    if request.method == "GET":
        query = """
            SELECT * 
            FROM PRODUCTS
            WHERE PRODUCT_ID = %s
            """
        values = (product_id,)
        cur = conn.cursor()
        cur.execute(query, values)
        found = cur.fetchone()
        if not found:
            flash("Product Not Found","Error")
            return redirect(url_for("home"))
        return render_template("product.html", item=found)
    if request.method == "POST":
        user = session["user_id"]
    # ✅ First check if stock is available
        stock_query = "SELECT STOCK FROM PRODUCTS WHERE PRODUCT_ID = %s"
        cur = conn.cursor()
        cur.execute(stock_query, (product_id,))
        stock = cur.fetchone()
    
        if not stock or stock[0] <= 0:
            flash("Product Out Of Stock", "Error")
            return redirect(url_for("product", product_id=product_id))
    
        query = "SELECT * FROM CART WHERE USER_ID = %s AND PRODUCT_ID = %s"
        cur = conn.cursor()
        cur.execute(query, (user, product_id))
        found = cur.fetchone()
    
        if found:
            query = """
            UPDATE CART SET QUANTITY = QUANTITY + 1
            WHERE USER_ID = %s AND PRODUCT_ID = %s
            """
            cur = conn.cursor()
            cur.execute(query, (user, product_id))
        else:
            query = """
                INSERT INTO CART (USER_ID, PRODUCT_ID, QUANTITY)
                VALUES (%s, %s, %s)
                """
            cur = conn.cursor()
            cur.execute(query, (user, product_id, 1))
    
    # ✅ Decrease stock in BOTH cases
        stock_query = """
            UPDATE PRODUCTS SET STOCK = STOCK - 1
            WHERE PRODUCT_ID = %s
        """
        cur = conn.cursor()
        cur.execute(stock_query, (product_id,))
        conn.commit()
    
        flash("Item Added To Cart", "Success")
        return redirect(url_for("product", product_id=product_id))
    
@app.route("/cart" , methods=["GET" , "POST"])
def cart():
    if "user_id" not in session:
        return redirect(url_for("login"))
    user = session["user_id"]
    if request.method == "GET":
        query = """
            SELECT PRODUCTS.PRODUCT_ID,PRODUCTS.IMAGE_URL , PRODUCTS.PRODUCT_NAME , PRODUCTS.PRICE , CART.QUANTITY, PRODUCTS.PRICE*CART.QUANTITY 
            FROM CART
            JOIN PRODUCTS
            ON CART.PRODUCT_ID = PRODUCTS.PRODUCT_ID
            WHERE USER_ID = %s
            """
        values = (user,)
        cur = conn.cursor()
        cur.execute(query,values)
        items = cur.fetchall()
        if not items:
            flash("No Items In Cart" , "Error")
        query = """
                SELECT SUM(PRODUCTS.PRICE * CART.QUANTITY)
                FROM CART
                JOIN PRODUCTS
                ON CART.PRODUCT_ID = PRODUCTS.PRODUCT_ID
                WHERE USER_ID = %s
                """
        cur.execute(query, (user,))
        grand_total = cur.fetchone()[0]
        return render_template("cart.html" ,items=items , grand_total=grand_total)
    product_id = int(request.form["id"])
    query = """
            DELETE FROM CART
            WHERE USER_ID = %s AND PRODUCT_ID = %s
            """
    values = (user , product_id)
    cur = conn.cursor()
    cur.execute(query , values)
    conn.commit()
    flash("Item Removed" , "Success")
    return redirect(url_for("cart"))

@app.route("/increase" ,methods=["POST"])
def increase():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    user = session["user_id"]
    product_id = int(request.form["product_id"])
    query = """
            SELECT STOCK
            FROM PRODUCTS
            WHERE PRODUCT_ID = %s
            """
    values = (product_id,)
    cur = conn.cursor()
    cur.execute(query, values)
    stock = cur.fetchone()
    if stock[0] <= 0:
        flash("Product Out Of Stock", "Error")
        return redirect(url_for("cart"))
    query = """
            UPDATE CART
            SET QUANTITY = QUANTITY + 1
            WHERE USER_ID = %s AND PRODUCT_ID = %s
            """
    values = (user, product_id)
    cur = conn.cursor()
    cur.execute(query , values)
    conn.commit()
    query = """
            UPDATE PRODUCTS
            SET STOCK = STOCK - 1
            WHERE PRODUCT_ID = %s
            """
    values = (product_id,)
    cur = conn.cursor()
    cur.execute(query , values)
    print("Rows Updated:", cur.rowcount)
    conn.commit()
    return redirect(url_for("cart"))

@app.route("/decrease" ,methods=["POST"])
def decrease():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    user = session["user_id"]
    product_id = int(request.form["product_id"])
    query = """
            SELECT QUANTITY
            FROM CART
            WHERE USER_ID = %s AND PRODUCT_ID = %s
            """
    values = (user , product_id)
    cur = conn.cursor()
    cur.execute(query,values)
    found = cur.fetchone()
    if not found:
        flash("Item Not Found", "Error")
        return redirect(url_for("cart"))
    if found[0] == 1:
        query = """
                DELETE FROM CART
                WHERE USER_ID = %s AND PRODUCT_ID = %s
                """
        values = (user,product_id)
        cur = conn.cursor()
        cur.execute(query,values)
        conn.commit()
        query = """
            UPDATE PRODUCTS
            SET STOCK = STOCK + 1
            WHERE PRODUCT_ID = %s
            """
        values = (product_id,)
        cur = conn.cursor()
        cur.execute(query , values)
        conn.commit()
        flash("Item Removed From Cart","Success")
        return redirect(url_for("cart"))
    query = """
            UPDATE CART
            SET QUANTITY = QUANTITY - 1
            WHERE USER_ID = %s AND PRODUCT_ID = %s
            """
    values = (user, product_id)
    cur = conn.cursor()
    cur.execute(query , values)
    conn.commit()
    query = """
            UPDATE PRODUCTS
            SET STOCK = STOCK + 1
            WHERE PRODUCT_ID = %s
            """
    values = (product_id,)
    cur = conn.cursor()
    cur.execute(query , values)
    conn.commit()
    return redirect(url_for("cart"))

@app.route("/place_order", methods=["POST"])
def placeorder():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user = session["user_id"]
    total = request.form["total"]

    # Get all cart items
    query = """
        SELECT PRODUCT_ID, QUANTITY
        FROM CART
        WHERE USER_ID = %s
    """
    values = (user,)

    cur = conn.cursor()
    cur.execute(query, values)
    found = cur.fetchall()

    if not found:
        flash("No Items Found", "Error")
        return redirect(url_for("cart"))

    # Create order
    query = """
        INSERT INTO ORDERS
        (USER_ID, TOTAL_AMOUNT)
        VALUES
        (%s, %s)
    """
    values = (user, total)

    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()

    order_id = cur.lastrowid

    # Add all products to ORDER_ITEMS
    for item in found:
        product_id = item[0]
        quantity = item[1]

        query = """
            INSERT INTO ORDER_ITEMS
            (ORDER_ID, PRODUCT_ID, QUANTITY)
            VALUES
            (%s, %s, %s)
        """

        values = (order_id, product_id, quantity)

        cur = conn.cursor()
        cur.execute(query, values)

    conn.commit()

    # Empty cart
    query = """
        DELETE FROM CART
        WHERE USER_ID = %s
    """

    values = (user,)

    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()

    flash("Order Placed Successfully", "Success")
    return redirect(url_for("home"))

@app.route("/orders", methods=["GET"])
def orders():
    if "user_id" not in session:
        return redirect(url_for("login"))
    user = session["user_id"]
    query = """
            SELECT * 
            FROM ORDERS
            WHERE USER_ID = %s
            """
    values = (user,)
    cur = conn.cursor()
    cur.execute(query , values)
    found = cur.fetchall()
    if not found:
        flash("No Orders Found","Error")
        return render_template("orders.html")
    return render_template("orders.html", items = found)

@app.route("/orderitems" , methods=["GET"])
def orderitems():
    if "user_id" not in session:
        return redirect(url_for("login"))
    user = session["user_id"]
    order_id = request.args["order_id"]
    query = """
            SELECT PRODUCTS.PRODUCT_NAME , ORDER_ITEMS.QUANTITY , PRODUCTS.PRICE , PRODUCTS.IMAGE_URL
            FROM ORDER_ITEMS
            JOIN PRODUCTS
            ON ORDER_ITEMS.PRODUCT_ID = PRODUCTS.PRODUCT_ID
            WHERE ORDER_ID = %s
            """
    values = (order_id,)
    cur = conn.cursor()
    cur.execute(query,values)
    found = cur.fetchall()
    if not found:
        flash("No Products Found","Error")
        return render_template("viewdetails.html")
    return render_template("viewdetails.html" , items=found)

@app.route("/search")
def search():

    if "user_id" not in session:
        return redirect(url_for("login"))

    keyword = request.args.get("search", "").strip()

    if not keyword:
        flash("Please Enter Search Term", "Error")
        return redirect(url_for("home"))

    query = """
            SELECT *
            FROM PRODUCTS
            WHERE PRODUCT_NAME LIKE %s
            """

    values = (f"%{keyword}%",)

    cur = conn.cursor()
    cur.execute(query, values)
    products = cur.fetchall()

    return render_template("search.html", products=products)

@app.route("/category")
def category():

    if "user_id" not in session:
        return redirect(url_for("login"))

    category_id = request.args.get("category")

    if not category_id:
        flash("Please Select Category", "Error")
        return redirect(url_for("home"))

    query = """
            SELECT *
            FROM PRODUCTS
            WHERE CATEGORY_ID = %s
            """

    cur = conn.cursor()
    cur.execute(query, (category_id,))
    products = cur.fetchall()

    category_names = {
        "1": "Smartphones",
        "2": "Laptops",
        "3": "Audio & Headphones"
    }

    category_name = category_names.get(
        category_id,
        "Products"
    )

    return render_template(
        "category.html",
        products=products,
        category_name=category_name
    )
if __name__=="__main__": 
    app.run(debug=True)