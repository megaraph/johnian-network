''' Generates and confirms user token for email confirmation '''

from itsdangerous import URLSafeTimedSerializer
from flask import current_app

app = current_app

SECRET_KEY = app.config['SECRET_KEY']
SECURITY_PASSWORD_SALT = app.config['SECURITY_PASSWORD_SALT']


def generate_confirmation_token(email):
    '''
    Generates user token by serializing `SECRET_KEY` and returning a dumped
    serializer with the `email` and the `SECURITY_PASSWORD_SALT`
    '''

    serializer = URLSafeTimedSerializer(SECRET_KEY)
    return serializer.dumps(email, salt=SECURITY_PASSWORD_SALT)

def confirm_token(token, expiration=3600):
    '''
    Confirms token by seralizing `SECRET_KEY` and checking it
    with the `token` from the confirmaton link, the `SECURITY_PASSWORD_SALT`
    and the `expiration`. When all those checks out it returns the `email` else
    it returns boolean value of `False` 
    '''

    serializer = URLSafeTimedSerializer(SECRET_KEY)
    try:
        email = serializer.loads(
            token,
            salt=SECURITY_PASSWORD_SALT,
            max_age=expiration
        )
    except:
        return False

    return email
