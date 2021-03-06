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
    args = parser.parse_args()
    event = vars(args)
    print(event)
    response = etl.main(event, None)
    print(response)
