import etl
from etl.sources import jh, hse


def main(event, context):
    etl.settings.DAYS = event.get('days')
    etl.settings.PROD = event.get('prod')

    source = event.get('source')
    extract = event.get('extract')

    options = {
        'jh': {
            'cases': jh.etl()
        },
        'hse': {
            'swabs': hse.swabs.etl()
        }
    }

    status = options[source][extract]

    return {**status, **event}
