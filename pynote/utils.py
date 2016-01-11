import click
from . import config


def echo(text, no_pager=False):
    """A helper which decides between using a pager or not."""
    if click.get_terminal_size()[1] < len(text.splitlines()) and not no_pager:
        click.echo_via_pager(text)
    else:
        click.echo(text)


def info(text):
    """Add 'Info: ' prefix and colorize output."""
    msg = 'Info: ' + text
    if config.COLORS:
        click.secho(msg, fg='yellow')
    else:
        click.echo(msg)


def error(text):
    """Add 'Error: ' prefix and colorize output."""
    msg = 'Error: ' + text
    if config.COLORS:
        click.secho(msg, fg='red')
    else:
        click.echo(msg)


def die(text):
    """A shortcut for error(); die()."""
    error(text)
    exit(1)
