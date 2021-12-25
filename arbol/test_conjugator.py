from arbol.conjugator import VerbTense, Conjugator, Tense
from arbol.config import VERB_DATABASE_PATH
from arbol.entity import Mood


def test_conjugator():
    conj = Conjugator(VERB_DATABASE_PATH)

    assert conj.conjugate("abrazar").form_1s == "abrazo"
    assert conj.conjugate("abrazar", tense=Tense.preterite).form_1s == "abracé"


def test_conjugation():
    conj = Conjugator(VERB_DATABASE_PATH)
    bailar = conj.verb_dict["bailar"]

    for tense in Tense:
        res = bailar.get_tense(Mood.indicative, tense)
    subj_tenses = ['Presente',
                   'Imperfecto',
                   'Presente perfecto',
                   'Pluscuamperfecto',
                   'Futuro',
                   'Futuro perfecto']
    for tense in subj_tenses:
        res = bailar.get_tense(Mood.subjunctive, tense)

    bailar.get_tense(Mood.imperative_affirmative, Tense.present)
    bailar.get_tense(Mood.imperative_negative, Tense.present)
