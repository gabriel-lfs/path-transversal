import base64
import os

from flask import Flask, request, jsonify

UPLOAD_DIRECTORY = "files/api_uploaded_files"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


app = Flask(__name__)


@app.route("/files")
def list_files():
    """Endpoint to list files on the server."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return jsonify(files)


@app.route("/download_file", methods=["POST"])
def get_file():
    """Download a file."""
    body = request.json
    with open(f'{UPLOAD_DIRECTORY}/{body["path"]}') as f:
        return '\n'.join(f.readlines())


@app.route("/upload_file", methods=["POST"])
def post_file():
    """Upload a file."""

    body = request.json

    with open(os.path.join(UPLOAD_DIRECTORY, body['filename']), "wb") as fp:
        fp.write(base64.standard_b64decode(body['file']))

    # Return 201 CREATED
    return "", 201


if __name__ == "__main__":
    app.run(debug=True, port=8000)