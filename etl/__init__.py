import json

import etl
from etl.hse.datasets import HSE
from etl.johnhopkins.datasets import JohnHopkins

settings = { 
    'time': 1,
    'prod': False,
    'load_base': 'http://localhost:8000',
}

def apply_settings(flags):
    for key, value in flags.items():
        settings[key] = value

    if flags.get('prod'):
        settings['load_base'] = 'https://www.johnclaro.com'


def run(flags, context):
    apply_settings(flags)
    source = flags.get('source')
    dataset = flags.get('dataset')

    sources = {
        'johnhopkins': JohnHopkins(dataset),
        'hse': HSE(dataset)
    }
    source = sources[source]
    task = source.etl()

    output = {'task': task, 'settings': settings}
    output = json.dumps(output, indent=4)
    return output
