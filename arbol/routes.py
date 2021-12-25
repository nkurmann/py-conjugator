from __future__ import annotations
from flask import Flask, render_template, request
from arbol.config import VERB_DATABASE_PATH, VERB_LOOKUP_PATH

from arbol.search_engine import SearchEngine
from arbol.conjugator import Conjugator
from arbol.entity import Mood, Tense, VerbTense, VerbConjugation


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

    indicative_past_tenses = [Tense.preterite,
                              Tense.imperfect,
                              Tense.present_perfect,
                              Tense.past_perfect,
                              Tense.conditional_perfect,
                              Tense.preterite_archaic]
    indicative_present_tenses = [Tense.present, Tense.conditional]
    indicative_future_tenses = [Tense.future, Tense.future_perfect]

    subjunctive_past_tenses = [Tense.imperfect,
                               Tense.present_perfect, Tense.past_perfect]
    subjunctive_present_tenses = [Tense.present]
    subjunctive_future_tenses = [Tense.future, Tense.future_perfect]

    @app.route("/<infinitive>")
    def conjugate(infinitive):

        gerund = conjugator.gerund_dict[infinitive]
        pastparticiple = conjugator.pastparticiple_dict[infinitive]
        english_meaning = conjugator.english_meaning_dict[infinitive]

        # maintain contents of search box
        query = request.args.get("q", default="", type=str)

        conjugation: VerbConjugation = conjugator.verb_dict[infinitive]
        indicative_past = conjugation.get_tenses(
            Mood.indicative, indicative_past_tenses)
        indicative_present = conjugation.get_tenses(
            Mood.indicative, indicative_present_tenses)
        indicative_future = conjugation.get_tenses(
            Mood.indicative, indicative_future_tenses)

        subjunctive_past = conjugation.get_tenses(
            Mood.subjunctive, subjunctive_past_tenses)
        subjunctive_present = conjugation.get_tenses(
            Mood.subjunctive, subjunctive_present_tenses)
        subjunctive_future = conjugation.get_tenses(
            Mood.subjunctive, subjunctive_future_tenses)

        imperative_present = conjugation.get_tenses(
            [Mood.imperative_affirmative, Mood.imperative_negative], Tense.present)

        pronouns = ["yo", "tú", "él/ella/ud.", "nosotros/as",
                    "vosotros/as", "ellos/as/uds."]

        def get_forms(verb_tense: VerbTense) -> list[str]:
            return [
                verb_tense.form_1s,
                verb_tense.form_2s,
                verb_tense.form_3s,
                verb_tense.form_1p,
                verb_tense.form_2p,
                verb_tense.form_3p
            ]

        return render_template("conjugate.html",
                               indicative_past=indicative_past,
                               indicative_present=indicative_present,
                               indicative_future=indicative_future,
                               subjunctive_past=subjunctive_past,
                               subjunctive_present=subjunctive_present,
                               subjunctive_future=subjunctive_future,
                               imperative_present=imperative_present,
                               infinitive=infinitive,
                               gerund=gerund,
                               pastparticiple=pastparticiple,
                               english_meaning=english_meaning,
                               pronouns=pronouns,
                               get_forms=get_forms,
                               query=query)

    @app.route("/xms")
    def xmas():
        return render_template("xms.html")

    return app
