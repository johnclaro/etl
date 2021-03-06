import etl
from etl.covid.datasets.hse import HSE
from etl.covid.datasets.johnhopkins import JohnHopkins


def main(event, context):
    etl.settings.DAYS = event.get('days')
    etl.settings.PROD = event.get('prod')

    source = event.get('source')
    extraction = event.get('extraction')

    sources = {
        'johnhopkins': JohnHopkins(extraction).etl(),
        'hse': HSE(extraction).etl()
    }
    status = sources[source]

    return {**status, **event}
