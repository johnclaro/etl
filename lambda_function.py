import argparse

from botocore.vendored import requests

import covid


def lambda_handler(event, context):
    res = requests.get('https://google.com')
    print(res)

    timeset = event.get('timeset', 'yesterday')
    dataset = event.get('dataset')
    response = {'dataset': dataset}

    if dataset == 'john_hopkins':
        jh = covid.etl.extract_csv(covid.datasets.JOHN_HOPKINS)
        jh = covid.etl.transform(jh, timeset)
        rows = covid.etl.load(jh)
        response['rows'] = rows
    elif dataset == 'hspc':
        hspc = covid.etl.extract_hspc(covid.datasets.HSPC)
        print(hspc)
    return response


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
        '--dataset',
        choices=('john_hopkins', 'hspc'),
        required=True,
        help='Dataset to be extracted'
    )
    args = parser.parse_args()
    event = vars(args)
    response = lambda_handler(event, None)
    print(response)
