from flask import Flask, render_template, request
from arbol.config import VERB_DATABASE_PATH, VERB_LOOKUP_PATH

from arbol.search_engine import SearchEngine
from arbol.conjugator import Conjugator, Conjugation, Verb


def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    se = SearchEngine(VERB_LOOKUP_PATH)
    conjugator = Conjugator(VERB_DATABASE_PATH)

    @app.route("/")
    def index():

        query = request.args.get("q", default="", type=str)
        print(f"Getting {query=}")
        search_results = se.search(query)
        print(f"Found {len(search_results)} results")
        return render_template("search.html",
                               query=query,
                               search_results=search_results)

    @app.route("/<infinitive>")
    def conjugate(infinitive):
        conj: Conjugation = conjugator.verb(infinitive)
        gerund = conjugator.gerund_dict[infinitive]
        pastparticiple = conjugator.pastparticiple_dict[infinitive]
        english_meaning = conjugator.english_meaning_dict[infinitive]


        query = request.args.get("q", default="", type=str) # maintain contents of search box

        return render_template("conjugate.html",
                               verb=conj, infinitive=infinitive, gerund=gerund, pastparticiple=pastparticiple, english_meaning=english_meaning, query=query)

    @app.route("/xms")
    def xmas():
        return render_template("xms.html")
    return app
