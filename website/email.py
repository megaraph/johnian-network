''' Module for sending email confirmation links via email '''

from __future__ import print_function
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

from flask_mail import Message
from flask import current_app
from . import mail

app = current_app

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = app.config['SENDINBLUE_API_KEY']


def send_email(to_email, subject, template):
    '''
    Sends an email message via sendinblue api
    '''
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    sender = {
        "name":"Johnian Network", 
        "email":app.config['SENDINBLUE_SEND_MAIL']
    }

    mail_name, _ = to_email.split("@")
    first_name, last_name = [name.capitalize() for name in mail_name.split(".")]
    to_name = f"{first_name} {last_name}"

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": to_email, "name": to_name}], 
        html_content=template, 
        sender=sender, 
        subject=subject
    )

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(f"\nAPI RESPONSE: {api_response}\n")
    except ApiException as e:
        print(f"Exception when calling SMTPApi->send_transac_email: {e}\n")

def send_email_smtp(to_email, subject, template):
    '''
    Sends an email message via smtp.gmail.com server to 
    the given user's email
    '''
    msg = Message(subject, sender=app.config['MAIL_USERNAME'],
        recipients=[to_email],
    )
    msg.html = template

    mail.send(msg)
    print("Mail sent")
