''' Web app configuration details '''
import os

class Config:
    '''
    Configuration class to run app configuration details
    '''

    # APP INFO
    DEBUG = bool(int(os.environ.get('TJN_DEBUG')))
    SECRET_KEY = os.environ.get('TJN_SECRET_KEY')
    SECURITY_PASSWORD_SALT = os.environ.get('TJN_SECURITY_PASSWORD_SALT')

    # DATABASE INFO
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') if not DEBUG else 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # WHITENOISE / CDN INFO
    WHITENOISE_MAX_AGE = 31536000 if not DEBUG else 0
    CDN = os.environ.get('TJN_CDN')
    STATIC_URL = CDN if not DEBUG else "http://127.0.0.1:5000/"

    # CLOUDINARY INFO
    CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME')
    CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY')
    CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET')

    # SENDINBLUE
    SENDINBLUE_API_KEY = os.environ.get('TJN_SENDINBLUE_API_KEY')
    SENDINBLUE_SEND_MAIL = os.environ.get('TJN_SENDINBLUE_SEND_MAIL')

    #SMTP
    MAIL_SERVER = 'smtp-relay.sendinblue.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'thejohniannetwork@gmail.com'
    MAIL_PASSWORD = os.environ.get('TJN_MAIL_PASSWORD')