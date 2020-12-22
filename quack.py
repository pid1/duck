#!/usr/bin/env python3
"""An HTML-based URL shortener for static sites."""

import argparse
import configparser
import os
import random
import string
import sys

# Create our parser object and define the URL param we take
parser = argparse.ArgumentParser(description="A Github Pages based URL shortener.")
parser.add_argument("url", help="The target URL.")
args = parser.parse_args()

HTML_RESULT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta http-equiv="Refresh" content="0; url='{target}'" />
    <link rel="icon" type="image/png" href="data:image/png;base64,">
</head>
</html>""".format(target=args.url)

# Attempt to load in the config file, gracefully handing the cases
# where we can't for whatever reason.
config = configparser.ConfigParser()
try:
    config.read('duck.ini')
except configparser.Error as exception:
    print(exception)
    print("Error parsing the config file. Quitting...")
    sys.exit(1)

SLUG = ''
slug_length = config.get('options', 'sluglength')
for length in range(int(slug_length)):
    SLUG = SLUG + random.choice(string.ascii_letters)

site_dir = config.get('config', 'sitedir')

# Do some sanity checking
if not os.path.isdir(site_dir):
    print("Configured site directory doesn't exist. Quitting...")
    sys.exit(1)
if os.path.isfile(site_dir + '/' + SLUG + '.html'):
    print("Slug already exists, please re-run \
    to regenerate the slug. Quitting...")
    sys.exit(1)


try:
    writefile = open(site_dir + '/' + SLUG + '.html', 'x')
    writefile.write(HTML_RESULT)
    writefile.close()
except OSError as exception:
    print(exception)
    print("Error saving the site file. Quitting...")
    sys.exit(1)
print("Success! Slug is " + SLUG)
