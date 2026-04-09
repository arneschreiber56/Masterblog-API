"""Masterblog: Exercise to practice the backend development of an API,
in this case for an Blog application"""
import logging

from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(app=app, key_func=get_remote_address)
CORS(app)  # This will enable CORS for all routes
# Configuration of logging
logging.basicConfig(
    filename="masterblog_backend.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]

def validate_data(data):
    """validates data of post request. Returns True if correct, returns False if
    empty"""
    if not data:
        return False
    return True


def find_post_by_id(id):
    """finds and returns a post by id or None, if search fails"""
    for post in POSTS:
        if post.get("id") == id:
            return post
    return None


@app.route('/api/posts', methods=["GET", "POST"])
@limiter.limit("10/minute") # limits the number of requests
def get_posts():
    app.logger.debug(f"{request.method} received for /api/posts")
    if request.method == "POST":
        # raise Exception supressed silent=True -> Error handling later with abort
        data = request.get_json(silent=True)
        if not validate_data(data):
            abort(400, description="Request body is missing or invalid JSON")
        new_title = data.get("title", "")
        new_content = data.get("content", "")
        if not new_title:
            abort(400, description="Title is missing")
        if not new_content:
            abort(400, description="Content is missing")
        new_id = max((post["id"] for post in POSTS), default=0) +1
        new_post = {
            "id": new_id,
            "title": new_title,
            "content": new_content
            }
        POSTS.append(new_post)
        return jsonify(new_post), 201
    return jsonify(POSTS)


@app.route("/api/posts/<int:id>", methods=["PUT"])
@limiter.limit("10/minute")
def update_post(id):
    """Updates a Post by id"""
    app.logger.debug(f"{request.method} request received for api/posts/{id}")
    post = find_post_by_id(id)
    if post is None:
        abort(404, description="Could not find a post with this ID!")
    new_data = request.get_json(silent=True)
    if not new_data:
        abort(400, description="Request body is missing or invalid JSON")
    new_post = post
    new_title = new_data.get("title", "")
    new_content = new_data.get("content", "")
    if new_title:
        # new_post points already at the correct location in POSTS,
        # so it will change immediately the global variable!
        new_post["title"] = new_title
    if new_content:
        new_post["content"] = new_content

    return jsonify(new_post), 200


@app.route("/api/posts/<int:id>", methods=["DELETE"])
@limiter.limit("10/minute")
def delete_post(id):
    """Deletes a Post by id"""
    app.logger.debug(f"{request.method} request received for api/posts/{id}")
    post = find_post_by_id(id)
    if post is None:
        abort(404, description="Could not find a post with this ID!")

    POSTS.remove(post)

    return jsonify(post), 200


@app.errorhandler(400)
def bad_request_error(error):
    """handle invalid data error"""
    return jsonify(
        {"error": f"Bad Request: {error.description}!"}
    ), 400


@app.errorhandler(404)
def not_found_error(error):
    """handle http errors in case a ressource is not found"""
    return jsonify({"error": f"Not found:{error.description}"}), 404


@app.errorhandler(405)
def method_not_allowed_error(error):
    return jsonify({"error": "Method Not Allowed"}), 405


@app.errorhandler(429)
def to_many_requests_error(error):
    return jsonify({"error": "Too Many Requests! 10 per minute allowed."}), 429


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
