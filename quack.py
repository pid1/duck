#!/usr/bin/env python3
"""An HTML-based URL shortener for static sites."""

import argparse
import configparser
import os
import random
import re
import string
import sys

# Create our parser object, define the URL params we take, and parse them
parser = argparse.ArgumentParser(description="A Github Pages based URL shortener.")
parser.add_argument("url", help="The target URL.")
parser.add_argument("--slug", help="Define the slug manually")
args = parser.parse_args()

# This generaes a minimally viable HTML that performs the browser redirection.
HTML_RESULT = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta http-equiv="Refresh" content="0; url='{args.url}'" />
    <title>Redirecting...</title>
    <link rel="icon" type="image/png" href="data:image/png;base64,">
</head>
</html>"""

# Check for duplicate target URLs
def duplicate_url_check(checkstring, site_directory):
    """Given a site directory and a test string, check to see if we've already created
    a .html file containing this test string"""
    for root, directory, files in os.walk(site_directory): #pylint: disable-unused-variable
        for name in files:
            file_name = os.path.splitext(name)
            if file_name[1] == ".html":
                try:
                    to_check = open(site_directory  + '/' + name, 'r', encoding="utf-8")
                except OSError as open_exception:
                    print(open_exception)
                    print("Failed to open site file for duplicate checking.")
                    sys.exit(1)
                if re.search(checkstring, to_check.read()):
                    return 0
                to_check.close()

# Generate a random unused slug.
# In the case of maximum recursion depth, we just bail out right now
def sluggen(slug_length, site_directory):
    """Generate a random slug, checking for duplicates"""
    try:
        slug = ''.join(random.choice(string.ascii_lowercase) for _ in range(slug_length))
        while os.path.isfile(site_directory + '/' + slug + '.html'):
            sluggen(slug_length, site_directory)
        return slug
    except OSError as exception:
        print("Failed to generate a slug. Try increasing the maximum slug length.")
        sys.exit(1)

def main():
    """Main function"""
    # Attempt to load in the config file, gracefully handing the cases
    # where we can't for whatever reason.
    config = configparser.ConfigParser()
    try:
        config.read('duck.ini')
    except configparser.Error as exception:
        print(exception)
        print("Error parsing the config file.")
        sys.exit(1)
    site_dir = config.get('config', 'sitedir')
    slug_length = config.getint('options', 'sluglength')

    # Ensure the site directory exists
    if not os.path.isdir(site_dir):
        print("Configured site directory doesn't exist.")
        sys.exit(1)

    # Ensure the slug doesn't exist already, if set
    if args.slug:
        if os.path.isfile(site_dir + '/' + args.slug + '.html'):
            if args.slug:
                print("This slug is already in use.")
                sys.exit(1)

    # We assume that if this string occurs in any HTML file within the target directory, this means
    # we already have a slug for the given target URL.
    dup_url_check = f"""<meta http-equiv="Refresh" content="0; url='{args.url}'" />"""

    # Check for duplicate URLs on the provided slug
    if duplicate_url_check(dup_url_check, site_dir) == 0:
        print("This target already exists.")
        sys.exit(0)

    # Create our slug, either user-provided or auto-generated
    slug = ""
    if args.slug:
        slug = args.slug
    else:
        slug = sluggen(slug_length, site_dir)

    # Write out our Refresh file
    try:
        writefile = open(site_dir + '/' + slug + '.html', 'x', encoding="utf-8")
        writefile.write(HTML_RESULT)
        writefile.close()
    except OSError as exception:
        print(exception)
        print("Error saving the site file.")
        sys.exit(1)

    # Let the user know we succeeded and give them the slug
    print("Success! Slug is " + slug)

if __name__ == "__main__":
    main()
