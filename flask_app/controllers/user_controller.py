from flask_app import app
from flask import render_template, redirect, request, session, flash 

from flask_app.models.user import User
from flask_app.models.show import Show
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html") 

#===========================================
#register /login routes
#==================================================

@app.route("/register", methods=["POST"])
def register():
    print(request.form)
    # 1 validating form information
    data= {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "password" : request.form["password"],
        "pass_conf" : request.form["pass_conf"]
    }
    if not User.validate_register(data):
        return redirect("/")


    #2 bcrypt password
    data["password"]= bcrypt.generate_password_hash(request.form['password'])



    #3 save new owner to db
    new_user_id= User.create_user(data)



    #4 enter owner id into session and redirect to dashboard
    session["user_id"] = new_user_id
    return redirect("/dashboard")



@app.route("/login", methods=["POST"])
def login():
    #this function is receiving data from form, specifically from login form
    #1 validate login info
    data = {
        "email" : request.form["email"],
        "password" : request.form["password"]
    }
    if not User.validate_login(data):
        return redirect("/") 


    #2 query for User info based on email
    user = User.get_by_email(data)
 

    #3 put user id into session and redirect to dashboard
    session["user_id"] = user.id
    return redirect("/dashboard") 

#=========================
#render dashboard
#===============

@app.route("/dashboard")
def show():


    if "user_id" not in session:
        flash("please login or register before entering the site!")
        return redirect("/")



    data= {
        "id" : session["user_id"]
    }
    user= User.get_by_id(data)
    all_shows= Show.get_all()

    return render_template("dashboard.html", user=user, all_shows =all_shows)


#=========================
#logout route
#========================

@app.route("/logout")
def logout():
    session.clear()
    flash("succesfully logged out!")
    return redirect("/")

