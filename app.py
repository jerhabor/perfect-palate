import os
from flask import (
    Flask, flash, render_template, 
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/recipes")
def recipes():
    recipes = list(mongo.db.recipes.find())
    return render_template("recipes.html", recipes=recipes)


@app.route("/recipes/<recipe_name>")
def full_recipe(recipe_name):
    info = {}
    recipes = list(mongo.db.recipes.find())
    for obj in recipes:
        if obj["recipe_name"] == recipe_name:
            info = obj
    return render_template("full_recipe.html", info=info)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Checking if username already exists in the DB as lowercase:
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        # Checking if email already exists in the DB:
        existing_email = mongo.db.users.find_one(
            {"email": request.form.get("email")})

        if existing_email:
            flash("Email already exists")
            return redirect(url_for("register"))

        # If username does not exist, then store in db:
        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "email": request.form.get("email")
        }
        mongo.db.users.insert_one(register)

        # After clicking register, user will now be in session:
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful")
        return redirect(url_for("recipes", username=session["user"]))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Checking if username already exists in the DB as lowercase:
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # Checking if the hashed password matches the user's input:
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    flash("Hello, {}".format(request.form.get("username")))
                    return redirect(url_for(
                        "recipes", username=session["user"]))
            else:
                # If the invalid password is incorrect then alert user.
                # For security reasons message displays either username
                # or password is incorrect. This minimises brute-forcing.
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # If the username does not exist then display the same message
            # as if the password was incorrect.
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    # Remove user from the browser session cookies:
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)


# Update to debug = False before submission !
