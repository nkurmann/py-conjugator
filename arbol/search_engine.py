import json
from typing import Dict, Iterable, List, Tuple, Union

from arbol.entity import FormedVerb, InvariantVerb, dict_to_verb
from unidecode import unidecode
from bisect import bisect, bisect_left, bisect_right


class SearchEngine:
    def __init__(self, verb_lookup_json_path: str) -> None:
        with open(verb_lookup_json_path) as fp:
            self.lookup_dict: dict = json.load(fp)
        self.accentless_matcher = AccentlessMatcher(self.lookup_dict.keys())

    def search(self, query) -> List[Union[InvariantVerb, FormedVerb]]:
        verbs = self.find_matching_verbs(query)
        print(f"Found {verbs=}")
        return [dict_to_verb(verb, match)
                for verb in verbs
                for match in self.lookup_dict[verb]]

    def find_matching_verbs(self, query) -> List[str]:
        """Finds the conjugated forms of all verbs that could reasonably match query."""

        print(f"Looking for query {query}")

        # exact matches
        if query in self.lookup_dict:
            print("found exact match")
            return [query]

        # cleaned matches
        if keys := self.accentless_matcher.find(query):
            print("found cleaned match")
            return keys

        # cleaned prefix matches
        if keys := self.accentless_matcher.find_by_prefix(query):
            print("found prefix match")
            return keys

        return []


def clean(s: str):
    return unidecode(s).lower().strip()


def create_multidict(values: List[Tuple[str, str]]) -> Dict[str, List[str]]:
    res: Dict[str, List[str]] = {}

    for clean_val, original_val in values:
        if clean_val not in res:
            res[clean_val] = []
        res[clean_val].append(original_val)

    return res


class AccentlessMatcher:
    def __init__(self, keys: Iterable[str]) -> None:

        # [("hable", "hablé"), ...]
        self.values = [(clean(key), key) for key in keys]
        # allow for bisect usage
        self.values.sort()

        self.full_match_dict = create_multidict(self.values)

    def find(self, query: str) -> List[str]:
        print("find")
        q = clean(query)
        if q in self.full_match_dict:
            return self.full_match_dict[q]
        return []

    def find_by_prefix(self, query: str) -> List[str]:
        print("find by prefix")
        if len(query) < 2:
            return []

        q = clean(query)
        low_q = (q, "")
        high_q = (q+"zzz", "")

        lo = bisect_left(self.values, low_q)
        hi = bisect(self.values, high_q)

        matches = self.values[lo:hi]
        return [r[1] for r in matches]
