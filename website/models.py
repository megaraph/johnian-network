'''
DATABASE module
'''

from datetime import datetime
from flask_login import UserMixin
from . import db


class PostLike(db.Model):
    '''
    Stores information for instructions to like a post
    '''
    _tablename_ = 'post_like'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    post_topic = db.Column(db.String(10), nullable=False)


class PostDislike(db.Model):
    '''
    Stores information for instructions to dislike a post
    '''
    _tablename_ = 'post_dislike'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    post_topic = db.Column(db.String(10), nullable=False)


class Posts(db.Model):
    '''
    Stores information for posts
    '''
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(305), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    topic = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    likes = db.relationship('PostLike', backref='post', lazy='dynamic')
    dislikes = db.relationship('PostDislike', backref='post', lazy='dynamic')
    image = db.Column(db.String(180), nullable=True)
    only_students = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"User('{self.title}', '{self.date_posted}')"


class Comment(db.Model):
    '''
    Stores information for comments
    '''
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    topic = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), default=None)
    likes = db.relationship('PostLike', backref='comment', lazy='dynamic')
    dislikes = db.relationship('PostDislike', backref='comment', lazy='dynamic')
    image = db.Column(db.String(180), nullable=True)
    only_students = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"Comment('{self.content}', '{self.date_posted}')"


class User(db.Model, UserMixin):
    '''
    Stores User info
    '''
    id = db.Column(db.Integer, primary_key=True)
    user_tag = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    profile_pic = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(90), nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_teacher = db.Column(db.Boolean, nullable=False, default=False)
    posts = db.relationship('Posts', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)
    liked = db.relationship(
        'PostLike',
        foreign_keys='PostLike.user_id',
        backref='user', lazy='dynamic')
    disliked = db.relationship(
        'PostDislike',
        foreign_keys='PostDislike.user_id',
        backref='user', lazy='dynamic')

    def like_post(self, post, comment=None):
        '''
        Instructions for liking a post
        '''
        if not comment and not self.has_liked_post(post):
            like = PostLike(user_id=self.id, post_id=post.id, post_topic=post.topic)
            db.session.add(like)

        if comment and not self.has_liked_comment(comment):
            like = PostLike(user_id=self.id, comment_id=comment.id, post_topic=comment.topic)
            db.session.add(like)

    def unlike_post(self, post, comment=None):
        '''
        Instructions for unliking a post
        '''
        if not comment and self.has_liked_post(post):
            PostLike.query.filter_by(
                user_id=self.id,
                post_id=post.id,
                post_topic=post.topic).delete()

        if comment and self.has_liked_comment(comment):
            PostLike.query.filter_by(
                user_id=self.id,
                comment_id=comment.id,
                post_topic=comment.topic).delete()

    def has_liked_post(self, post):
        '''
        Confirm if user has liked post
        '''
        return PostLike.query.filter(
            PostLike.user_id == self.id,
            PostLike.post_id == post.id).count() > 0

    def has_liked_comment(self, comment):
        '''
        Confirm if user has liked comment
        '''
        return PostLike.query.filter(
            PostLike.user_id == self.id,
            PostLike.comment_id == comment.id).count() > 0

    def dislike_post(self, post, comment=None):
        '''
        Instructions for disliking a post
        '''
        if not comment and not self.has_disliked_post(post):
            dislike = PostDislike(user_id=self.id, post_id=post.id, post_topic=post.topic)
            db.session.add(dislike)

        if comment and not self.has_disliked_comment(comment):
            dislike = PostDislike(user_id=self.id, comment_id=comment.id, post_topic=comment.topic)
            db.session.add(dislike)

    def undislike_post(self, post, comment=None):
        '''
        Instructions for removing a dislike from a post
        '''
        if not comment and self.has_disliked_post(post):
            PostDislike.query.filter_by(
                user_id=self.id,
                post_id=post.id,
                post_topic=post.topic).delete()

        if comment and self.has_disliked_comment(comment):
            PostDislike.query.filter_by(
                user_id=self.id,
                comment_id=comment.id,
                post_topic=comment.topic).delete()

    def has_disliked_post(self, post):
        '''
        Confirm if user has disliked post
        '''
        return PostDislike.query.filter(
            PostDislike.user_id == self.id,
            PostDislike.post_id == post.id).count() > 0

    def has_disliked_comment(self, comment):
        '''
        Confirm if user has disliked comment
        '''
        return PostDislike.query.filter(
            PostDislike.user_id == self.id,
            PostDislike.comment_id == comment.id).count() > 0

    def clout_rating(self):
        posts = self.posts
        likes = 0
        dislikes = 0
        post_count = 0

        for post in posts:
            likes += post.likes.count()
            dislikes += post.dislikes.count()
            post_count += 1

        if post_count == 0:
            return post_count

        clout_points = likes - dislikes

        return clout_points

    def __repr__(self):
        return f"User('{self.profile_pic}', '{self.user_tag}', '{self.email}')"


class Topics(db.Model):
    '''
    Stores information for the boards/topics
    '''
    id = db.Column(db.Integer, primary_key=True)
    topic_address = db.Column(db.String(10), nullable=False)
    topic_name = db.Column(db.String(40), nullable=False)
    topic_description = db.Column(db.Text, nullable=False)
    topic_image = db.Column(db.String(180), nullable=False)
    only_students = db.Column(db.Boolean, nullable=False, default=False)
