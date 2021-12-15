'''
This python file is responsible for the interactivity of user accounts that
is unique to each user.
'''

from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from email_validator import validate_email
from . import db
from .models import User

user_account = Blueprint('user_account', __name__)

@user_account.route('/account')
@login_required
def account():
    ''' This function returns the home page or the page where you get to choose the boards '''

    image_file = current_user.profile_pic
    clout_rating = current_user.clout_rating()

    return render_template(
        'account.html',
        user=current_user,
        image_file=image_file,
        clout_rating=clout_rating
    )


def send_reset_email(email):
    ''' Sends reset token to user's email via smtp server '''

    from .token import generate_confirmation_token
    token = generate_confirmation_token(email)
    confirm_url = url_for('user_account.confirm_change_password', token=token, _external=True)

    from .email import send_email
    subject = "[IMPORTANT] Change password instructions"
    html = render_template(
        'password_email.html',
        confirm_url=confirm_url,
        user_email=email
    )
    send_email(email, subject, html)


@user_account.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    ''' This function returns the instructions for changing the current user's password '''

    if request.method == 'POST':
        email = request.form.get('email')

        try:
            validate_email(email)
        except:
            flash('Enter a valid email address', category='email-error')
            return redirect(request.referrer)

        user = User.query.filter_by(email=email).first()
        if user is None:
            flash("Couldn't find email in database", category='email-error')
            return redirect(request.referrer)

        send_reset_email(user.email)
        flash('An email has been sent to you with instructions to reset your password', category='info')

        return redirect(url_for('auth.login'))

    return render_template('forgot_password.html')


@user_account.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    ''' This function returns the instructions for changing the current user's password '''

    if not current_user.is_authenticated:
        return redirect(url_for('forgot_password'))

    send_reset_email(current_user.email)
    flash('An email has been sent to you with instructions to reset your password', category='info')

    return redirect(request.referrer)


@user_account.route('/confirm_change_password/<token>', methods=['GET', 'POST'])
def confirm_change_password(token):
    ''' This function returns the instructions for confirming current user's change password token '''

    from .token import confirm_token

    try:
        email = confirm_token(token)
    except:
        return False

    user = User.query.filter_by(email=email).first()
    if user is None:
        flash('Probably an invalid or expired token', category='info')
        return render_template('user_not_found.html')

    if request.method == 'POST':
        new_password = request.form.get('newPassword')
        confirm_new_password = request.form.get('confirmPassword')

        if len(new_password) < 7 or len(new_password) > 18:
            flash('Password must be greater than 7 characters and less than 18 characters',
                category='password-error')
            return redirect(request.referrer)
        
        if len(confirm_new_password) < 1 or new_password != confirm_new_password:
            flash('Passwords do not match', category='password_confirmation-error')
            return redirect(request.referrer)

        user.password = generate_password_hash(new_password, method='sha256')
        db.session.commit()

        flash('Your password has been changed, login to continue', category='info')
        return redirect(url_for('auth.logout'))

    return render_template('change_password.html')


@user_account.route('/compare_with/<int:user_id>')
@login_required
def compare_with(user_id):
    ''' Returns a page to compare current user's clout rating with another user '''

    compare_with_user = User.query.get_or_404(user_id)

    compare_with_user_image = compare_with_user.profile_pic
    current_user_image = current_user.profile_pic

    compare_clout_rating = compare_with_user.clout_rating()
    current_clout_rating = current_user.clout_rating()

    return render_template(
        'compare_with.html',
        compare_with_user = compare_with_user,
        compare_with_user_image = compare_with_user_image,
        current_user_image = current_user_image,
        compare_clout_rating = compare_clout_rating,
        current_clout_rating = current_clout_rating
    )
