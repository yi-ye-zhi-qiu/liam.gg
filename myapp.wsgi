#!/usr/bin/env python3
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/liamisaacs/')

from app import app as application
# where "__init__" is the name of the py file
# that initializes your flask app

# app configs can be set here
# or can be done in envvars or files
# env is dev by default, useful to debug
#application.secret_key = 'random key'
#application.env = 'production'
