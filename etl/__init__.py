import etl
from etl.sources import jh, hspc


def main(event, context):
    etl.settings.DAYS = event.get('days')
    etl.settings.PROD = event.get('prod')

    source = event.get('source')
    if source == 'jh':
        status = jh.etl()
    elif source == 'hspc':
        status = hspc.etl()

    return {**status, **event}
