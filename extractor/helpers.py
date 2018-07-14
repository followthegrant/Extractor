"""
extraction helpers
"""


def get_author_abbrev_mapping(authors):
    return {
        a['name']: ''.join([i[0].upper() for i in a['name'].split()])
        for a in authors
    }
