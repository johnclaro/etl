import json

import etl
from etl.covid.hse.source import HSE
from etl.covid.johnhopkins.source import JohnHopkins


def main(flags, context):
    etl.settings.TIME = flags.get('time')
    etl.settings.PROD = flags.get('prod')
    etl.settings.SOURCE = flags.get('source')
    etl.settings.DATASET = flags.get('dataset')

    sources = {
        'johnhopkins': JohnHopkins(),
        'hse': HSE()
    }
    source = sources[etl.settings.SOURCE]
    task = source.etl()
    output = {'task': task, 'flags': flags}
    output = json.dumps(output, indent=4)
    return output
