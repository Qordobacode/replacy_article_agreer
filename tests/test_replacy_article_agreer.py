import en_core_web_sm
from replacy import ReplaceMatcher
from spacy.util import filter_spans
from replacy_article_agreer import ArticleAgreer


nlp = en_core_web_sm.load()

match_dict = {
    "a-to-an": {
        "patterns": [{"LOWER": "problem", "POS": "NOUN"}],
        "suggestions": [[{"TEXT": "answer"}]],
        "description": "we don't have problems here",
        "tests": {"positive": [], "negative": []},
    },
    "an-to-a": {
        "patterns": [{"LOWER": "issue", "POS": "NOUN"}],
        "suggestions": [[{"TEXT": "solution"}]],
        "description": "good vibes ONLY",
        "tests": {"positive": [], "negative": []},
    },
    "overlap": {
        "patterns": [{"LOWER": "problem"}, {"LOWER": "issue"}],
        "suggestions": [[{"TEXT": "whatever"}]],
        "tests": {"positive": [], "negative": []},
    },
}

replaCy = ReplaceMatcher(nlp, match_dict)
aa = ArticleAgreer()
replaCy.add_pipe(filter_spans, name="filter_spans", before="joiner")
replaCy.add_pipe(aa, name="article_agreer", after="joiner")


def test_a_to_an():
    orig = "I have a problem."
    span = replaCy(orig)[0]
    replacement = span._.suggestions[0]
    assert (
        orig.replace(span.text, replacement) == "I have an answer."
    ), "Automatically corrects a to an"


def test_an_to_a():
    orig = "I have an issue."
    span = replaCy(orig)[0]
    replacement = span._.suggestions[0]
    assert (
        orig.replace(span.text, replacement) == "I have a solution."
    ), "Automatically corrects a to an"


def test_with_filtering():
    orig = "This big problem issue."
    span = replaCy(orig)[0]
    replacement = span._.suggestions[0]
    assert (
        orig.replace(span.text, replacement) == "This big whatever."
    ), "Respects span filtering"
