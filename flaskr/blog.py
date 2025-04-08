from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


def get_post(id, check_author=True):
    db = get_db()
    post = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)
    
    post = dict(post) 

    # Fetch like count for the post
    like_count = db.execute(
        'SELECT COUNT(*) FROM post_likes WHERE post_id = ?',
        (id,)
    ).fetchone()[0]

    # Check if the current user has liked this post
    user_liked = db.execute(
        'SELECT 1 FROM post_likes WHERE post_id = ? AND user_id = ?',
        (id, g.user['id'])
    ).fetchone() is not None

    post['likes_count'] = like_count
    post['user_liked'] = user_liked

     # Fetch comments for the post
    comments = db.execute(
        'SELECT c.id, c.body, c.created, u.username'
        ' FROM comments c JOIN user u ON c.user_id = u.id'
        ' WHERE c.post_id = ? ORDER BY c.created DESC',
        (id,)
    ).fetchall()

    post['comments'] = comments
    
    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))


@bp.route('/<int:id>')
def post_details(id):
    post = get_post(id, check_author=False)  # You can set check_author=False for details page
    return render_template('blog/post_details.html', post=post)


@bp.route('/<int:id>/like', methods=('POST',))
@login_required
def like_post(id):
    db = get_db()
    post = get_post(id, check_author=False)  # Get the post, no need to check author for liking

    # Check if the user has already liked the post
    like = db.execute(
        'SELECT 1 FROM post_likes WHERE post_id = ? AND user_id = ?',
        (id, g.user['id'])
    ).fetchone()

    if like:
        # User already liked, so we remove the like (unlike)
        db.execute(
            'DELETE FROM post_likes WHERE post_id = ? AND user_id = ?',
            (id, g.user['id'])
        )
        db.commit()
        flash('You unliked this post.', 'info')
    else:
        # User has not liked the post yet, so we add the like
        db.execute(
            'INSERT INTO post_likes (post_id, user_id) VALUES (?, ?)',
            (id, g.user['id'])
        )
        db.commit()
        flash('You liked this post!', 'success')

    return redirect(url_for('blog.post_details', id=id))


@bp.route('/<int:id>/comment', methods=('POST',))
@login_required
def comment(id):
    post = get_post(id, check_author=False)  # Fetch the post without author check

    body = request.form['body']
    error = None

    if not body:
        error = 'Comment cannot be empty.'

    if error is not None:
        flash(error)
    else:
        db = get_db()
        db.execute(
            'INSERT INTO comments (post_id, user_id, body) VALUES (?, ?, ?)',
            (id, g.user['id'], body)
        )
        db.commit()
        flash('Your comment has been posted!', 'success')

    return redirect(url_for('blog.post_details', id=id))
