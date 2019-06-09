"""
base parser for disclosures, works with already extracted text blocks
"""


import nltk.data
from lxml import html

from extractor.helpers import get_author_abbrev_mapping


tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')


def _get_parafs(elements, parafs=[]):
    el = next(elements)
    if el.tag == 'p':
        parafs.append(el.text)
        _get_parafs(elements, parafs)
    return parafs


def _get_part(elements, part_name):
    elements = (e for e in elements)
    for el in elements:
        if el.text and part_name in el.text.lower():
            return _get_parafs(elements, [])
    return []


def _replace(part, mapping):
    """
    replace TM with Tim Smith
    """
    if part:
        for name, abbrev in mapping.items():
            part = part.replace(abbrev, name)
        return part


def _get_sentences(content, part, mapping):
    text = ' '.join(_replace(p, mapping) for p in _get_part(content, part) if p)
    return tokenizer.tokenize(text)


def parse(doc, authors):
    mapping = get_author_abbrev_mapping(authors)
    doc = html.fromstring(doc.decode())
    content = doc.xpath("//div[@id='author-information-section']/div[@id='author-information-content']")
    if content:
        disclosures = {part: _get_sentences(content[0], part, mapping) for part in ('interests', 'financial')}
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
    return authors, None
