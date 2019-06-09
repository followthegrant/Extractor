"""
plos parser for disclosures
"""


import nltk.data
from lxml import html

from extractor.helpers import get_author_abbrev_mapping


tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')


def _replace(part, mapping):
    """
    replace TM with Tim Smith
    """
    if part:
        for name, abbrev in mapping.items():
            part = part.replace(abbrev, name)
        return part


def _get_sentences(content, mapping):
    text = _replace(content, mapping) or ''
    return [t.strip() for t in tokenizer.tokenize(text)]


def parse(doc, authors):
    mapping = get_author_abbrev_mapping(authors)
    doc = html.fromstring(doc.decode())
    financial = doc.xpath("//*[@id='artText']/div[2]/p[6]/text()")[0]
    interests = doc.xpath("//*[@id='artText']/div[2]/p[7]/text()")[0]
    disclosures = {
        'interests': _get_sentences(interests, mapping),
        'financial': _get_sentences(financial, mapping)
    }
    # author specific disclosures
    for author in authors:
        author['disclosures'] = {kind: [d for d in _disclosures if d and author['name'] in d]
                                 for kind, _disclosures in disclosures.items()}
    # paper wide disclosures
    paper_disclosures = {
        kind: [d for d in _disclosures if d and d not in [_d for a in authors for _d in a['disclosures'][kind]]]
        for kind, _disclosures in disclosures.items()
    }
    return authors, paper_disclosures
