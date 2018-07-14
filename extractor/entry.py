import argparse
import logging
import sys

from importlib import import_module


COMMANDS = {
    'metadata': {
        'args': ({
            'flag': 'info',
            'help': 'YAML File containing extraction infos'
        }, {
            'flag': 'directory',
            'help': 'Base directory containing downloaded papers'
        }, {
            'flag': '--pretty',
            'help': 'Output JSON format nice indented or 1 record per row',
            'action': 'store_true',
            'default': False
        })
    },
    'sync_elasticsearch': {
        'args': ({
            'flag': 'source',
            'help': 'JSON tree file our directory containing trees'
        }, {
            'flag': '--host',
            'help': 'Elasticsearch host:port',
            'default': 'localhost:9200'
        }, {
            'flag': '--index',
            'help': 'Name of elasticsearch index',
            'default': 'genesapi'
        }, {
            'flag': '--overwrite',
            'help': 'Overwrite existing index',
            'action': 'store_true'
        }, {
            'flag': '--quiet',
            'help': 'Don\'t raise exceptions from elasticsearch client',
            'action': 'store_true',
            'default': False
        }, {
            'flag': '--jobs',
            'help': 'Thread count for `parallel_bulk`',
            'type': int,
            'default': 8
        }, {
            'flag': '--queue-size',
            'help': 'Queue size for `parallel_bulk`',
            'type': int,
            'default': 8
        }, {
            'flag': '--chunk-size',
            'help': 'Number of documents per chunk',
            'type': int,
            'default': 100
        }, {
            'flag': '--chunk-bytes',
            'help': 'Maximum bytes per chunk',
            'type': int,
            'default': 512000000
        })
    }
}


def main():
    parser = argparse.ArgumentParser(prog='ftg_extractor')
    parser.add_argument('--loglevel', default='INFO')
    subparsers = parser.add_subparsers(help='commands help')
    for name, opts in COMMANDS.items():
        subparser = subparsers.add_parser(name)
        subparser.set_defaults(func=name)
        for args in opts.get('args', []):
            flag = args.pop('flag')
            subparser.add_argument(flag, **args)

    args = parser.parse_args()
    logging.basicConfig(stream=sys.stderr, level=getattr(logging, args.loglevel))

    if hasattr(args, 'func'):
        try:
            func = import_module('extractor.%s' % args.func)
            func.main(args)
        except ImportError:
            raise Exception('`%s` is not a valid command.' % args.func)
