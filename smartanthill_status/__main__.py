# Copyright (C) 2015 OLogN Technologies AG
#
# This source file is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License version 2
# as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import click
import requests

from smartanthill_status import __version__
from smartanthill_status.database import create_all
from smartanthill_status.travis_log_parser import (
    parse_latest_builds_statistics, parse_log_file)
from smartanthill_status.web import app


@click.group()
@click.version_option(__version__)
def cli():
    pass


@cli.command()
def syncdb():
    # Import here is necessary to make sqlalchemy see models defined under
    # models.py file.
    import smartanthill_status.models  # noqa
    create_all()


@cli.command()
def embedded_build_stats():
    parse_latest_builds_statistics()


@cli.command()
def runserver():
    app.run(reloader=True)


@cli.command()
@click.argument("file_path")
def parse_file(file_path):
    parse_log_file(file_path)


def main():
    # https://urllib3.readthedocs.org/en/latest/security.html#insecureplatformwarning
    requests.packages.urllib3.disable_warnings()

    cli()


if __name__ == "__main__":
    main()
