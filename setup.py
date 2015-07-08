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

from setuptools import setup

from smartanthill_status import (
    __author__, __description__, __email__, __license__, __title__, __url__,
    __version__)

setup(
    name=__title__,
    version=__version__,
    packages=['smartanthill_status'],
    url=__url__,
    license=__license__,
    author=__author__,
    author_email=__email__,
    description=__description__,
    entry_points={
        'console_scripts': [
            "smartanthill-status = smartanthill_status.__main__:main",
        ],
    },
    install_requires=[
        "click",
        "bottle",
        "SQLAlchemy",
        "mysql-connector-python",
        "requests",
    ],
)
