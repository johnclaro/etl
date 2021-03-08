import os
from distutils.util import strtobool

TIME = 1
PROD = bool(strtobool(os.environ.get('PROD', 'False')))

if PROD:
    URL = 'https://www.johnclaro.com'
else:
    URL = 'http://localhost:8000'
