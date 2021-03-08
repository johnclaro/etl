import json

import etl
from etl.hse.datasets import HSE
from etl.johnhopkins.datasets import JohnHopkins


def run(flags, context):
    etl.settings.TIME = flags.get('time')
    etl.settings.PROD = flags.get('prod')

    source = flags.get('source')
    dataset = flags.get('dataset')

    sources = {
        'johnhopkins': JohnHopkins(dataset),
        'hse': HSE(dataset)
    }
    source = sources[source]
    task = source.etl()
    output = {'task': task, 'flags': flags}
    output = json.dumps(output, indent=4)
    return output
