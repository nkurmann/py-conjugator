from arbol.search_engine import AccentlessMatcher, SearchEngine, create_multidict
from arbol.config import VERB_LOOKUP_PATH


def test_simple_search():
    se = SearchEngine(VERB_LOOKUP_PATH)
    results = se.search("ubica")
    assert len(results) == 2
    assert results[1].mood == "Imperative Affirmative"
    assert not results[0].has_long


def test_find():
    matcher = AccentlessMatcher("áéíóúaeiou")
    assert matcher.find("á") == ["a", "á"]


def test_find_by_prefix():
    matcher = AccentlessMatcher([
        "temé",
        "teme",
        "temo",
        "aaa",
        "zzz",

    ])
    assert matcher.find_by_prefix("tem") == ["teme", "temé", "temo"]
    assert matcher.find_by_prefix("teme") == ["teme", "temé"]


def test_create_multidict():
    values = [("jim", "beer"),
              ("joshua", "cider"),
              ("jim", "breadsticks")]
    assert create_multidict(values) == {"jim": ["beer", "breadsticks"],
                                        "joshua": ["cider"]}
