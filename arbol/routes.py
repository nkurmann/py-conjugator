from flask import Flask, render_template


def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")

    @app.route("/")
    def index():
        return render_template("index.html",
                               infinitive="saludar (al mundo)")
    return app
