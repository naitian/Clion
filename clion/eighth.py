# -*- coding: utf-8 -*-
from .utils import get, post, DictDotLookup


def get_block_list(auth, length, start, end):
    """Get list of blocks.

    :auth: auth object
    :length: number of blocks
    :start: start date
    :end: end date (requires start date, overrides length)

    """

    if start is not None:
        blocks = DictDotLookup(get("blocks",
                                 data={"start_date": start},
                                 auth=auth)).results
    else:
        blocks = DictDotLookup(get("blocks", auth=auth)).results
    return blocks


def get_sched_activities(auth, block):
    """Get list of scheduled activities for a block.

    :auth: auth object
    :block: block id

    """
    return DictDotLookup(get("blocks/" + str(block), auth=auth))


def post_signup(auth, said, aid=None, bid=None):
    """Sign up for activity using scheduled_activity id by default

    :auth: auth object
    :said: scheduled activity id
    """

    data = {"scheduled_activity": said,
            "use_scheduled_activity": True}

    return DictDotLookup(post("signups/user", data=data, auth=auth))
