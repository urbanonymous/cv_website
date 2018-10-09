""" - Urbano Gutierrez CV - V0.3 - OCTOBER 2018 """
import os
from flask import (Flask, Response, abort, flash, jsonify, redirect,
                   render_template, request, send_from_directory, session, url_for)
from flask_sockets import Sockets
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from werkzeug.debug import DebuggedApplication
from werkzeug.serving import run_with_reloader
from werkzeug.utils import secure_filename


# APP SETTINGS
BASE_DIR = "/".join(os.path.realpath(__file__).split("/")[:-1])
UPLOAD_FOLDER = "{}/uploads/".format(BASE_DIR)
QR_FOLDER = "{}/static/img/qr/".format(BASE_DIR)

app = Flask(__name__)
app.debug = True
app.secret_key = os.urandom(12)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["SESSION_TYPE"] = "filesystem"
sockets = Sockets(app)


# ENDPOINTS
@app.route("/", methods=["GET"])
@app.route("/index", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/static/webapp")
def redirect_web():
    return redirect(url_for("index"))

@app.route("/404")
def error_404():
    return render_template("404.html")

@app.route('/download/cv', methods=["GET"])
def download_cv():
    return send_from_directory(directory="static/downloads", filename="cv.pdf")

@app.route('/download/vc', methods=["GET"])
def download_vc():
    return send_from_directory(directory="static/downloads", filename="vc.pdf")


# SERVER
def run_server():
    if app.debug:
        application = DebuggedApplication(app)
    else:
        application = app

    server = pywsgi.WSGIServer(("", 80), application,
                               handler_class=WebSocketHandler)
    server.serve_forever()


if __name__ == "__main__":
    run_with_reloader(run_server)
