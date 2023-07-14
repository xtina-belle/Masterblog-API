import flask


app = flask.Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    """Render a home page"""
    return flask.render_template("index.html")


@app.route("/<int:post_id>/update", methods=["GET"])
def update_page(post_id):
    """Render update page for post"""
    return flask.render_template("update.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)
