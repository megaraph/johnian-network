'''
Module that stores all project/web app decorators
'''
from functools import wraps
from flask import redirect, url_for
from flask_login import current_user

def check_confirmed(func):
    '''
    Decorator that checks if current user is confirmed
    '''
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.confirmed is False:
            return redirect(url_for('auth.unconfirmed'))
        return func(*args, **kwargs)

    return decorated_function
