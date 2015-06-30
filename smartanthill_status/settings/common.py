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

import os.path

import requests

from smartanthill_status import __version__

PACKAGE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASE_URI = ""

HEADERS = {
    'User-Agent': "smartanthill_status/%(version)s %(default)s"
                  % {'version': __version__,
                     'default': requests.utils.default_user_agent()},
    'Accept': "application/vnd.travis-ci.2+json",
}

REPO_BASE_URI = \
    "https://api.travis-ci.org/repos/smartanthill/smartanthill2_0-embedded"

JOB_LOG_URL = \
    'https://s3.amazonaws.com/archive.travis-ci.org/jobs/%(job_id)s/log.txt'
