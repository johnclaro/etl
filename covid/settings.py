import os
from distutils.util import strtobool


DEBUG = bool(strtobool(os.environ.get('DEBUG', 'True')))

if DEBUG:
    WEBSITE_URL = 'http://localhost:8000'
else:
    WEBSITE_URL = 'https://johnclaro.com'