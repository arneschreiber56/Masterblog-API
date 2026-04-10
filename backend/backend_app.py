"""Masterblog: Exercise to practice the backend development of an API,
in this case for a Blog application"""
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

LIMIT_REQ = "10/minute"


def has_data(data):
    """validates data of POST request. Returns True if correct, returns False if
    empty"""
    if not data:
        return False
    return True


def find_post_by_id(post_id):
    """finds and returns a post by ID or None if search fails"""
    for post in POSTS:
        if post.get("id") == post_id:
            return post
    return None


def find_post_by_title(title_query, post):
    """finds a matching post by matching the query in the title.
    Returns True if match or False if not. Returns True if a query is empty"""
    if title_query:
        match_title = title_query in post.get("title").lower()
    else:
        match_title = True
    return match_title


def find_post_by_content(content_query, post):
    """finds a matching post by matching the query with the content. Returns
    True if match or False if not. Returns True if a query is empty"""
    if content_query:
        match_content = content_query in post.get("content").lower()
    else:
        match_content = True
    return match_content


def sort_posts(lst, sort_field, direction):
    """Sorts posts after method in sort in order given by direction. Returns
    sorted list"""
    sort_direc = direction == "desc"
    sorted_list = sorted(lst, key=lambda x: x[sort_field], reverse=sort_direc )
    return sorted_list


@app.route('/api/posts', methods=["GET", "POST"])
@limiter.limit(LIMIT_REQ) # limits the number of requests
def get_posts():
    app.logger.debug(f"{request.method} received for /api/posts")
    if request.method == "POST":
        # raise Exception suppressed silent=True -> Error handling later with abort
        data = request.get_json(silent=True)
        if not has_data(data):
            abort(400, description="Request body is missing or invalid JSON")
        new_title = data.get("title", "").strip()
        new_content = data.get("content", "").strip()
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
    sort = request.args.get("sort", "").strip()
    direction = request.args.get("direction", "").strip()
    lst = POSTS[:]
    if sort:
        if direction not in ("asc", "desc"):
            abort(400, description="Sort direction is not valid")
        if sort not in ("title", "content"):
            abort(400, description="Sort method is not valid")

        sorted_posts = sort_posts(lst, sort, direction)
        return jsonify(sorted_posts), 200
    return jsonify(POSTS), 200


@app.route("/api/posts/search", methods=["GET"])
@limiter.limit(LIMIT_REQ)
def search_posts():
    """GET-request route for searching and returning posts with the search
    phrase in the title or content. Returns an empty list if no match is found.
    """
    app.logger.debug(f"{request.method} request received for api/posts/search")
    title_query = request.args.get("title", "").strip().lower()
    content_query = request.args.get("content", "").strip().lower()
    matching_posts = []

    for post in POSTS:
        match_title = find_post_by_title(title_query, post)
        match_content = find_post_by_content(content_query, post)

        # for a double query only a post should be returned, which matches all
        # search queries
        if match_title and match_content:
            matching_posts.append(post)

    return jsonify(matching_posts)


@app.route("/api/posts/<int:post_id>", methods=["PUT"])
@limiter.limit(LIMIT_REQ)
def update_post(post_id):
    """Updates a Post by id"""
    app.logger.debug(f"{request.method} request received for api/posts/{post_id}")
    post = find_post_by_id(post_id)
    if post is None:
        abort(404, description="Could not find a post with this ID!")
    new_data = request.get_json(silent=True)
    if not new_data:
        abort(400, description="Request body is missing or invalid JSON")
    new_post = post
    new_title = new_data.get("title", "").strip()
    new_content = new_data.get("content", "").strip()
    if new_title:
        # new_post points already at the correct location in POSTS,
        # so it will change immediately the global variable!
        new_post["title"] = new_title
    if new_content:
        new_post["content"] = new_content

    return jsonify(new_post), 200


@app.route("/api/posts/<int:post_id>", methods=["DELETE"])
@limiter.limit(LIMIT_REQ)
def delete_post(post_id):
    """Deletes a Post by id"""
    app.logger.debug(f"{request.method} request received for api/posts/{post_id}")
    post = find_post_by_id(post_id)
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
    return jsonify({"error": f"Not found: {error.description}"}), 404


@app.errorhandler(405)
def method_not_allowed_error(error):
    return jsonify({"error": "Method Not Allowed"}), 405


@app.errorhandler(429)
def to_many_requests_error(error):
    return jsonify({"error": "Too Many Requests! 10 per minute allowed."}), 429


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
