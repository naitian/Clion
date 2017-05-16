# -*- coding: utf-8 -*-

from .utils import get, DictDotLookup


def get_user_info(auth, uid=None):
    """Returns user profile
    """
    if uid is None:
        data = get("profile", auth=auth)
    return DictDotLookup(data)
