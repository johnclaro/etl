import argparse

import covid


def lambda_handler(event, context):
    timeset = event.get('timeset', 'yesterday')
    jh = covid.etl.extract(covid.datasets.JOHN_HOPKINS)
    jh = covid.etl.transform(jh, timeset)
    loaded = covid.etl.load(jh)
    return {'status': f'Upserted {loaded} row(s)'}


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
    response = lambda_handler(event, None)
    print(response)
