''' This python file is responsible for the interactivity of each board of the web app '''

import os
import secrets
import json
from datetime import datetime
from flask import Blueprint, render_template, request, url_for, redirect, abort, flash, current_app, jsonify
from flask_login import login_required, current_user
from flask_cors import cross_origin
from cloudinary import uploader
from .decorators import check_confirmed
from .models import User, Topics, Posts, PostLike, PostDislike, Comment
from . import db

boards = Blueprint('boards', __name__)
ALLOWED_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.gif']

@boards.route('/')
@login_required
@check_confirmed
def board_choose():
    ''' Returns the home page (page where you get to choose topics) '''

    # if current user is not a teacher, it returns all the topics
    # otherwise, it does not return "only students" topics
    if not current_user.is_teacher:
        topics = Topics.query
    else:
        topics = Topics.query.filter_by(only_students=False)

    return render_template(
        'boards_choose.html', 
        topics=topics
    )


@boards.route('/boards/<topic_address>')
@login_required
@check_confirmed
def board_choice(topic_address):
    ''' Returns the user's selected topic's page '''

    topic = Topics.query.filter_by(topic_address=topic_address).first_or_404()
    if current_user.is_teacher and topic.only_students:
        abort(403)

    # if current user is not a teacher, every post of the selected topic is returned 
    # but if current user is a teacher then it does not return "only students" posts,
    # also since we're paginating, each page only has 30 posts
    page = request.args.get('page', 1, type=int)
    if not current_user.is_teacher:
        posts = Posts.query.filter_by(topic=topic_address).order_by(Posts.date_posted.desc()).paginate(page=page, per_page=30)
    else:
        posts = Posts.query.filter_by(topic=topic_address, only_students=False).order_by(Posts.date_posted.desc()).paginate(page=page, per_page=30)

    comments = Comment()
    board_likes = PostLike.query.filter_by(post_topic=topic_address).count()
    board_dislikes = PostDislike.query.filter_by(post_topic=topic_address).count()
    time_now = datetime.strptime(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "%Y-%m-%d %H:%M:%S")

    return render_template(
        'topic_choice.html',
        posts=posts,
        topic=topic,
        time_now=time_now,
        board_likes=board_likes,
        board_dislikes=board_dislikes,
        comments=comments
    )


def save_image(image):
    ''' 
    Saves `image` in `static/post_images` with a random 16 character name and
    uploads it to Cloudinary then unlinks it from `static/post_images`, returns
    string representation of dict `cloud_file`
    '''

    random_name = secrets.token_hex(8)
    _, f_extension = os.path.splitext(image.filename)
    image_name = random_name + f_extension
    image_path = os.path.join(current_app.root_path, 'static/post_images', image_name)
    image.save(image_path)

    try:
        upload_result = uploader.upload(image_path, folder='johnian-net')
        cloud_file = {
            'id': upload_result['public_id'],
            'ext': upload_result['format'],
            'resource_type': upload_result['resource_type'],
            'type': upload_result['type'],
            'version': upload_result['version'],
            'original_filename': upload_result['original_filename']
        }
    except:
        pass

    os.unlink(image_path)
    return json.dumps(cloud_file)


def delete_image(image):
    ''' Deletes `image` from Cloudinary and returns image's name '''
    post_image = json.loads(image)
    result = uploader.destroy(post_image['id'])

    print(result)
    return image


@boards.route('/boards/<topic_address>/post/new', methods=['GET', 'POST'])
@cross_origin()
@login_required
@check_confirmed
def new_post(topic_address):
    '''
    ## New post path:
    - View: create_post.html
    1. First of all, makes sure topic exists
    2. If an image is attached, makes sure that it has an appropriate extension,
       once that checks out, it gets saved
    3. Makes sure the post has a title
    4. Inserts new post to db and if topic is only for students or if the user 
       tags the post as only students, the post gets an only_students tag
    '''

    topic = Topics.query.filter_by(topic_address=topic_address).first_or_404()

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        only_students = bool(request.form.get('only_students'))
        image = request.files['image']
        image_file = None

        if image:
            _, f_extension = os.path.splitext(image.filename)
            if f_extension in ALLOWED_EXTENSIONS:
                try:
                    image_file = save_image(image)
                except:
                    flash('Error uploading image. Try another image.', category='file-type-error')
                    return redirect(url_for(
                        'boards.new_post',
                        topic_address=topic_address
                    ))
            else:
                flash('Only images can be accepted', category='file-type-error')
                return redirect(url_for(
                    'boards.new_post',
                    topic_address=topic_address
                ))

        # the split method is there to check if the title is just
        # filled with whitespace or not, example: title = '      '
        # title.split() == [] which is less than 1
        if len(title.split()) < 1:
            flash('Your post needs a title', category='post-title-error')
            return redirect(url_for(
                'boards.new_post',
                topic_address=topic_address
            ))

        post = Posts(
            title=title,
            content=content,
            author=current_user,
            topic=topic_address,
            user_id=current_user.id,
            image=image_file,
            only_students=only_students
        )

        if topic.only_students:
            post.only_students = True

        db.session.add(post)
        db.session.commit()
        flash(f'Your post has been posted on {topic.topic_name}!', category='post-success')

        return redirect(url_for(
            'boards.selected_post',
            topic_address=topic_address,
            post_id=post.id
        ))

    return render_template(
        'create_post.html',
        topic=topic
    )


