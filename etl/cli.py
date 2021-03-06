import argparse

import etl


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'source',
        choices=('jh', 'hspc'),
        help='(1) jh: John Hopkins, '
             '(2) hspc: Health Protection Surveillance Centre'
    )
    parser.add_argument(
        '-d',
        '--days',
        default=1,
        type=int,
        help='0: All, N: Today - N days'
    )
    parser.add_argument(
        '-p',
        '--prod',
        dest='prod',
        action='store_true',
        help='Activate production mode'
    )
    parser.set_defaults(prod=False)
    args = parser.parse_args()
    event = vars(args)
    status = etl.main(event, None)
    return {**status, **event}