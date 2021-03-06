import etl
from covid.sources.hse import JohnHopkins, HSE


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
