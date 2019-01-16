from werkzeug.exceptions import default_exceptions
from flask import redirect, render_template, request, url_for
import datetime

from user import User
from config import db, app, Constants
from helpers import apology

#init db
db.create_all()

#@app.route("/index", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def index():
    ''' Main page with a list of users in db'''
    page = request.args.get('page', 1, type=int)
    list_of_users = User().get_list(page=page, users_per_page=Constants.USERS_PER_PAGE)
    next_url = url_for('index', page=list_of_users.next_num) if list_of_users.has_next else None
    prev_url = url_for('index', page=list_of_users.prev_num) if list_of_users.has_prev else None
    return render_template("index.html", users=list_of_users.items,
                          next_url=next_url, prev_url=prev_url)

@app.route("/add", methods=["GET", "POST"])
def add_user():
    """Add user"""
    # User reached route via POST
    if request.method == "POST":
        try:
            result = User().add(name=request.form.get("name"),
                                    date_of_birth=datetime.datetime.strptime(request.form.get("date_of_birth"), '%Y-%m-%d'),
                                    email=request.form.get("email")
                                    )
        except AssertionError as err:
            return apology(err,400)
    # User reached route via GET
    else:
        return render_template("index.html")
   # Redirect to home page
    return redirect("/")


@app.route("/get", methods = ['GET'])
def get_user():
    ''' Forward main page to user_info page'''

    email = request.args['email']
    user = User().get_user('email', email)

    return render_template('user_info.html', user=user)


@app.route("/update", methods = ['GET', 'POST'])
def update_user():
    ''' Update user's info'''

    old_email = request.args['email']
    user = User().get_user('email', old_email)

     # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        result = User().update(user_id=user.id,
                                       name=request.form.get("username"),
                                       date_of_birth=request.form.get("date of birth"),
                                       email=request.form.get("email")
                                      )
    return render_template('user_info.html', user=result)


@app.route("/remove", methods = ['GET'])
def remove_user():
    ''' Remove user and forward to main page'''

    email = request.args['email']
    result = User().remove(email)
    return render_template('index.html')


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
