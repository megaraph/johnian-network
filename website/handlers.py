from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)
def error_404(error):
    error_popper = "Oh no!"
    error_code = "404"
    error_img = error_code
    error_message = "Deadend! Comeback to the homepage and continue where you left off"

    return render_template(
        'error_page.html',
        error_popper=error_popper,
        error_code=error_code,
        error_img=error_img,
        error_message=error_message
    ), 404

@errors.app_errorhandler(403)
def error_403(error):
    error_popper = "Forbidden!"
    error_code = "403"
    error_img = error_code
    error_message = "You stumbled across something you weren’t meant to access. Comeback to the homepage"

    return render_template(
        'error_page.html',
        error_popper=error_popper,
        error_code=error_code,
        error_img=error_img,
        error_message=error_message
    ), 403

@errors.app_errorhandler(405)
def error_405(error):
    error_popper = "Woops!"
    error_code = "405"
    error_img = "403"
    error_message = "You stumbled across something you weren’t meant to access. Comeback to the homepage"

    return render_template(
        'error_page.html',
        error_popper=error_popper,
        error_code=error_code,
        error_img=error_img,
        error_message=error_message
    ), 405

@errors.app_errorhandler(500)
def error_500(error):
    error_popper = "Woops!"
    error_code = "500"
    error_img = error_code
    error_message = "There’s a bug in the system! Comeback to the homepage to continue where you left off"

    return render_template(
        'error_page.html',
        error_popper=error_popper,
        error_code=error_code,
        error_img=error_img,
        error_message=error_message
    ), 500
