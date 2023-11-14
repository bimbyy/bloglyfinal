from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from models import User, Post, Tag, PostTag  # Import the new models

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'class123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ... (existing code)

# Routes for Tags

@app.route('/tags')
def list_tags():
    tags = Tag.query.all()
    return render_template('tags_list.html', tags=tags)

@app.route('/tags/new', methods=['GET', 'POST'])
def add_tag():
    if request.method == 'POST':
        tag_name = request.form['name']
        tag = Tag(name=tag_name)
        db.session.add(tag)
        db.session.commit()
        flash('Tag added successfully', 'success')
        return redirect(url_for('list_tags'))
    return render_template('add_tag.html')

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    tag = Tag.query.get(tag_id)
    return render_template('show_tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=['GET', 'POST'])
def edit_tag(tag_id):
    tag = Tag.query.get(tag_id)
    if request.method == 'POST':
        tag.name = request.form['name']
        db.session.commit()
        flash('Tag updated successfully', 'success')
        return redirect(url_for('list_tags'))
    return render_template('edit_tag.html', tag=tag)

# Routes for Posts with Tags

@app.route('/posts/<int:post_id>/add_tags', methods=['GET', 'POST'])
def add_tags_to_post(post_id):
    post = Post.query.get(post_id)
    if request.method == 'POST':
        tag_ids = request.form.getlist('tags')
        tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

        for tag in tags:
            post.tags.append(tag)

        db.session.commit()
        flash('Tags added to post successfully', 'success')
        return redirect(url_for('post_detail', post_id=post.id))

    tags = Tag.query.all()
    return render_template('add_tags_to_post.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit_tags', methods=['GET', 'POST'])
def edit_tags_of_post(post_id):
    post = Post.query.get(post_id)
    if request.method == 'POST':
        tag_ids = request.form.getlist('tags')
        post.tags.clear()  # Clear existing tags

        tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

        for tag in tags:
            post.tags.append(tag)

        db.session.commit()
        flash('Tags of post updated successfully', 'success')
        return redirect(url_for('post_detail', post_id=post.id))

    tags = Tag.query.all()
    return render_template('edit_tags_of_post.html', post=post, tags=tags)

# ... (other existing routes)

if __name__ == '__main__':
    app.run(debug=True)
