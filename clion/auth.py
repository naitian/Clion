# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from os import path, mkdir, remove
from json import loads, dumps

import click
import requests

from .utils import get_auth_path, BASE_URL


CLIENT_ID = "jsPriMNQKrcxx2dzQjDrwgOr35PgTgOpXiHXGCjC"


def login_required(func):
    """Authentication decorator
    """
    def check_auth(*args, **kwargs):
        if path.exists(get_auth_path()):
            auth = loads(open(get_auth_path(), 'r').readline())

            auth_time = datetime.fromtimestamp(auth["auth_time"])
            expiry = timedelta(seconds=auth["expires_in"])
            now = datetime.now()

            if now > auth_time + expiry:
                # Requires refresh
                auth = refresh(auth['refresh_token'])
        else:
            click.echo("You must log in using 'clion login' first.")
            return
        func(auth, *args, **kwargs)
    return check_auth


def auth(username, password):
    """Prompt for username and password
    """
    if not path.exists(click.get_app_dir("clion")):
        mkdir(click.get_app_dir("clion"))

    r = requests.post(BASE_URL + "oauth/token",
                      data={
                          "grant_type": "password",
                          "client_id": CLIENT_ID,
                          "scope": "read write",
                          "username": username,
                          "password": password
                      })
    auth = r.json()
    try:
        print(auth)
        assert auth['access_token'] is not None
        auth['auth_time'] = datetime.now().timestamp()
        auth_file = open(get_auth_path(), 'w+')
        auth_file.write(dumps(auth))
        auth_file.close()
        return True
    except:
        return False


def unauth():
    """Delete auth file.
    :returns: TODO

    """
    try:
        remove(get_auth_path())
        return True
    except:
        return False


def refresh(token):
    """Refreshes with refresh token, then writes new auth info to file and
    returns the auth info

    :token: Refresh token

    """
    auth_file = open(get_auth_path(), 'w')

    r = requests.post(BASE_URL + "oauth/token",
                      data={
                          "grant_type": "refresh_token",
                          "client_id": CLIENT_ID,
                          "refresh_token": token
                      })
    auth = r.json()
    auth['auth_time'] = datetime.now().timestamp()
    auth_file.write(dumps(auth))

    return auth
