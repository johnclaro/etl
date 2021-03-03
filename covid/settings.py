import os
from distutils.util import strtobool


DEBUG = bool(strtobool(os.environ.get('DEBUG', 'False')))

if DEBUG:
    WEBSITE_URL = 'http://localhost:8000'
else:
    WEBSITE_URL = 'https://www.johnclaro.com'
