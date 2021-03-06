import etl
from etl.sources import jh, hse


def main(event, context):
    etl.settings.DAYS = event.get('days')
    etl.settings.PROD = event.get('prod')

    source = event.get('source')
    if source == 'jh':
        status = jh.etl()
    elif source == 'hse':
        status = hse.etl()

    return {'status': **status, 'options': **event}
