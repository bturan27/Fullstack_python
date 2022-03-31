import re
from flask_app import app
from flask import render_template, redirect, request, session, flash

from flask_app.models.show import Show
from flask_app.models.user import User


@app.route("/delete/<int:id>") # Create app route from delete button specifying by id
def delete(id): # Create delete function passing in the id from the app route
    data={ 
        "id" : id
    }
    Show.delete(data) # Pass in delete method from the class in your model file
    return redirect ("/dashboard") # Redirect user back to TV SHOWs page after the delete function intializes
# =======================
# create SHOW routes
# =====================
@app.route("/new")
def new_show():
    if "user_id" not  in session:
        flash("please login or register before entering the site!")
        return redirect("/")

    return render_template("show_new.html")

#checkkkkkkk

@app.route("/new", methods=["POST"])
def add_show():
    # validate form data

    data = {
        "title" : request.form["title"],
        "network" : request.form["network"],
        "release_date" : request.form["release_date"],
        "description" : request.form["description"],
        "user_id" : session["user_id"]
    }

    if not Show.validate_show(data):
        return redirect ("/new")



    #save new show to db
    Show.new_show(data)

    #redirect back to the dashboard page
    return redirect("/dashboard")

#=================
#show one SHOW route
#==============
@app.route("/show/<int:show_id>")
def show_show(show_id):
    if "user_id" not  in session:
        flash("please login or register before entering the site!")
        return redirect("/")
    data_for_user= {
        "id" : session['user_id']
    }
    data_for_show = {
        "id" : show_id 
    }
    user_Current = User.get_by_id(data_for_user)
    show = Show.show_show(data_for_show)
    return render_template("showone.html", show=show, user = user_Current )

##=================================================================================
#edit one tv show route
#================================================================================
@app.route ("/edit/", methods=["POST"])
def update_show():
    data= {
        "title" : request.form["title"],
        "network" : request.form["network"],
        "release_date" : request.form["release_date"],
        "description" : request.form["description"], 
        "user_id" : session["user_id"]
    }
    if not Show.validate_show(data):
        return redirect("/dashboard")
    Show.update_show(data) 
    #pass paintng info to the html
    
    return redirect("/dashboard")


@app.route("/edit/<int:id>")
def edit_show(id):
    data ={
        "id" : id
    }
    show = Show.show_show(data)
    return render_template("show_edit.html",show=show)
    


