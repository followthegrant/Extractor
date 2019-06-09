"""
optimize records for indexing into elasticsearch:
- add autocomplete lists
- spread paper records into single coi-statement records
"""


import logging
import json
import sys


logger = logging.getLogger(__name__)


def _unpack(paper, args):
    paper = json.loads(paper)
    authors = paper.pop('authors')

    # author specific disclosures
    for author in authors:
        disclosures_data = author.pop('disclosures', {})
        for type_, disclosures in disclosures_data.items():
            for disclosure in disclosures:
                if disclosure:
                    data = {
                        'type': type_,
                        'scope': 'author',
                        'disclosure': disclosure,
                        'author': author,
                        'paper': paper
                    }
                    if args.pretty:
                        sys.stdout.write(json.dumps(data, indent=2) + '\n')
                    else:
                        sys.stdout.write(json.dumps(data) + '\n')

    # paper specific disclosures
    disclosures_data = paper.pop('disclosures', {}) or {}
    for type_, disclosures in disclosures_data.items():
        for disclosure in disclosures:
            if disclosure:
                data = {
                    'type': type_,
                    'scope': 'paper',
                    'disclosure': disclosure,
                    'authors': authors,
                    'paper': paper
                }
                if args.pretty:
                    sys.stdout.write(json.dumps(data, indent=2) + '\n')
                else:
                    sys.stdout.write(json.dumps(data) + '\n')


def main(args):
    if args.file:
        with open(args.file) as f:
            for line in f.readlines():
                _unpack(line, args)
    else:
        for line in sys.stdin:
            _unpack(line, args)
