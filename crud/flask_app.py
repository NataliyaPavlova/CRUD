from werkzeug.exceptions import default_exceptions
from flask import redirect, render_template, request

from user_repository import UserRepository
from config import db, app
from helpers import apology

#init db
db.create_all()

@app.route("/index", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def index():
    ''' Main page with a list of users in db'''
    page = request.args.get('page', 1, type=int)
    list_of_users = UserRepository.get_list(page, app.config['USERS_PER_PAGE'])
    next_url = url_for('explore', page=list_of_users.next_num) if list_of_users.has_next else None
    prev_url = url_for('explore', page=list_of_users.prev_num) if list_of_users.has_prev else None
    return render_template("index.html", users=list_of_users.items,
                          next_url=next_url, prev_url=prev_url)

@app.route("/add", methods=["GET", "POST"])
def add_user():
    """Add user"""

    # User reached route via POST
    if request.method == "POST":
        result = UserRepository.add(name=request.form.get("username"),
                                    date_of_birth=request.form.get("date of birth"),
                                    email=request.form.get("email")
                                    )
    # User reached route via GET
    else:
        return redirect("/")
   # Redirect to home page
    return redirect("/")


@app.route("/get", methods = ['GET'])
def get_user():
    ''' Forward main page to user_info page'''

    email = request.args['email']
    user = UserRepository.get_user(email)

    return render_template('/user_info.html', user=user)


@app.route("/update", methods = ['GET', 'POST'])
def update_user():
    ''' Update user's info'''

    old_email = request.args['email']
    user = UserRepository.get_user(old_email)

     # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        result = UserRepository.update(user_id=user.id,
                                       name=request.form.get("username"),
                                       date_of_birth=request.form.get("date of birth"),
                                       email=request.form.get("email")
                                      )
    return render_template('/user_info.html', user=result)


@app.route("/remove", methods = ['GET'])
def remove_user():
    ''' Remove user and forward to main page'''

    email = request.args['email']
    result = UserRepository.remove(email)
    return render_template('/')


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
