from flask import Flask, render_template, request
from arbol.config import VERB_LOOKUP_PATH

from arbol.search_engine import SearchEngine


def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    se = SearchEngine(VERB_LOOKUP_PATH)

    @app.route("/")
    def index():

        query = request.args.get("q", default="", type=str)
        print(f"Getting {query=}")
        search_results = se.search(query)
        print(f"Found {len(search_results)} results")
        return render_template("search.html",
                               query=query,
                               search_results=search_results)
    return app
