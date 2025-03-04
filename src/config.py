# coding: utf-8

"""
Helper methods to get the user's OAuth credentials.
"""

import json
import os.path

try:
    # pylint: disable=redefined-builtin,invalid-name
    input = raw_input
except NameError:
    pass


def read(msg):
    """Wrapper around the input module for easier mock-ing."""
    return input(msg)


def get_oauth(path):
    """Loads the OAuth credentials from the file if it exists, otherwise asks the user for them."""
    if os.path.exists(path):
        return read_oauth(path)

    auth = {
        'consumer_key': '',
        'consumer_secret': '',
        'access_token': '',
        'access_token_secret': ''
    }
    auth['consumer_key'] = read('Consumer key: ')
    auth['consumer_secret'] = read('Consumer secret: ')
    auth['access_token'] = read('Access token: ')
    auth['access_token_secret'] = read('Access token secret: ')

    write_oauth(path, auth)
    return auth


def read_oauth(path):
    """Read the OAuth config file and fix any inconsistency within if necessary."""
    data = open(path).read()
    parsed = json.loads(data)

    # Rename "consumer_token" to "consumer_key"
    if 'consumer_token' in parsed:
        parsed['consumer_key'] = parsed['consumer_token']
        del parsed['consumer_token']
        write_oauth(path, parsed)

    return parsed


def write_oauth(path, auth):
    """Write the OAuth config file as pretty-printed JSON."""
    with open(path, 'w') as oauth_file:
        json.dump(auth, oauth_file, indent=4, default=str)
