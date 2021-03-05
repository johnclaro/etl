import argparse

import beetle


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d',
        '--days',
        choices=('a', '1',),
        nargs='?',
        default='1',
        help='(a) - All, (1) - 1 day'
    )
    parser.add_argument(
        '-s',
        '--source',
        choices=('jh', 'hspc'),
        required=True,
        help='(jh) - John Hopkins, (hspc) - Health Protection Surveillance Centre'
    )
    args = parser.parse_args()
    event = vars(args)
    response = beetle.main(event, None)
    print(response)
