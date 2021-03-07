import etl
from etl.covid.datasets.hse import HSE
from etl.covid.datasets.johnhopkins import JohnHopkins


def main(event, context):
    etl.settings.TIME = event.get('time')
    etl.settings.PROD = event.get('prod')
    etl.settings.SOURCE = event.get('source')
    etl.settings.DATASET = event.get('dataset')

    sources = {
        'johnhopkins': JohnHopkins(),
        'hse': HSE()
    }
    source = sources[etl.settings.SOURCE]
    status = source.etl()
    message = {**status, **event}
    return message
