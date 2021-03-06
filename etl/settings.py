import os
from distutils.util import strtobool

DAYS = 1
DEBUG = bool(strtobool(os.environ.get('DEBUG', 'True')))

if DEBUG:
    URL = 'http://localhost:8000'
else:
    URL = 'https://www.johnclaro.com'
