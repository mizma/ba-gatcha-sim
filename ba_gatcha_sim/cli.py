#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2026 mizma <omoikane@path-works.net>
# All rights reserved.

"""Main CLI Setup and Entrypoint."""

from __future__ import absolute_import, division, print_function

# Import the main click library
import click
# Import the sub-command implementations
from .basim import basim
# Import the version information
from ba_gatcha_sim._version import __version__

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.command()
@click.option(
    '--old', '-o', is_flag=True,
    help='run old gatcha sim'
    )
@click.option(
    '--reset', '-r', is_flag=True,
    help='reset old count after 2 PU pull'
    )
@click.option(
    '--new', '-n', is_flag=True,
    help='run new gatcha sim'
    )
@click.option(
    '--target', '-t', default=2, type=int,
    metavar='<tgt>',
    help='simulate up to target pickup count'
    )
@click.option(
    '--cycles', '-c', default=10000, type=int,
    metavar='<cyc>',
    help='number of cycles to simulate'
    )
@click.option(
    '--count', '-C', default=0, type=int,
    metavar='<cnt>',
    help='initial count for new gatcha'
    )
@click.option(
    '--verbose', '-v', count=True,
    help='output in verbose mode'
    )
@click.version_option(version=__version__)
def cli(**kwargs):
    """BlueArchive gatcha monte-carlo simulation
    """
    basim.cmd(kwargs)
    pass

# Entry point
def main():
    """Main script."""
    cli()

if __name__ == '__main__':
    main()
