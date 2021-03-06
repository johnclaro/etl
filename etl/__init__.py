import etl
from etl.sources import jh, hspc


def main(event, context):
    etl.settings.DAYS = event.get('days')

    source = event.get('source')
    if source == 'jh':
        jh.etl()
    elif source == 'hspc':
        hspc.etl()

    return {'status': 'Completed'}
