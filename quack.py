#!/usr/bin/env python3
"""An HTML-based URL shortener for static sites."""

import argparse
import configparser
import os
import random
import re
import string
import sys

# Create our parser object and define the URL param we take
parser = argparse.ArgumentParser(description="A Github Pages based URL shortener.")
parser.add_argument("url", help="The target URL.")
parser.add_argument("--slug", help="Define the slug manually")
args = parser.parse_args()

HTML_RESULT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta http-equiv="Refresh" content="0; url='{target}'" />
    <title>Redirecting...</title>
    <link rel="icon" type="image/png" href="data:image/png;base64,">
</head>
</html>""".format(target=args.url)

DUP_CHECK = """<meta http-equiv="Refresh" content="0; url='{target}'" />""".format(target=args.url)

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
if args.slug:
    SLUG = args.slug
else:
    slug_length = config.get('options', 'sluglength')
    for length in range(int(slug_length)):
        SLUG = SLUG + random.choice(string.ascii_letters)

site_dir = config.get('config', 'sitedir')

# Do some sanity checking

# Ensure the site directory exists
if not os.path.isdir(site_dir):
    print("Configured site directory doesn't exist. Quitting...")
    sys.exit(1)

# Ensure the slug doesn't exist already
if os.path.isfile(site_dir + '/' + SLUG + '.html'):
    print("Slug already exists, please re-run to regenerate the slug. Quitting...")
    sys.exit(1)

# Check for duplicates
for root, dirs, files in os.walk(site_dir):
    for name in files:
        file_extension = os.path.splitext(name)
        if file_extension[1] == ".html":
            try:
                to_check = open(site_dir + '/' + name, 'r')
            except OSError as exception:
                print(exception)
                print("Failed to open site file for duplicate checking. Quitting...")
                sys.exit(1)
            if re.search(DUP_CHECK, to_check.read()):
                print("This target already exists as slug " + file_extension[0])
                sys.exit(0)
            to_check.close()

# Write out our Refresh file
try:
    writefile = open(site_dir + '/' + SLUG + '.html', 'x')
    writefile.write(HTML_RESULT)
    writefile.close()
except OSError as exception:
    print(exception)
    print("Error saving the site file. Quitting...")
    sys.exit(1)

# Let the user know we succeeded and give them the slug
print("Success! Slug is " + SLUG)