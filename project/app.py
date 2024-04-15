import sqlite3
import sqlalchemy
from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, apology

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///vapes.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    vapes1 = db.execute("SELECT * FROM vape LIMIT 4")
    vapes2 = db.execute("SELECT * FROM vape LIMIT 4 OFFSET 4")
    users = db.execute("SELECT * FROM users")
    return render_template("index.html", vapes1= vapes1, vapes2 = vapes2, users = users)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", [request.form.get("username")])

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)
        
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()
    session["user_id"] = None

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    session.clear()

    if request.method == "POST":
        users = db.execute("SELECT username FROM users")
        i = 0
        for user in users:
            if request.form.get("username") in users[i]["username"]:
                i += 1
                return apology("username already registered", 400)
        if not request.form.get("username"):
            return apology("must provide username", 400)
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        elif not request.form.get("confirmation"):
            return apology("must provide confirmation password", 400)
        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("passwords don't match", 400)
        
        db.execute("INSERT INTO users(username, hash) VALUES(?,?)",request.form.get("username"), generate_password_hash(request.form.get("password"), method = 'pbkdf2', salt_length = 16))
        return render_template("login.html")
    else:
        return render_template("register.html")
    

@app.route("/add", methods=["GET", "POST"])
def add():
    """Add to cart"""
    if request.method == "POST":
        if session.get("user_id") is None :
            return render_template("register.html")
        else:
            id = int(request.form.get("cart-button"))

            vapes = db.execute("SELECT * FROM vape")
            carts = db.execute("SELECT * FROM cart")
        
            i = 0
            quantity = 1
            for vape in vapes:
                if id == int(vapes[i]["id"]):
                    name = vapes[i]["name"]
                    price = vapes[i]["price"]

                    j = 0
                    flag = 0
                    for cart in carts:
                        if name == carts[j]["name"]:
                            quantity = carts[j]["quantity"]
                            quantity += 1
                            db.execute("UPDATE cart SET quantity = ?, total_price = ? WHERE name = ? AND id = ?", quantity, quantity*price, name, carts[j]["id"])
                            flag = 1
                            break
                        else:
                            j += 1

                    if flag == 0:
                        db.execute("INSERT INTO cart(name, quantity, total_price) VALUES (?,?,?)",name, quantity, price*quantity)

                i += 1
            
            return redirect("/")
    else:
        carts = db.execute("SELECT * FROM cart")
        return render_template("cart.html", carts = carts)

@app.route("/cart", methods=["GET", "POST"])
def cart():
    """View cart"""
    if request.method == "POST":
        return redirect("/")
    else:
        carts = db.execute("SELECT * FROM cart")
        grand = 0
        i = 0
        for cart in carts:
            grand += carts[i]["total_price"]
            i += 1

        hide = 0
        if grand > 0:
            hide = 1
        return render_template("cart.html", carts = carts, hide = hide, grand = grand, pay = 0)


@app.route("/clear", methods=["GET", "POST"])
def clear():
    """Clear the cart"""
    db.execute("DELETE FROM cart")
    return render_template("cart.html", hide = 0, pay = 0)

@app.route("/pay", methods = ["GET", "POST"])
def pay():
    """Payment"""
    if request.method == "POST":
        name = request.form.get("fullname")
        address1 = request.form.get("address1")
        address2 = request.form.get("address2")
        email = request.form.get("email")
        phone = request.form.get("phone")
        postal = request.form.get("postal")
        gateway = request.form.get("gateway")
        amount = int(request.form.get("amount"))


        if not name:
            return apology("must provide name", 400)
        elif not address1:
            return apology("must provide address1", 400)
        elif not address2:
            return apology("must provide address2", 400)
        elif not email:
            return apology("must provide email", 400)
        elif not phone:
            return apology("must provide phone", 400)
        elif not postal:
            return apology("must provide postal", 400)
        elif not gateway:
            return apology("must provide gateway", 400)
        

        db.execute("INSERT INTO payments (user_id, name, address1, address2, email, phone, postal, amount) VALUES (?,?,?,?,?,?,?,?)", session["user_id"], name, address1, address2, email, phone, postal, amount)

        db.execute("DELETE FROM cart")
        return render_template("cart.html", hide = 0, pay = 1)
 
    else:
        carts = db.execute("SELECT * FROM cart")
        grand = 0
        i = 0
        for cart in carts:
            grand += carts[i]["total_price"]
            i += 1
        return render_template("pay.html", grand = grand)
