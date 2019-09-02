import base64
import os
from uuid import uuid4

from decouple import config
from flask import Flask, request, jsonify, abort
from redis import Redis

UPLOAD_DIRECTORY = "files/api_uploaded_files"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


api = Flask(__name__)
redis = Redis(
    host=config('REDIS_HOST', default='localhost'),
    port=config('REDIS_PORT', default='6379')
)


@api.route("/files")
def list_files():
    """Endpoint to list files on the server."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return jsonify(files)


@api.route("/download_file", methods=["POST"])
def get_file():
    """Download a file."""
    body = request.json
    filename = redis.hget(UPLOAD_DIRECTORY, body["path"])
    if not filename:
        abort(404, 'Arquivo inexistente')

    filename = filename.decode('utf-8')
    with open(f'{UPLOAD_DIRECTORY}/{filename}') as f:
        return '\n'.join(f.readlines())


@api.route("/upload_file", methods=["POST"])
def post_file():
    """Upload a file."""

    body = request.json
    unique_id = str(uuid4())
    redis.hset(UPLOAD_DIRECTORY, body['filename'], unique_id)
    with open(os.path.join(UPLOAD_DIRECTORY, unique_id), "wb") as fp:
        fp.write(base64.standard_b64decode(body['file']))

    # Return 201 CREATED
    return "", 201


if __name__ == "__main__":
    api.run(debug=True)
