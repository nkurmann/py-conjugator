from dataclasses import dataclass
from enum import Enum
# {
#     "translation": "controlled\r",
#     "verb": "controlar",
#     "tense": "Pastparticiple"
# },
# {
#     "performer": "yo",
#     "mood": "Indicative",
#     "infinitive": "controlar",
#     "long": "he controlado",
#     "performer_en": "I",
#     "tense": "Present Perfect",
#     "has_long": true,
#     "translation": "to control; to inspect; check"
# },


class Mood(str, Enum):
    indicative = "Indicativo"
    subjunctive = "Subjunctive"
    imperative_affirmative = "Imperativo Afirmativo"
    imperative_negative = "Imperativo Negativo"


class Tense(str, Enum):
    present = "Presente"
    future = "Futuro"
    imperfect = "Imperfecto"
    preterite = "Pretérito"
    conditional = "Condicional"
    present_perfect = "Presente perfecto"
    future_perfect = "Futuro perfecto"
    past_perfect = "Pluscuamperfecto"
    preterite_archaic = "Pretérito anterior"
    conditional_perfect = "Condicional perfecto"


def dict_to_verb(conjugated_form: str, verb_dict: dict):
    if verb_dict["tense"] == "Pastparticiple":
        return InvariantVerb(conjugated=conjugated_form, **verb_dict)
    if verb_dict["tense"] == "Gerund":
        return InvariantVerb(conjugated=conjugated_form, **verb_dict)
    if verb_dict["tense"] == "Infinitive":
        return InfinitiveVerb(conjugated=conjugated_form, **verb_dict)
    return FormedVerb(conjugated=conjugated_form, **verb_dict)


@dataclass
class InvariantVerb:
    # the conjugated form matched by the query
    conjugated: str

    translation: str
    tense: str
    verb: str  # english

    # "translation": "to destroy",
    # "tense": "Infinitive",
    # "verb_english": "I destroy; am destroying"


def InfinitiveVerb(conjugated: str, translation: str, verb_english: str, tense: str):
    return InvariantVerb(conjugated=conjugated, translation=translation, verb=verb_english, tense=tense)


@dataclass
class FormedVerb:
    # the conjugated form matched by the query
    conjugated: str

    performer: str
    mood: str
    infinitive: str
    performer_en: str
    tense: str
    translation: str

    has_long: bool
    long: str = None

    def get_performer(self):
        is_imperative = self.mood == Mood.imperative_affirmative or self.mood == Mood.imperative_negative
        if is_imperative:
            return f"({self.performer})"
        return self.performer

    def get_formed_verb(self):
        if self.has_long:
            return self.long
        return self.conjugated

    def get_full_tense(self):
        if self.mood == Mood.indicative or self.mood == "Indicative":
            return self.tense
        if (self.mood == Mood.imperative_affirmative) \
                or (self.mood == Mood.imperative_negative) \
                or (self.mood == "Imperative Affirmative")\
                or (self.mood == "Imperative Negative"):
            return self.mood
        return f"{self.mood} {self.tense}"  # subjunctive


class Conjugation:
    def __init__(self, **kwargs):

        self.english = kwargs["verb_english"]  # sentence
        # self.english_meaning = kwargs["infinitive_english"]

        # self.gerund = kwargs["gerund"]
        # self.gerund_english = kwargs["gerund_english"]

        # self.pastparticiple = kwargs["pastparticiple"]
        # self.pastparticiple_english = kwargs["pastparticiple_english"]

        self.infinitive = kwargs["infinitive"]

        self.mood = kwargs["mood"]
        self.mood_english = kwargs["mood_english"]

        self.tense = kwargs["tense"]
        self.tense_english = kwargs["tense_english"]

        self.form_1s = kwargs["form_1s"]
        self.form_2s = kwargs["form_2s"]
        self.form_3s = kwargs["form_3s"]
        self.form_1p = kwargs["form_1p"]
        self.form_2p = kwargs["form_2p"]
        self.form_3p = kwargs["form_3p"]
