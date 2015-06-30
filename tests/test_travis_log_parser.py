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

from smartanthill_status.travis_log_parser import parse_log_file


def test_log_parser_avr_size_result():
    filename = os.path.join(os.path.dirname(__file__), 'log_avr.txt')
    result = parse_log_file(filename)
    assert 1 == len(result)
    record = result[0]
    assert 'uno' == record.env
    assert 11124 == record.rom
    assert 452 == record.ram


def test_log_parser_other_size_result():
    filename = os.path.join(os.path.dirname(__file__), 'log_msp430.txt')
    result = parse_log_file(filename)
    assert 1 == len(result)
    record = result[0]
    assert 'msp430' == record.env
    assert 14846 == record.rom
    assert 430 == record.ram
