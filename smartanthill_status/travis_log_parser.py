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

import logging
import re

from requests.sessions import Session
from sqlalchemy.sql.expression import exists

from smartanthill_status.database import db_session
from smartanthill_status.models import BuildStatistics
from smartanthill_status.settings import HEADERS, JOB_LOG_URL, REPO_BASE_URI
from smartanthill_status.utils import iter_lines, rollback_on_exception

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


BEGINNING_OF_LINE_WITH_ENV_NAME_REGEX = \
    re.compile("^\[\w{3} \w{3} \d{2} \d{2}:\d{2}:\d{2} \d{4}\]")
ENV_NAME_REGEX = \
    re.compile("Processing \x1b\[36m\x1b\[1m(.*)\x1b\[0m")
BLOCK_END_LINE_REGEX = \
    re.compile("^=+")


AVR_MEMORY_USAGE_BLOCK_REGEX = re.compile("^\"avr-size\"")
AVR_ROM_REGEX = \
    re.compile("^Program: +(\d+) bytes \(\d{1,3}\.\d{1,2}% Full\)\x1b\[0m")
AVR_RAM_REGEX = \
    re.compile("^Data: +(\d+) bytes \(\d{1,3}\.\d{1,2}% Full\)\x1b\[0m")

OTHER_MEMORY_USAGE_BLOCK_REGEX = re.compile("^\"[a-z0-9\-]+(?<!avr)-size\"")
OTHER_ROM_AND_RAM_REGEX = \
    re.compile("(?P<text>\d+)\s+(?P<data>\d+)\s+(?P<bss>\d+)\s+")


class InvalidStateTransition(Exception):
    pass


class States(object):
    NOT_IN_BLOCK = "NOT_IN_BLOCK"
    IN_ENVIRONMENT_BLOCK = "IN_ENVIRONMENT_BLOCK"
    IN_AVR_MEMORY_USAGE_BLOCK = "IN_AVR_MEMORY_USAGE_BLOCK"
    IN_OTHER_MEMORY_USAGE_BLOCK = "IN_MSP430_MEMORY_USAGE_BLOCK"


class LogParser(object):

    ALLOWED_TRANSITIONS = {
        States.NOT_IN_BLOCK: [States.IN_ENVIRONMENT_BLOCK],
        States.IN_ENVIRONMENT_BLOCK: [States.IN_AVR_MEMORY_USAGE_BLOCK,
                                      States.IN_OTHER_MEMORY_USAGE_BLOCK,
                                      States.NOT_IN_BLOCK],
        States.IN_AVR_MEMORY_USAGE_BLOCK: [States.IN_ENVIRONMENT_BLOCK],
        States.IN_OTHER_MEMORY_USAGE_BLOCK: [States.IN_ENVIRONMENT_BLOCK],
    }

    def __init__(self, file_obj):
        self.file_obj = file_obj
        self._state = States.NOT_IN_BLOCK
        self.env = None

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        if new_state not in self.ALLOWED_TRANSITIONS[self.state]:
            raise InvalidStateTransition()
        if self.env:
            prefix = "%s:" % self.env
        else:
            prefix = ""
        logging.debug("%sTransition from %s to %s"
                      % (prefix, self.state, new_state))
        self._state = new_state

    def parse(self):
        """Performs log parsing.

        :rtype: list of BuildStatistics
        """
        statistics_records = []
        for line in iter_lines(self.file_obj):
            if self.state == States.NOT_IN_BLOCK:
                if BEGINNING_OF_LINE_WITH_ENV_NAME_REGEX.match(line):
                    env = ENV_NAME_REGEX.search(line).group(1)
                    self.env = env
                    self.state = States.IN_ENVIRONMENT_BLOCK
                    record = BuildStatistics(env=env)

            elif self.state == States.IN_ENVIRONMENT_BLOCK:

                if AVR_MEMORY_USAGE_BLOCK_REGEX.match(line):
                    self.state = States.IN_AVR_MEMORY_USAGE_BLOCK

                elif OTHER_MEMORY_USAGE_BLOCK_REGEX.match(line):
                    self.state = States.IN_OTHER_MEMORY_USAGE_BLOCK

                elif BLOCK_END_LINE_REGEX.match(line):
                    self.state = States.NOT_IN_BLOCK
                    self.env = None
                    if 'SUCCESS' in line:
                        statistics_records.append(record)

            elif self.state == States.IN_AVR_MEMORY_USAGE_BLOCK:
                if not record.rom:
                    rom_match = AVR_ROM_REGEX.match(line)
                    if rom_match:
                        record.rom = int(rom_match.group(1))
                elif not record.ram:
                    ram_match = AVR_RAM_REGEX.match(line)
                    if ram_match:
                        record.ram = int(ram_match.group(1))

                if record.rom and record.ram:
                    self.state = States.IN_ENVIRONMENT_BLOCK

            elif self.state == States.IN_OTHER_MEMORY_USAGE_BLOCK:
                match = OTHER_ROM_AND_RAM_REGEX.match(line)
                if match:
                    result = match.groupdict()
                    data = int(result['data'])
                    text = int(result['text'])
                    bss = int(result['bss'])
                    record.rom = text + data
                    record.ram = data + bss
                    self.state = States.IN_ENVIRONMENT_BLOCK

        assert self.state == States.NOT_IN_BLOCK, "Invalid state"
        return statistics_records


def parse_log_file(filename):
    with open(filename, "r") as f:
        parser = LogParser(f)
        return parser.parse()


def parse_latest_builds_statistics():
    requests_session = Session()
    requests_session.headers.update(HEADERS)
    response = requests_session.get(REPO_BASE_URI + "/builds",
                                    params={'event_type': "push"}).json()
    commits = {commit['id']: commit for commit in response['commits']}

    def build_is_from_develop_branch(build):
        return 'develop' == commits[build['commit_id']]['branch']

    def build_exists_in_database(build):
        return db_session.query(exists().where(
            BuildStatistics.build_id == build['id'])).scalar()

    for build in response['builds']:
        with rollback_on_exception(db_session, logger):
            if not build_is_from_develop_branch(build) \
                    or build_exists_in_database(build):
                continue
            job_id = build['job_ids'][0]
            log = requests_session.get(JOB_LOG_URL % {'job_id': job_id},
                                       stream=True)
            log_parser = LogParser(log)
            records = log_parser.parse()
            for record in records:
                record.build_id = build['id']
                record.job_id = job_id
            db_session.add_all(records)
            db_session.commit()
            logger.debug('%s statistics records saved.' % len(records))
