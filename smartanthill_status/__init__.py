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
import os
import json
import logging
import logging.config


__version__ = "0.0.1"

__title__ = "smartanthill-status"
__description__ = "Misc status information about SmartAnthill Project"
__url__ = "https://github.com/smartanthill/smartanthill-status"

__author__ = "OLogN Technologies AG"
__email__ = "info@o-log-n.com"

__license__ = "GNU GPL v2.0"
__copyright__ = "Copyright (c) 2015, OLogN Technologies AG"


def _get_user_agent():
    result = "smartanthill_status/%s" % __version__
    try:
        import requests
        result += " %s" % requests.utils.default_user_agent()
    except ImportError:
        pass
    return result


config = dict(
    SQLALCHEMY_DATABASE_URI=None,
    HEADERS={
        'User-Agent': _get_user_agent(),
        'Accept': "application/vnd.travis-ci.2+json",
    },
    REPO_BASE_URI="https://api.travis-ci.org/repos/"
                  "smartanthill/smartanthill2_0-embedded",
    JOB_LOG_URL="https://s3.amazonaws.com/archive.travis-ci.org"
                "/jobs/%(job_id)s/log.txt",
    DEBUG=False,
    API_CORS_ORIGIN="*",
    LOGGING=dict(version=1),
)

assert "SMARTANTHILL_STATUS_CONFIG_PATH" in os.environ
with open(os.environ.get("SMARTANTHILL_STATUS_CONFIG_PATH")) as f:
    config.update(json.load(f))

logging.getLogger(__name__).addHandler(logging.NullHandler())
logging.config.dictConfig(config['LOGGING'])
