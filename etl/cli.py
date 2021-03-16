import argparse

import etl


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'source',
        help='Name of source'
    )
    parser.add_argument(
        '-t',
        '--time',
        default=1,
        type=int,
        help='0: All, N: Today - N days'
    )
    parser.add_argument(
        '--prod',
        dest='prod',
        action='store_true',
        help='Activate production mode'
    )
    parser.add_argument(
        '-d',
        '--dataset',
        required=True,
        help='Set dataset to be extracted'
    )
    parser.add_argument(
        '-u',
        '--username',
        help='Username for load base'
    )
    parser.add_argument(
        '-p',
        '--password',
        help='Password for load base'
    )
    parser.set_defaults(prod=False)
    args = parser.parse_args()
    flags = vars(args)
    output = etl.run(flags, None)
    return output
