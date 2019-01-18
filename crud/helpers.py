from flask import render_template
#from functools import wraps
from config import Constants

def apology(message, code=400):
    """Renders message as an apology to user."""
    return render_template("apology.html", top=code, bottom=message), code

def make_public(function):
    ''' Decorator to make only public attributes visible '''
    def wrap(*args, **kwargs):
        instance = function(*args, **kwargs)
        user_dct={}
        for attr in Constants.USER_ATTR:
            if attr=='date_of_birth':
                user_dct[attr]=str(getattr(instance, attr)).split()[0]
            else:
                user_dct[attr] = getattr(instance, attr)
        return user_dct
    return wrap