@boards.route('/boards/<topic_address>/post/<int:post_id>')
@login_required
@check_confirmed
def selected_post(topic_address, post_id):
    ''' Returns the user's selected post's page '''

    post = Posts.query.filter_by(id=post_id, topic=topic_address).first_or_404()
    topic = Topics.query.filter_by(topic_address=topic_address).first()

    if current_user.is_teacher and post.only_students:
        abort(403)

    board_likes = PostLike.query.filter_by(post_topic=topic_address).count()
    board_dislikes = PostDislike.query.filter_by(post_topic=topic_address).count()
    time_now = datetime.strptime(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "%Y-%m-%d %H:%M:%S")

    page = request.args.get('page', 1, type=int)
    comments = Comment.query.filter_by(post_id=post_id, comment_id=None).order_by(Comment.date_posted.desc()).paginate(page=page, per_page=15)
    comment_count = Comment.query.filter_by(post_id=post_id, comment_id=None).count()

    return render_template(
        'post.html',
        post=post,
        topic=topic,
        time_now=time_now,
        board_likes=board_likes,
        board_dislikes=board_dislikes,
        comments=comments, 
        comment_count=comment_count
    )


@boards.route('/<int:post_id>/edit/remove_image', methods=['GET', 'POST'])
@cross_origin()
@login_required
@check_confirmed
def remove_image(post_id):
    ''' Removes post's current saved image when editing the post '''

    post = Posts.query.get_or_404(post_id)
    delete_image(post.image)
    post.image = None
    db.session.commit()

    return redirect(url_for(
        'boards.edit_post',
        topic_address=post.topic,
        post_id=post.id
    ))


@boards.route('/boards/<topic_address>/post/<int:post_id>/edit', methods=['GET', 'POST'])
@cross_origin()
@login_required
@check_confirmed
def edit_post(topic_address, post_id):
    '''
    ## Edit post path:
    - View: edit_post.html
    1. First of all, makes sure current path exists and current user is
       either the author of the post or an admin.
    2. If an image is attached, makes sure that it has an appropriate extension and does
       not have another image currently saved, once that checks out, it gets saved
    3. Makes sure the post has a title
    4. Updates changes to db
    '''

    post = Posts.query.filter_by(id=post_id, topic=topic_address).first_or_404()
    topic = Topics.query.filter_by(topic_address=topic_address).first()

    if post.author != current_user and not current_user.is_admin:
        abort(403)

    if request.method == 'POST':
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        post.only_students = bool(request.form.get('only_students'))
        image = request.files['image']

        if image:
            _, f_extension = os.path.splitext(image.filename)
            if f_extension in ALLOWED_EXTENSIONS:
                try:
                    delete_image(post.image)
                    post.image = save_image(image)
                except:
                    post.image = save_image(image)
            else:
                flash('Only images can be accepted', category='file-type-error')
                return redirect(url_for(
                    'boards.edit_post',
                    topic_address=topic_address,
                    post_id=post_id
                ))

        # the split method is there to check if the title is just filled 
        # with whitespace or not, example: post.title = '      '
        # post.title.split() == [] which is less than 1
        if len(post.title.split()) < 1:
            flash('Your post needs a title', category='post-title-error')
            return redirect(url_for(
                    'boards.edit_post',
                    topic_address=topic_address,
                    post_id=post_id
                ))

        db.session.commit()
        flash(f'Your post has been edited on {topic.topic_name}!', category='post-success')

        return redirect(url_for(
            'boards.selected_post',
            topic_address=topic_address,
            post_id=post_id
        ))

    return render_template(
        'edit_post.html',
        topic=topic,
        post=post
    )


