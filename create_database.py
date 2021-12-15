import click
from flask.cli import with_appcontext
from website import db
from app import app

@click.command(name="create_database")
@with_appcontext
def create_database():
    '''Creates app database'''
    db.create_all(app=app)
    print('--- Database Created! ---')


if __name__ == "__main__":
    create_database()
