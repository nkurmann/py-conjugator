from csv import DictReader
from typing import Dict, Tuple
from arbol.entity import VerbTense, Mood, Tense, VerbConjugation
from enum import Enum


class Conjugator:
    def __init__(self, verb_database_csv_path: str) -> None:

        self.verb_dict: Dict[str, VerbConjugation] = {}
        self.gerund_dict: Dict[str, str] = {}
        self.pastparticiple_dict: Dict[str, str] = {}
        self.english_meaning_dict: Dict[str, str] = {}

        with open(verb_database_csv_path) as fp:
            for e in DictReader(fp):
                infinitive = e["infinitive"]

                if infinitive not in self.verb_dict:
                    self.verb_dict[infinitive] = VerbConjugation()
                    self.english_meaning_dict[infinitive] = e["infinitive_english"]
                    self.gerund_dict[infinitive] = e["gerund"]
                    # self.gerund_english = kwargs["gerund_english"]

                    self.pastparticiple_dict[infinitive] = e["pastparticiple"]
                    # self.pastparticiple_english = kwargs["pastparticiple_english"]

                # mood = e["mood"]
                # tense = e["tense"]

                self.verb_dict[infinitive].add_tense(VerbTense(**e))

    def conjugate(self, infinitive: str, mood: Mood = Mood.indicative, tense: Tense = Tense.present) -> VerbTense:
        return self.verb_dict[infinitive].get_tense(mood, tense)
