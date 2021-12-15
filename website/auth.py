''' This python file is responsible for the backend/script of the login, sign up, and logout page '''

from random import randint
from email_validator import validate_email
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .load import load_admins, load_topics
from .models import User
from . import db

auth = Blueprint('auth', __name__)


@auth.before_app_first_request
def load_admins_path():
    ''' Loads admins and topics from load_admins and load_topics function '''

    load_admins()
    load_topics()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    '''
    ## Sign-up path:
    - View: sign-up.html
    1. Performs exceptions to provided form data:
            - makes sure inputted email is valid
            - makes sure account doesn't already exist
            - makes sure email is not an injection attack
            - makes sure inputted email is an SJI email
            - passwords are the right length and match each other
    2. Gives users:
            - 4 digit random tag
            - is_teacher status from .user_list and rejects emails
              not found in the list
            - random profile picture
    3. Creates new user from given data and inserted into database
    4. Sends user a confirmation email
    5. Logs in new user and redirects to unconfirmed page
    '''

    if current_user.is_authenticated:
        return redirect(url_for('boards.board_choose'))

    if request.method == 'POST':
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        try:
            validate_email(email)
        except:
            flash('Enter a valid email address', category='email-error')
            return redirect(request.referrer)

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Account already exists.', category='signup-error')
        elif len(email) > 32:
            flash('Email exceeded 32 characters limit', category='email-error')
        elif not email.endswith('@sji.edu.ph'):
            flash('Enter email address that ends with "@sji.edu.ph"', category='email-error')
        elif password1 is None or len(password1) < 7 or len(password1) > 18:
            flash('Password must be at least 7 characters and less than 18 characters',
                category='password-error')
        elif password2 is None or password1 != password2:
            flash('Passwords do not match', category='password_confirmation-error')
        else:
            while True:
                random_tag = randint(1000, 9999)
                tag = User.query.filter_by(user_tag=random_tag).first()
                if tag is None:
                    break

            from .user_list import users
            try:
                is_teacher = users[email]
            except:
                flash('Email not allowed. Email us if you think there is a problem.', 
                    category='email-error')
                return redirect(request.referrer)

            profile_pic = f'default{randint(1, 4)}.png'
            
            new_user = User(
                user_tag=random_tag,
                email=email,
                profile_pic=profile_pic,
                password=generate_password_hash(password1, method='sha256'),
                confirmed=False,
                is_admin=False,
                is_teacher=is_teacher
            )

            db.session.add(new_user)
            db.session.commit()

            from .token import generate_confirmation_token
            token = generate_confirmation_token(new_user.email)
            confirm_url = url_for('auth.confirm_email', token=token, _external=True)

            from .email import send_email
            subject = "[IMPORTANT] Please confirm your email"
            html = render_template(
                'activate.html',
                confirm_url=confirm_url,
                user_email=new_user.email
            )
            send_email(new_user.email, subject, html)

            login_user(new_user)
            return redirect(url_for('auth.unconfirmed'))

    return render_template("sign-up.html")


@auth.route('/confirm/<token>')
def confirm_email(token):
    ''' Used to confirm the confirmation link and login the user '''

    from .token import confirm_token
    try:
        email = confirm_token(token)
    except:
        flash('Token cannot be processed, try again', 'other-danger')
        return redirect(url_for('auth.unconfirmed'))

    user = User.query.filter_by(email=email).first()
    if user is None:
        return render_template('user_not_found.html')

    if user.confirmed:
        flash('Account already confirmed. Please login to continue', category='email-error')
        return redirect(url_for('auth.login'))
    else:
        user.confirmed = True
        db.session.commit()
        flash('Account succesfully created. Welcome to the Johnian Network!',
                    category='auth-success')
    return redirect(url_for('boards.board_choose'))


@auth.route('/unconfirmed')
@login_required
def unconfirmed():
    '''
    Redirects user to the unconfirmed page if user has not confirmed
    their email. Otherwise, it redirects them to the homepage.
    '''

    if current_user.confirmed:
        return redirect(url_for('boards.board_choose'))

    return render_template(
        'unconfirmed.html',
        current_user=current_user.email
    )


@auth.route('/resend')
@login_required
def resend_confirmation():
    ''' Regenerates a new confirmation link to be resent to the current_user's email. '''

    from .token import generate_confirmation_token
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)

    from .email import send_email
    subject = "[IMPORTANT] Please confirm your email"
    html = render_template(
        'activate.html',
        confirm_url=confirm_url,
        user_email=current_user.email
    )
    send_email(current_user.email, subject, html)

    flash('A new confirmation email has been sent.', 'other-success')
    return redirect(url_for('auth.unconfirmed'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    '''
    ## Login path:
    - View: login.html
    1. Performs exceptions to provided form data:
            - makes sure inputted email is valid
            - makes sure email is not an injection attack
            - makes sure inputted email is an SJI email
            - makes sure password is the right length
    2. Makes sure account exists
    3. Checks inputted password and if matches user's password, it logs 
       user in and remembers user if checkbox has been checked
    '''

    if current_user.is_authenticated:
        return redirect(url_for('boards.board_choose'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        checkbox = request.form.get('checkbox')

        if email is None or len(email) > 36:
            flash('Enter valid email', category='email-error')
        elif not email.endswith('@sji.edu.ph'):
            flash('Enter email address that ends with "@sji.edu.ph"', category='email-error')
        elif password is None or len(password) < 7 or len(password) > 18:
            flash('Password must be greater than 7 characters and less than 18 characters',
                category='password-error')
        else:
            user = User.query.filter_by(email=email).first()
            if user:
                if check_password_hash(user.password, password):
                        login_user(user, remember=checkbox)
                        flash('Login Success', category='auth-success')
                        return redirect(url_for('boards.board_choose'))
                else:
                    flash('Incorrect password. Check email address and password',
                        category='password-error')
            else:
                flash("Couldn't find email and password.", category='email-error')

    return render_template(
        "login.html",
        user=current_user
    )

@auth.route('/logout')
@login_required
def logout():
    ''' Logs out a user and redirects back to login page '''

    logout_user()
    return redirect(url_for('auth.login'))
