import argparse

import covid


def lambda_handler(event, context):
    timeset = event['timeset']

    nyt = covid.etl.extract(covid.datasets.NEW_YORK_TIMES)
    jh = covid.etl.extract(covid.datasets.JOHN_HOPKINS)

    nyt = covid.etl.transform(nyt, timeset)
    jh = covid.etl.transform(jh, timeset)
    df = covid.etl.join(nyt, jh)

    return {'status': 200}


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
