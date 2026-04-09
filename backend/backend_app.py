"""Masterblog: Exercise to practice the backend development of an API,
in this case for an Blog application"""
import logging

from flask import Flask, jsonify, request
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


@app.route('/api/posts', methods=['GET'])
@limiter.limit("10/minute") # limits the number of requests
def get_posts():
    app.logger.debug(f"{request.method} received for /api/posts")
    return jsonify(POSTS)


@app.errorhandler(400)
def invalid_data_error(error):
    """handle invalid data error"""
    return jsonify({"error": "Invalid data sent!"})


@app.errorhandler(404)
def not_found_error(error):
    """handle http errors in case a ressource is not found"""
    return jsonify({"error": "Requested ressource could not be found!"})


@app.errorhandler(405)
def method_not_allowed_error(error):
    return jsonify({"error": "Method Not Allowed"}), 405


@app.errorhandler(429)
def to_many_requests_error(error):
    return jsonify({"error": "Too Many Requests! 10 per minute allowed."}), 429


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