@boards.route('/boards/<topic_address>/post/<int:post_id>/delete', methods=['POST'])
@cross_origin()
@login_required
@check_confirmed
def delete_post(topic_address, post_id):
    '''
    ## Delete post path:
    - View: redirects to board_choice
    1. First of all, makes sure current path exists and current user is
       either the author of the post or an admin.
    2. Deletes post's likes/dislikes
    3. If an image is attached, the image gets deleted
    4. Deletes all post's comments, the comments' likes/dislikes, and their images
    5. Post is deleted from db
    '''

    post = Posts.query.filter_by(id=post_id, topic=topic_address).first_or_404()
    topic = Topics.query.filter_by(topic_address=topic_address).first()

    if post.author != current_user and not current_user.is_admin:
        abort(403)

    if request.method == 'POST':
        PostLike.query.filter_by(post_id=post.id).delete()
        PostDislike.query.filter_by(post_id=post.id).delete()
        if post.image:
            delete_image(post.image)

        comments = Comment.query.filter_by(post_id=post.id)
        for comment in comments:
            PostLike.query.filter_by(comment_id=comment.id).delete()
            PostDislike.query.filter_by(comment_id=comment.id).delete()
            if comment.image:
                delete_image(comment.image)
        comments.delete()

        db.session.delete(post)
        db.session.commit()
        flash(f'Your post has been deleted from {topic.topic_name}!', category='post-success')

        return redirect(url_for(
            'boards.board_choice',
            topic_address=topic_address
        ))


@boards.route('/boards/<topic_address>/post/<int:post_id>/comment/<int:comment_id>', methods=['GET', 'POST'])
@cross_origin()
@login_required
@check_confirmed
def create_comment(topic_address, post_id, comment_id):
    '''
    ## Create comment path:
    - View: current selected post
    1. First of all, makes sure current path exists
    2. If an image is attached, makes sure that it has an appropriate extension,
       once that checks out, it gets saved
    3. Makes sure the new comment has content
    4. Checks if new comment is being commented under a post or under another comment. If under
       another comment, the new comment's comment_id is the original comment's id
    5. Inserts new comment to db and gets an only_students tag if post
       is also only for students
    '''

    post = Posts.query.filter_by(id=post_id, topic=topic_address).first_or_404()

    if request.method == 'POST':
        content = request.form.get('content')
        only_students = bool(request.form.get('only_students'))
        image = None
        image_file = None
        
        try:
            image = request.files['image']
        except:
            pass

        if image:
            _, f_extension = os.path.splitext(image.filename)
            if f_extension in ALLOWED_EXTENSIONS:
                image_file = save_image(image)
            else:
                flash('Only images can be accepted', category='file-type-error')
                return redirect(url_for(
                    'boards.selected_post',
                    topic_address=topic_address,
                    post_id=post_id
                ))

        # the split method is there to check if the content is just filled with whitespace or not,
        # example: content = '          '; content.split() == [] which is less than 1, also the
        # reason why it's inside a try except block is because the form sometimes disappears so
        # an AttributeError will be raised since content will be None and the split method
        # won't work on something that is None
        try:
            if len(content.split()) < 1:
                raise AttributeError
        except:
            flash('Your comment needs content', category='post-content-error')
            return redirect(request.referrer)

        new_comment = Comment(
            content=content,
            topic=topic_address,
            user_id=current_user.id,
            author=current_user,
            post_id=post_id,
            comment_id=None,
            image=image_file,
            only_students=post.only_students
        )

        # if there is an original comment (new comment being commented under another comment)
        original_comment = Comment.query.filter_by(id=comment_id, post_id=post.id).first()
        if original_comment:
            new_comment.post_id = original_comment.post_id
            new_comment.comment_id = original_comment.id

        db.session.add(new_comment)
        db.session.commit()
        flash(f'Your comment has been posted on Anonymous#{post.author.user_tag}\'s post!',
            category='post-success')

        return redirect(url_for(
            'boards.selected_comment',
            topic_address=topic_address,
            post_id=post_id,
            comment_id=new_comment.id
        ))


