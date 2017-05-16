# -*- coding: utf-8 -*-

from os import path
from pprint import pformat

import click
import requests

from colorama import Fore, Back, Style


BASE_URL = "https://ion.tjhsst.edu/"


def get_auth_path():
    """Return path for auth.json
    :returns: TODO

    """
    base_path = click.get_app_dir('clion')
    auth_file_path = path.join(base_path, 'auth.json')

    return auth_file_path


def get(endpoint, data=None, auth=None):
    """GET request to endpoint

    :endpoint: endpoint without base url
        Ex. "https://ion.tjhsst.edu/api/schedule" -> "schedule"
    """
    url = BASE_URL + "api/" + endpoint
    headers = None

    if auth:
        headers = {"Authorization": auth['token_type'] +
                   ' ' + auth['access_token']}
    r = requests.get(url, params=data, headers=headers)

    if r.status_code // 100 == 2:
        return r.json()
    else:
        error("Error: " + str(r.status_code))
        return r.json()


def post(endpoint, data=None, auth=None):
    """POST request to endpoint

    :endpoint: endpoint without base url
        Ex. "https://ion.tjhsst.edu/api/schedule" -> "schedule"
    """
    url = BASE_URL + "api/" + endpoint
    headers = None

    if auth:
        headers = {"Authorization": auth['token_type'] +
                   ' ' + auth['access_token']}
    r = requests.post(url, data=data, headers=headers)

    if r.status_code // 100 == 2:
        return r.json()
    else:
        error("Error: " + str(r.status_code))
        return r.json() 


def success(message):
    """Print success message with green background
    """
    click.echo("{}Success: {}{}".format(Back.GREEN + Fore.BLACK,
                                        message,
                                        Style.RESET_ALL))


def error(message):
    """Print error message with red background
    """
    click.echo("{}Error: {}{}".format(Back.RED + Fore.WHITE,
                                      message,
                                      Style.RESET_ALL))


def bold(message):
    """Make string bold
    """
    return "{}{}{}".format(Style.BRIGHT, message, Style.RESET_ALL)


def dim(message):
    """Make string dim
    """
    return "{}{}{}".format(Style.DIM, message, Style.RESET_ALL)


def color(message, color):
    """Color the string with colorama color
    """
    return "{}{}{}".format(color, message, Style.RESET_ALL)


class DictDotLookup(object):
    """
    http://code.activestate.com/recipes/576586-dot-style-nested-lookups-over-dictionary-based-dat/
    Creates objects that behave much like a dictionaries, but allow nested
    key access using object '.' (dot) lookups.
    """
    def __init__(self, d):
        for k in d:
            if isinstance(d[k], dict):
                self.__dict__[k] = DictDotLookup(d[k])
            elif isinstance(d[k], (list, tuple)):
                l = []
                for v in d[k]:
                    if isinstance(v, dict):
                        l.append(DictDotLookup(v))
                    else:
                        l.append(v)
                self.__dict__[k] = l
            else:
                self.__dict__[k] = d[k]

    def __getitem__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]

    def __iter__(self):
        return iter(self.__dict__.keys())

    def __repr__(self):
        return pformat(self.__dict__)
