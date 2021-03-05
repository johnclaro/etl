import etl
from etl.sources import jh, hspc


def main(event, context):
    etl.settings.TIMESET = event.get('timeset')

    dataset = event.get('dataset')
    if dataset == 'jh':
        jh.etl()
    elif dataset == 'hspc':
        hspc.etl()

    return {'status': 'Completed'}
