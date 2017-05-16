#!/usr/bin/env python
# -*- coding: utf-8 -*-

# this is a comment

from datetime import datetime

import click
from colorama import init, Fore, Back, Style

from .auth import auth, login_required, unauth
from .bell import get_bell_schedule
from .eighth import get_block_list, get_sched_activities, post_signup
from .user import get_user_info
from .utils import success, error, bold, color

init()
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
WEEKDAYS_ABB = ["Mon.", "Tue.", "Wed.", "Thu.", "Fri.", "Sat.", "Sun."]


@click.group()
@click.version_option()
def cli():
    """Command line client for ion.tjhsst.edu
    """
    pass


@cli.command()
@click.option("--user", prompt=True)
@click.password_option(confirmation_prompt=False)
def login(user, password):
    """Log in
    """
    if auth(user, password):
        success("Successfully logged in!")
    else:
        error("Could not log in.")


@cli.command()
def logout():
    """Log out of Ion
    """
    if unauth():
        success("Successfully logged out.")
    else:
        error("Could not log out. Are you logged in?")


@cli.command()
@click.option("--date", help="Date in YYYY-MM-DD format")
def bell(date):
    """Get bell schedule"""
    schedule = get_bell_schedule(date)

    if schedule["day_type"] == 'r':
        click.echo(Back.RED, nl=False)
    if schedule["day_type"] == 'b':
        click.echo(Back.BLUE, nl=False)
    if schedule["day_type"] == 'a':
        click.echo(Back.WHITE, nl=False)

    click.echo(bold("{} ({}){}".format(schedule["day_name"],
                                       schedule["date"],
                                       Style.RESET_ALL)))

    pad = max([len(x["name"]) for x in schedule["blocks"]])
    for block in schedule["blocks"]:
        click.echo("{0: <{3}}   ({1}-{2})".format(block["name"],
                                                  block["start"],
                                                  block["end"],
                                                  pad))


@cli.command(name="me", short_help="Get information about current user")
@login_required
def me(auth):
    """Get information on current user
    """
    user = get_user_info(auth)
    info_template = """You're logged in as {0.full_name}.
Your username is {0.ion_username}, and your internal Ion ID is {0.id}.""".format(user)
    click.echo(info_template)


@cli.group()
def eighth():
    """Eighth period stuff
    """
    pass


@eighth.command(name="blocks", short_help="List upcoming blocks")
@click.option("--length", help="Number of blocks to display", default=10)
@click.option("--start", help="Start date in YYYY-MM-DD format")
@click.option("--end", help="End date in YYYY-MM-DD format")
@login_required
def list_blocks(auth, length, start, end):
    if start is None:
        start = datetime.now().strftime("%Y-%m-%d")
    if end is not None:
        end = datetime.strptime(end, "%Y-%m-%d").date()
    blocks = get_block_list(auth, length, start, end)

    ct = 0
    click.echo(bold("Block\t\tDate\t\tBlock ID\tLocked"))
    for block in blocks:
        if end is None and ct == length:
            return
        date = datetime.strptime(block.date, "%Y-%m-%d").date()
        day = WEEKDAYS[date.weekday()]
        if end is not None and date > end:
            return

        line = "{1} ({0.block_letter})\t{0.date}\t{0.id}\t\t{0.locked}".format(block, day)
        if block.locked:
            click.echo(color(line, Fore.RED))
        else:
            click.echo(line)
        ct += 1


@eighth.command(name="activities", short_help="List activities for a block")
@click.argument("block_id")
@click.option("--hide-restricted", "-r", is_flag=True)
@click.option("--hide_full", "-f", is_flag=True)
@login_required
def activities(auth, block_id, hide_restricted, hide_full):
    activities = get_sched_activities(auth, block_id)
    text = bold("Activity\t\t\tActivity ID\tCapacity\tSignup ID\n")
    for sched_act_id in activities.activities:
        sched_act = activities.activities[sched_act_id]
        line = sched_act.name_with_flags[:27]
        line += "..." if len(sched_act.name_with_flags) > 27 else " " * (30 - len(sched_act.name_with_flags))
        line += "\t"
        line += str(sched_act.id)
        line += "\t\t"
        line += "{}/{}".format(sched_act.roster.count, sched_act.roster.capacity)
        line += "\t\t"
        line += str(sched_act.scheduled_activity.id)
        line += "\n"

        if sched_act.restricted_for_user:
            line = color(line, Fore.RED)
            if hide_restricted:
                line = ""
        if sched_act.favorited:
            line = color(line, Back.YELLOW)

        if hide_full and (sched_act.roster.count + 1) / (sched_act.roster.capacity + 1) >= 1:
            line = ""

        text += line
    click.echo_via_pager(text)


@eighth.command(name="signup", short_help="Sign up for an activity")
@click.argument("sched_act_id")
@login_required
def signup(auth, sched_act_id):
    """Sign up for an activity (using scheduled_activity)
    """
    signup = post_signup(auth, sched_act_id)
    click.echo("Successfully signed up for {}!".format(signup.name))
