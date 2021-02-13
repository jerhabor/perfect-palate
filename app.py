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


@app.route("/recipes/<recipe_id>", methods=["GET", "POST"])
def full_recipe(recipe_id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template("full_recipe.html", recipe=recipe)


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
        return redirect(url_for("profile", username=session["user"]))

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
                    return redirect(url_for(
                        "profile", username=session["user"]))
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


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # The session user's username is retrieved from MongoDB
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    recipes = list(mongo.db.recipes.find(
        {"recipe_by": session["user"]}))
    recipe_by = mongo.db.recipes.find_one(
        {"recipe_by": session["user"]})["recipe_by"]
    return render_template(
        "profile.html", username=username,
        recipes=recipes, recipe_by=recipe_by)


@app.route("/search")
def search():
    query = request.args.get("query", "-minutes -mins")
    recipes = list(mongo.db.recipes.find({"$text": {"$search": query}}))
    return render_template("recipes.html", recipes=recipes)


@app.route("/new_recipe", methods=["GET", "POST"])
def new_recipe():
    if request.method == "POST":
        is_vegetarian = "Yes" if request.form.get(
            "is_vegetarian") == "Yes" else "No"

        # Creating a dictionary for ingredients with 'key:value' pairs
        # being 'ingredient_name:ingredient_amount' respectively.
        ingredient_name = request.form.getlist("ingredient_name")
        ingredient_amount = request.form.getlist("ingredient_amount")
        ingredients = {}
        for index in range(len(ingredient_name)):
            ingredients[ingredient_name[index]] = ingredient_amount[index]

        # Creating a dictionary for the method with 'key:value' pairs
        # being 'step number:step description' respectively.
        method = request.form.getlist("method")
        method_obj = {}
        for element in method:
            # Starting the steps from 1; as by default, the starting
            # index of a list is 0. For the step to be a key of the
            # dictionary, it must be converted to a string.
            method_step = method.index(element) + 1
            method_obj[str(method_step)] = str(element)

        allergens = request.form.get("allergens")
        allergens_list = [x.strip() for x in allergens.split(",")]

        recipe = {
            "cuisine_type": request.form.get("cuisine_type"),
            "recipe_name": request.form.get("recipe_name"),
            "meal_time": request.form.getlist("meal_time"),
            "description": request.form.get("description"),
            "servings": request.form.get("servings"),
            "is_vegetarian": is_vegetarian,
            "cooking_time": request.form.get("cooking_time"),
            "ingredients": ingredients,
            "method": method_obj,
            "allergens": allergens_list,
            "image": request.form.get("image"),
            "video": request.form.get("video"),
            "recipe_by": session["user"]
        }
        mongo.db.recipes.insert_one(recipe)
        flash("Thank you! Your recipe has been successfully added.")
        return redirect(url_for("recipes"))

    return render_template("new_recipe.html")


@app.route("/edit_recipe/<recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    if request.method == "POST":
        is_vegetarian = "Yes" if request.form.get(
            "is_vegetarian") == "Yes" else "No"

        # Creating a dictionary for ingredients with 'key:value' pairs
        # being 'ingredient_name:ingredient_amount' respectively.
        ingredient_name = request.form.getlist("ingredient_name")
        ingredient_amount = request.form.getlist("ingredient_amount")
        ingredients = {}
        for index in range(len(ingredient_name)):
            ingredients[ingredient_name[index]] = ingredient_amount[index]

        # Creating a dictionary for the method with 'key:value' pairs
        # being 'step number:step description' respectively.
        method = request.form.getlist("method")
        method_obj = {}
        for element in method:
            # Starting the steps from 1; as by default, the starting
            # index of a list is 0. For the step to be a key of the
            # dictionary, it must be converted to a string.
            method_step = method.index(element) + 1
            method_obj[str(method_step)] = str(element)

        allergens = request.form.get("allergens")
        allergens_list = [x.strip() for x in allergens.split(",")]

        submit = {
            "cuisine_type": request.form.get("cuisine_type"),
            "recipe_name": request.form.get("recipe_name"),
            "meal_time": request.form.getlist("meal_time"),
            "description": request.form.get("description"),
            "servings": request.form.get("servings"),
            "is_vegetarian": is_vegetarian,
            "cooking_time": request.form.get("cooking_time"),
            "ingredients": ingredients,
            "method": method_obj,
            "allergens": allergens_list,
            "image": request.form.get("image"),
            "video": request.form.get("video"),
            "recipe_by": session["user"]
        }
        mongo.db.recipes.update({"_id": ObjectId(recipe_id)}, submit)
        flash("Recipe Successfully Updated")

    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template("edit_recipe.html", recipe=recipe)


@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({"_id": ObjectId(recipe_id)})
    flash("Recipe Deleted")
    return redirect(url_for("recipes"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)


# Update to debug = False before submission !
