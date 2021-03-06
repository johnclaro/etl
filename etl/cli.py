import argparse

import etl


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'source',
        choices=('johnhopkins', 'hse'),
        help='Refer to README for list of sources'
    )
    parser.add_argument(
        '-t',
        '--time',
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
    parser.add_argument(
        '-d',
        '--dataset',
        choices=('cases', 'swabs', 'vaccines'),
        default='cases',
        help='Set dataset to be extracted'
    )
    parser.set_defaults(prod=False)
    args = parser.parse_args()
    event = vars(args)
    status = etl.main(event, None)
    return {**status, **event}