@boards.route('/boards/<topic_address>/post/<int:post_id>/<int:comment_id>')
@login_required
@check_confirmed
def selected_comment(topic_address, post_id, comment_id):
    ''' Returns the user's selected comment's page '''

    comment = Comment.query.filter_by(id=comment_id, topic=topic_address, post_id=post_id).first_or_404()
    post = Posts.query.get_or_404(comment.post_id)

    if current_user.is_teacher and post.only_students:
        abort(403)

    topic = Topics.query.filter_by(topic_address=comment.topic).first()
    board_likes = PostLike.query.filter_by(post_topic=comment.topic).count()
    board_dislikes = PostDislike.query.filter_by(post_topic=comment.topic).count()
    time_now = datetime.strptime(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "%Y-%m-%d %H:%M:%S")

    page = request.args.get('page', 1, type=int)
    comments = Comment.query.filter_by(comment_id=comment.id).order_by(Comment.date_posted.desc()).paginate(page=page, per_page=15)
    reply_count = Comment.query.filter_by(comment_id=comment.id).count()

    return render_template(
        'comment.html',
        post=post,
        comment=comment,
        topic=topic,
        time_now=time_now,
        board_likes=board_likes,
        board_dislikes=board_dislikes,
        comments=comments,
        reply_count=reply_count
    )


@boards.route('/<int:comment_id>/edit/remove_comment_image', methods=['GET', 'POST'])
@cross_origin()
@login_required
@check_confirmed
def remove_comment_image(comment_id):
    ''' Removes comment's current saved image when editing the comment '''

    comment = Comment.query.get_or_404(comment_id)
    delete_image(comment.image)
    comment.image = None
    db.session.commit()

    return redirect(url_for(
        'boards.edit_comment',
        topic_address=comment.topic,
        post_id=comment.post_id,
        comment_id=comment.id
    ))


@boards.route('/boards/<topic_address>/post/<int:post_id>/<int:comment_id>/edit', methods=['GET', 'POST'])
@cross_origin()
@login_required
@check_confirmed
def edit_comment(topic_address, post_id, comment_id):
    '''
    ## Edit comment path:
    - View: edit_comment.html
    1. First of all, makes sure current path exists and current user is
       either the author of the comment or an admin.
    2. If an image is attached, makes sure that it has an appropriate extension and does
       not have another image currently saved, once that checks out, it gets saved
    3. Makes sure the post has a title
    4. Updates changes to db
    '''

    post = Posts.query.filter_by(id=post_id, topic=topic_address).first_or_404()
    comment = Comment.query.filter_by(id=comment_id, topic=topic_address, post_id=post_id).first_or_404()
    topic = Topics.query.filter_by(topic_address=topic_address).first()

    if comment.author != current_user and not current_user.is_admin:
        abort(403)

    if request.method == 'POST':
        comment.content = request.form.get('content')
        comment.only_students = bool(request.form.get('only_students'))
        image = request.files['image']

        if image:
            _, f_extension = os.path.splitext(image.filename)
            if f_extension in ALLOWED_EXTENSIONS:
                try:
                    delete_image(comment.image)
                    comment.image = save_image(image)
                except:
                    comment.image = save_image(image)
            else:
                flash('Only images can be accepted', category='file-type-error')
                return redirect(url_for(
                    'boards.edit_comment',
                    topic_address=topic_address, 
                    post_id=post_id,
                    comment_id=comment_id
                ))

        # the split method is there to check if the content is just filled 
        # with whitespace or not, example: content = '          '
        # content.split() == [] which is less than 1
        if len(comment.content.split()) < 1:
            flash('Your comment needs content', category='post-content-error')
            return redirect(url_for(
                'boards.edit_comment',
                topic_address=topic_address, 
                post_id=post_id,
                comment_id=comment_id
            ))

        db.session.commit()
        flash('Your comment has been edited!', category='post-success')

        return redirect(url_for(
            'boards.selected_comment',
            topic_address=topic_address,
            post_id=post_id,
            comment_id=comment_id
        ))

    return render_template(
        'edit_comment.html',
        topic=topic,
        comment=comment,
        post=post
    )


