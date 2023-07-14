import dataclasses
import datetime
import logging
import os

import flask
from flask import request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from DB.blog_posts_db import BlogPostsDB
from DB.blog_posts_db import PostDto


# Absolute path to the JSON file in directory DB
json_path = os.path.join(os.path.dirname(__file__), "DB", "blog_posts.json")

POST_DATA = ["id_", "title", "content", "author", "like", "date"]

app = flask.Flask(__name__)
CORS(app)  # This will enable CORS for all routes
limiter = Limiter(get_remote_address, app=app)
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

blog_posts_db = BlogPostsDB(json_path)
blog_posts_db.setup()


@app.route("/api/posts", methods=["GET"])
@limiter.limit("20/minute")
def get_posts():
    """Adds post to db or
    :returns: list of posts or sorted list of posts"""
    if "sort" in request.args:
        app.logger.info("GET request received for /api/posts?sort")
        if request.args["sort"] in POST_DATA:
            return flask.jsonify(_sort_posts(request.args["sort"], request.args["direction"]))
        return flask.jsonify({"error": "Invalid sort key"}), 400
    app.logger.info("GET request received for /api/posts")
    return flask.jsonify(blog_posts_db.get_blog_posts())


@app.route("/api/posts", methods=["POST"])
@limiter.limit("20/minute")
def add_posts():
    """Adds post to db or
    :returns: list of posts or sorted list of posts"""
    post = request.get_json()
    if not _is_valid_post_data(post):
        return flask.jsonify({"error": "Invalid post data"}), 400
    post["id_"] = max((post.id_ for post in blog_posts_db.get_blog_posts()), default=0) + 1
    post["author"] = "Your name"
    post["date"] = datetime.date.today().strftime("%Y-%m-%d")
    blog_posts_db.add_post(PostDto(**post))
    return flask.jsonify(post), 201


@app.route("/api/posts/<int:post_id>/like", methods=["POST"])
@limiter.limit("20/minute")
def like_post(post_id: int):
    """Can delete post from DB, edit post data or likes"""
    post = blog_posts_db.get_post(post_id)
    if not post:
        return flask.jsonify({"error": f"Post with id {post_id} was not found"}), 404

    blog_posts_db.like_post(post_id)
    return flask.jsonify(dataclasses.asdict(blog_posts_db.get_post(post_id)))


@app.route("/api/posts/<int:post_id>/update", methods=["GET"])
@limiter.limit("20/minute")
def update_post(post_id):
    """Render update page for post by id"""
    post = blog_posts_db.get_post(post_id)
    if not post:
        return "Post not found", 404
    return flask.jsonify(dataclasses.asdict(post))


@app.route("/api/posts/<int:post_id>", methods=["PUT"])
@limiter.limit("20/minute")
def edit_post(post_id: int):
    """Can delete post from DB, edit post data or likes"""
    post = blog_posts_db.get_post(post_id)
    if not post:
        return flask.jsonify({"error": f"Post with id {post_id} was not found"}), 404

    new_post = request.get_json()
    post = dataclasses.asdict(post)
    for key, value in new_post.items():
        post[key] = value
    blog_posts_db.update_post(post_id, post["title"], post["content"])
    return flask.jsonify(post), 200


@app.route("/api/posts/<int:post_id>", methods=["DELETE"])
@limiter.limit("20/minute")
def delete_post(post_id: int):
    """Can delete post from DB, edit post data or likes"""
    post = blog_posts_db.get_post(post_id)
    if not post:
        return flask.jsonify({"error": f"Post with id {post_id} was not found"}), 404

    blog_posts_db.delete_post(post_id)
    return flask.jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200


@app.route("/api/posts/search")
@limiter.limit("20/minute")
def search():
    """:returns: filtered by request args list of posts """
    result = []
    for key, value in request.args.items():
        for post in blog_posts_db.get_blog_posts():
            post = dataclasses.asdict(post)
            if key in post and value.lower() in post[key].lower():
                if post in result:
                    continue
                result.append(post)
    return flask.jsonify(result)


def _sort_posts(key, direction):
    """
    Sort a list of posts by key
    :param key: post attribute
    :param direction: asc or desc
    :return: sorted list of posts
    """
    posts = blog_posts_db.get_blog_posts()
    if direction == "desc":
        return sorted(posts, key=lambda post: getattr(post, key), reverse=True)
    return sorted(posts, key=lambda post: getattr(post, key), reverse=False)


def _is_valid_post_data(post):
    """Checks if all needed data is present for post
    :param post: dict with post data
    :returns: bool"""
    return "title" in post and "content" in post


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004, debug=True)
