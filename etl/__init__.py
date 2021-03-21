import json

from etl.hse.datasets import HSE
from etl.johnhopkins.datasets import JohnHopkins

settings = {
    'time': 1,
    'load_base': 'http://localhost:8000',
}


def apply_settings(flags):
    for key, value in flags.items():
        settings[key] = value

    if not flags.get('debug'):
        settings['load_base'] = 'https://www.johnclaro.com'


def run(flags, context):
    apply_settings(flags)
    source = flags.get('source')
    output = {'results': [], 'settings': settings}

    sources = {
        'hse': HSE,
        'johnhopkins': JohnHopkins
    }

    try:
        source_object = sources[source]()
    except KeyError:
        exit('That source does not exist')

    results = source_object.etl()
    for result in results:
        output['results'].append(result)

    output = json.dumps(output, indent=4)
    return output
