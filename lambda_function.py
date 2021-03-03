import argparse

import covid


def lambda_handler(event, context):
    timeset = event['timeset']
    jh = covid.etl.extract(covid.datasets.JOHN_HOPKINS)
    jh = covid.etl.transform(jh, timeset)
    response = covid.etl.load(jh)
    return {'status': response.read()}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--timeset',
        choices=['full', 'yesterday'],
        nargs='?',
        default='yesterday',
        help='Provide date range of dataset to be uploaded'
    )
    args = parser.parse_args()
    event = {'timeset': args.timeset}
    lambda_handler(event, None)