@boards.route('/boards/<topic_address>/post/<int:post_id>/<int:comment_id>/delete', methods=['POST'])
@cross_origin()
@login_required
@check_confirmed
def delete_comment(topic_address, post_id, comment_id):
    '''
    ## Delete comment path:
    - View: redirects to selected_post
    1. First of all, makes sure current path exists and current user is
       either the author of the comment or an admin.
    2. Deletes comment, its replies, likes/dislikes, and images
    '''

    def delete(comment):
        comment_replies = Comment.query.filter_by(comment_id=comment.id).all()
        if comment_replies:
            # for each of the parent's children
            for comment_reply in comment_replies:
                comment_replies = Comment.query.filter_by(comment_id=comment_reply.id).all()
                current_comment = comment_reply

                # get the very bottom node which will be stored in current_comment
                while comment_replies:
                    current_comment = comment_replies[0]
                    comment_replies = Comment.query.filter_by(comment_id=current_comment.id).all()

                # go one node up -> above_node and delete above_node's children nodes; repeat until the
                # current comment reaches the top reply (one of the parent's children -> comment_reply)
                while current_comment != comment_reply:
                    above_node = Comment.query.filter_by(id=current_comment.comment_id).first()

                    replies = Comment.query.filter_by(comment_id=above_node.id)
                    for reply in replies:
                        PostLike.query.filter_by(comment_id=reply.id).delete()
                        PostDislike.query.filter_by(comment_id=reply.id).delete()
                        if reply.image:
                            delete_image(reply.image)
                    replies.delete()

                    current_comment = above_node

            # delete parent's children
            comment_replies = Comment.query.filter_by(comment_id=comment.id).all()
            for comment_reply in comment_replies:
                PostLike.query.filter_by(comment_id=comment_reply.id).delete()
                PostDislike.query.filter_by(comment_id=comment_reply.id).delete()
                if comment_reply.image:
                    delete_image(comment_reply.image)
                db.session.delete(comment_reply)

        # delete parent
        PostLike.query.filter_by(comment_id=comment.id).delete()
        PostDislike.query.filter_by(comment_id=comment.id).delete()
        if comment.image:
            delete_image(comment.image)
        db.session.delete(comment)

        db.session.commit()


    post = Posts.query.filter_by(id=post_id, topic=topic_address).first_or_404()
    comment = Comment.query.filter_by(id=comment_id, topic=topic_address, post_id=post_id).first_or_404()
    topic = Topics.query.filter_by(topic_address=topic_address).first()

    if comment.author != current_user and not current_user.is_admin:
        abort(403)

    if request.method == 'POST':
        delete(comment)
        flash('Your comment has been deleted!', category='post-success')

        return redirect(url_for(
            'boards.selected_post',
            topic_address=topic.topic_address,
            post_id=post.id
        ))


@boards.route('/like', methods=['POST'])
@login_required
@check_confirmed
def like_action():
    ''' 
    Adds or removes a like/dislike to or from a post 
    via ajax request sent from votes.js
    '''

    action_request = json.loads(request.data)
    post_id = action_request['postId']
    action = action_request['action']
    user_id = action_request['userId']

    user = User.query.get_or_404(user_id)
    post = Posts.query.get_or_404(post_id)

    if action == 'like':
        if user.has_disliked_post:
            user.undislike_post(post)
        user.like_post(post)
        db.session.commit()
    if action == 'unlike':
        user.unlike_post(post)
        db.session.commit()

    if action == 'dislike':
        if user.has_liked_post:
            user.unlike_post(post)
        user.dislike_post(post)
        db.session.commit()
    if action == 'undislike':
        user.undislike_post(post)
        db.session.commit()

    return jsonify({})


@boards.route('/like_comment', methods=['POST'])
@login_required
@check_confirmed
def like_action_comment():
    ''' 
    Adds or removes a like/dislike to or from a comment
    via ajax request sent from votes.js
    '''

    action_request = json.loads(request.data)
    comment_id = action_request['commentId']
    action = action_request['action']
    user_id = action_request['userId']

    user = User.query.get_or_404(user_id)
    comment = Comment.query.get_or_404(comment_id)

    if action == 'like':
        if user.has_disliked_comment:
            user.undislike_post(post=None, comment=comment)
        user.like_post(post=None, comment=comment)
        db.session.commit()
    if action == 'unlike':
        user.unlike_post(post=None, comment=comment)
        db.session.commit()

    if action == 'dislike':
        if user.has_liked_comment:
            user.unlike_post(post=None, comment=comment)
        user.dislike_post(post=None, comment=comment)
        db.session.commit()
    if action == 'undislike':
        user.undislike_post(post=None, comment=comment)
        db.session.commit()

    return jsonify({})
