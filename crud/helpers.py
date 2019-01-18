from flask import render_template
#from functools import wraps
from config import Constants

def apology(message, code=400):
    """Renders message as an apology to user."""
    return render_template("apology.html", top=code, bottom=message), code

def make_public(function):
    ''' Decorator to make only public attributes visible '''
    def wrap(*args, **kwargs):
        instances_list = [function(*args, **kwargs)]
        result=[]
        for instance in instances_list:
            user_dct={}
            for attr in Constants.USER_ATTR:
                user_dct[attr] = getattr(instance.__class__, attr)
            result.append(user_dct)
        return result
    return wrap
