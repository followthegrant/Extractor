import argparse
import logging
import sys

from importlib import import_module


COMMANDS = {
    'extract': {
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
    'get_disclosures': {
        'args': ({
            'flag': '--file',
            'help': 'input file with 1 json record per line'
        }, {
            'flag': '--pretty',
            'help': 'Output JSON format nice indented or 1 record per row',
            'action': 'store_true',
            'default': False
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
