# -*- coding: utf-8 -*-

from utils import get


def get_bell_schedule(date):
    """Print out bell schedule

    :date: Date formatted in YYYY-MM-DD

    """
    if date is not None:
        data = get("schedule/{}".format(date))
    else:
        data = get("schedule")['results'][0]

    schedule = {}

    schedule['day_name'] = data['day_type']['name']
    schedule['date'] = data['date']
    schedule['blocks'] = data['day_type']['blocks']

    if 'red' in schedule['day_name'].lower():
        schedule['day_type'] = 'r'
    elif 'blue' in schedule['day_name'].lower():
        schedule['day_type'] = 'b'
    else:
        schedule['day_type'] = 'a'

    return schedule
