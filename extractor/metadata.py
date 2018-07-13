"""
extract metadata for papers and export as csv
"""


import logging
import sys
import pandas as pd
import os
import yaml
from bs4 import BeautifulSoup as bs

from extractor.util import get_files

logger = logging.getLogger(__name__)


def _extract_metadata(rows, info):
    res = []
    for _, row in rows:
        publisher = info.get(row['publisher_slug'])
        if not publisher:
            logger.log(logging.ERROR, 'No extraction info for publisher `%s`' % row['publisher_name'])
        else:
            pass
            # with open(row[])
            # doc =
            # for key, value


def main(args):
    with open(args.info) as f:
        info = yaml.load(f)

    files = get_files(args.directory, lambda x: x.endswith('.html'))
    df = pd.read_csv(args.index)
    df['file'] = df['path'].map(lambda x: os.path.split(x)[1])
    df = df[df['file'].isin(f[0] for f in files)]
    import ipdb; ipdb.set_trace()
