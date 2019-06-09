"""
extract metadata for papers and export as csv
"""


from datetime import datetime
import logging
import json
import yaml
from importlib import import_module
from bs4 import BeautifulSoup as bs
from bs4.element import Tag
import sys

from extractor.util import get_files, parallelize


logger = logging.getLogger(__name__)


def _should_process(doc, type_info):
    """
    return true or false if given `doc` should be processed
    """
    doc_type = doc.find('meta', {'name': type_info['key']})
    if not doc_type:
        doc_type = doc.find('meta', {'property': type_info['key']})
    if doc_type:
        doc_type = doc_type.get('content')
        return doc_type in type_info['values'], doc_type
    return False, doc_type


def _get_disclosures(doc, authors, parser_name):
    parser = import_module('extractor.%s' % parser_name)
    return parser.parse(doc, authors)


def _extract_author(el, author_info):
    data = {
        'name': el.get('content'),
        'institutions': []
    }
    for _el in el.next_siblings:
        if isinstance(_el, Tag):
            name = _el.get('name')
            if author_info.get('institution') and name == author_info.get('institution'):
                data['institutions'].append(_el.get('content'))
            if name == author_info['name']:
                break
    return data


def _extract_metadata(files, info, pretty):
    res = []
    for fname, fpath in files:
        with open(fpath) as f:
            doc = bs(f, 'html.parser')

        should_process, doc_type = _should_process(doc, info['type'])
        if should_process:
            logger.log(logging.DEBUG, 'processing `%s` ...' % fpath)

            # initial data
            metadata = {
                'type': doc_type,
                'meta': {
                    'fname': fname,
                    'fpath': fpath,
                    'parsed': datetime.now().isoformat()
                }
            }

            # meta data
            for key, name in info['meta'].items():
                meta = doc.find('meta', {'name': name})
                if not meta:
                    meta = doc.find('meta', {'property': name})
                if meta:
                    metadata[key] = meta.get('content')
                else:
                    if key in info.get('defaults', []):
                        metadata[key] = info['defaults'][key]
                        logger.log(
                            logging.DEBUG,
                            'Using default ("%s") for `%s` in `%s`' % (info['defaults'][key], name, fpath)
                        )
                    else:
                        logger.log(
                            logging.WARNING,
                            'No meta entry and no default value found for `%s` in `%s`' % (name, fpath)
                        )

            # tags
            if info.get('tags'):
                metadata['tags'] = [i.get('content') for i in doc.find_all('meta', {'name': info['tags']})]

            # authors
            authors = [_extract_author(el, info['authors'])
                       for el in doc.find_all('meta', {'name': info['authors']['name']})]

            # extract disclosures
            authors, paper_disclosures = _get_disclosures(doc, authors, info['disclosure_parser'])
            metadata['authors'] = authors
            metadata['disclosures'] = paper_disclosures

            if pretty:
                sys.stdout.write(json.dumps(metadata, indent=2))
            else:
                sys.stdout.write(json.dumps(metadata) + '\n')
            res.append(1)
        else:
            res.append(0)
    return res


def main(args):
    with open(args.info) as f:
        info = yaml.load(f)

    files = get_files(args.directory, lambda x: x.endswith('.html'))
    # res = _extract_metadata(files, info, args.pretty)
    res = parallelize(_extract_metadata, files, info, args.pretty)
    count = sum(res)
    skipped = len(res) - count
    logger.log(logging.INFO, 'Extracted metadata from %s files, %s skipped.' % (count, skipped))
