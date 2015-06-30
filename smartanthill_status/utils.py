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

from contextlib import contextmanager


@contextmanager
def rollback_on_exception(session, logger=None):
    try:
        yield
    except Exception as e:
        session.rollback()
        if logger is not None:
            logger.exception(e)


def iter_lines(container):
    """Yields content line by line.

    Useful for processing streamed data.
    """
    line = ''
    for chunk in container:
        if '\n' in chunk:
            left, chunk = chunk.split('\n', 1)
            yield line + left
            line = ''
        while '\n' in chunk:
            left, chunk = chunk.split('\n', 1)
            yield left
        if chunk:
            line += chunk
    if line:
        yield line
