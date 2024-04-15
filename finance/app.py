import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from fractions import Fraction

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    stocks = db.execute("SELECT symbol, SUM(shares) AS shares FROM history WHERE id = ? AND action = ? GROUP BY symbol", session["user_id"], "BUY")
    sells = db.execute("SELECT symbol, SUM(shares) AS shares FROM history WHERE id = ? AND action = ? GROUP BY symbol", session["user_id"], "SELL")

    total = 0
    current = []
    holding_price = []
    i = 0
    for stock in stocks:
        for sell in sells:
            if sell["symbol"] == stock["symbol"]:
                stock["shares"] -= int(sell["shares"])

        current.append(lookup(stock["symbol"]))
        holding_price.append(round(current[i]["price"] * int(stock["shares"]),2))
        i += 1

    total = sum(holding_price) + cash[0]["cash"]

    return render_template("index.html", listcurrent = list(current), liststocks = list(stocks), stocks = stocks, current = current, cash = round(cash[0]["cash"],2), holding_price = holding_price, total = round(total,2), sells = sells)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        try:
            shares = int(request.form.get("shares"))
        except ValueError:
            return apology("shares must be a positive integer", 400)
        if not symbol:
            return apology("must provide symbol", 403)
        elif not shares:
            return apology("must provide shares", 403)
        elif lookup(symbol) == None:
            return apology("symbol doesn't exist", 400)
        elif shares < 1 :
            return apology("cannot comprehend the no of shares", 400)



        quote = lookup(symbol)
        total_price = quote["price"] * shares

        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        cash = cash[0]["cash"]

        if total_price > cash:
            return apology("inadequate balance", 404)
        else:
            current_time = datetime.datetime.now()
            db.execute("UPDATE users SET cash = ? WHERE id = ?", cash - total_price, session["user_id"])
            db.execute("INSERT INTO history(id, symbol, shares, price, holding_price, action, datetime) VALUES(?,?,?,?,?,?,?)", session["user_id"], symbol, shares, quote["price"], total_price, "BUY", current_time)
            return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    histories = db.execute("SELECT * FROM history WHERE id = ?", session["user_id"])
    return render_template("history.html", histories = histories)




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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

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

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide symbol", 400)
        elif lookup(symbol) == None:
            return apology("symbol doesn't exist", 400)
        else:
            quote = lookup(symbol)
            return render_template("quoted.html", quote = quote)
    else:
        return render_template("quote.html")



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

        db.execute("INSERT INTO users(username, hash) VALUES(?, ?)", request.form.get("username"), generate_password_hash(request.form.get("password"), method = 'pbkdf2', salt_length = 16))
        return render_template("login.html")
    else:
        return render_template("register.html")



@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":

        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        stocks = db.execute("SELECT SUM(shares) AS shares FROM history WHERE id = ? AND symbol = ? AND action = ? GROUP BY symbol", session["user_id"], symbol, "BUY")

        if not symbol:
            return apology("must provide symbol", 403)
        elif not shares:
            return apology("must provide shares", 403)
        elif not int(shares) >= 1:
            return apology("must provide a positive integer", 403)
        elif stocks[0]["shares"] == None:
            return apology("you dont own this stock", 404)
        elif int(shares) > stocks[0]["shares"]:
            return apology("invalid no of shares", 400)
        else:
            current_time = datetime.datetime.now()

            quote = lookup(symbol)
            total_price = quote["price"] * int(shares)

            cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
            cash = cash[0]["cash"]

            db.execute("UPDATE users SET cash = ? WHERE id = ?", cash + total_price, session["user_id"])
            db.execute("INSERT INTO history(id, symbol, shares, price, holding_price, action, datetime) VALUES(?,?,?,?,?,?,?)", session["user_id"], symbol, shares, quote["price"], total_price, "SELL", current_time)
            return redirect("/")
    else:
        all = db.execute("SELECT DISTINCT symbol FROM history WHERE id = ? ORDER BY symbol ASC", session["user_id"])
        return render_template("sell.html", all = all)

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        if not request.form.get("amount"):
            return apology("must specify amount", 403)
        elif int(request.form.get("amount")) < 1 and int(request.form.get("amount")) > 10000:
            return apology("cannot comprehend amount", 404)

        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        cash = cash[0]["cash"]

        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash + int(request.form.get("amount")), session["user_id"])
        return redirect("/")

    else:
        return render_template("cash.html")









