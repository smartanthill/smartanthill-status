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

from smartanthill_status.utils import iter_lines


def test_iter_lines():
    def chunk_generator():
        yield 'line #1\n'
        yield 'line #2\nline #3'
        yield '\nline #4 part 1'
        yield '; line #4 part 2'

    lines = list(iter_lines(chunk_generator()))
    expected_lines = [
        'line #1',
        'line #2',
        'line #3',
        'line #4 part 1; line #4 part 2',
    ]
    assert lines == expected_lines
