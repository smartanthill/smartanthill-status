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

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.mysql import INTEGER

from smartanthill_status.database import Base


class BuildStatistics(Base):
    __tablename__ = "build_statistics"
    id = Column(INTEGER(unsigned=True), primary_key=True)

    build_id = Column(INTEGER(unsigned=True), nullable=False)
    job_id = Column(INTEGER(unsigned=True), nullable=False)
    committed_at = Column(DateTime, nullable=False)

    env = Column(String(10), nullable=False)
    rom = Column(INTEGER(unsigned=True), nullable=False)
    ram = Column(INTEGER(unsigned=True), nullable=False)

    def to_dict(self):
        d = {key: getattr(self, key)
             for key in ['build_id', 'rom', 'ram', 'env']}
        d['committed_at'] = self.committed_at.isoformat()
        return d
