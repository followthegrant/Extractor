"""
nature parser for disclosures
"""


from lxml import html

from extractor.helpers import get_author_abbrev_mapping


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


def _replace(p, mapping):
    """
    replace TM with Tim Smith
    """
    if p:
        for name, abbrev in mapping.items():
            p = p.replace(abbrev, name)
        return p


def parse(doc, authors):
    mapping = get_author_abbrev_mapping(authors)
    doc = html.fromstring(doc.decode())
    content = doc.xpath("//div[@id='author-information-section']/div[@id='author-information-content']")
    if content:
        disclosures = {
            'interests': [_replace(p, mapping) for p in _get_part(content[0], 'interests')],
            'financial': [_replace(p, mapping) for p in _get_part(content[0], 'financial')],
        }
        for author in authors:
            author['disclosures'] = disclosures
    return authors
