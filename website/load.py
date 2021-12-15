''' Loads data to database from a csv file '''

import csv
import ast
import os
from .models import User, Topics
from flask import current_app
from werkzeug.security import generate_password_hash
from . import db


def load_admins():
    ''' Loads admins to database from TJN_ADMINS environement variable '''

    admins_str = os.environ.get('TJN_ADMINS')
    admins_list = ast.literal_eval(admins_str)

    for admin in admins_list:
        email = admin.get('email')
        password = admin.get('password')
        user_tag = admin.get('user_tag')
        profile_pic = admin.get('profile_pic')
        is_teacher = admin.get('is_teacher')

        admin = User.query.filter_by(email=email).first()
        if not admin:
            new_admin = User(
                email=email,
                user_tag=user_tag,
                profile_pic=profile_pic,
                password=generate_password_hash(password, method='sha256'),
                confirmed=True,
                is_admin=False if is_teacher else True,
                is_teacher=bool(is_teacher)
            )
            db.session.add(new_admin)
            db.session.commit()


def load_topics():
    ''' Loads topics to database from topics.csv file '''

    topics_csv = os.path.join(current_app.root_path, 'static/sheets/topics.csv')
    with open(topics_csv, 'r') as topics_file:
        reader = csv.DictReader(topics_file)

        for row in reader:
            topic_address = row['topic_address']
            topic_name = row['topic_name']
            topic_description = row['topic_description']
            topic_image = topic_address + ".png"
            only_students = bool(row['only_students'])

            topic = Topics.query.filter_by(topic_address=topic_address).first()
            if not topic:
                new_topic = Topics(
                    topic_address=topic_address, 
                    topic_name=topic_name, 
                    topic_description=topic_description,
                    topic_image=topic_image,
                    only_students=only_students
                )
                db.session.add(new_topic)
                db.session.commit()
