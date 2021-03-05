import argparse

from etl import jh, hspc


def main(event, context):
    dataset = event.get('dataset')
    if dataset == 'jh':
        jh.etl(event)
    elif dataset == 'hspc':
        hspc.etl(event)
    return {'status': 'Completed'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--timeset',
        choices=('full', 'yesterday',),
        nargs='?',
        default='yesterday',
        help='Date range of dataset to be extracted and uploaded'
    )
    parser.add_argument(
        '-d',
        '--dataset',
        choices=('jh', 'hspc'),
        required=True,
        help='Dataset to be extracted'
    )
    args = parser.parse_args()
    event = vars(args)
    response = main(event, None)
    print(response)
