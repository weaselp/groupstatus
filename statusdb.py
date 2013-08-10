#!/usr/bin/python

###
# Copyright (c) 2013, Peter Palfrader <peter@palfrader.org>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
###

import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm
import sqlalchemy.types

import datetime
import re


Base = sqlalchemy.ext.declarative.declarative_base()

DBmessage_tag = sqlalchemy.Table('message_tag', Base.metadata,
    sqlalchemy.Column('message_id', sqlalchemy.types.Integer, sqlalchemy.ForeignKey('message.message_id')),
    sqlalchemy.Column('tag_id', sqlalchemy.types.Integer, sqlalchemy.ForeignKey('tag.tag_id'))
)

class DBTag(Base):
    __tablename__ = 'tag'

    tag_id = sqlalchemy.Column(sqlalchemy.types.Integer, primary_key=True)
    tag = sqlalchemy.Column(sqlalchemy.types.String)
    url = sqlalchemy.Column(sqlalchemy.types.String)

    def __init__(self, tag, url=None):
        self.tag = tag
        if url is not None:
            self.url = url
        else:
            m = re.match('#([0-9]+)$', tag)
            if m:
                self.url = 'http://bugs.torproject.org/%s'%(m.group(1))

class DBMessage(Base):
    __tablename__ = 'message'

    message_id = sqlalchemy.Column(sqlalchemy.types.Integer, primary_key=True)
    ts = sqlalchemy.Column(sqlalchemy.types.DateTime, default=datetime.datetime.now)
    channel = sqlalchemy.Column(sqlalchemy.types.String)
    person = sqlalchemy.Column(sqlalchemy.types.String)
    message = sqlalchemy.Column(sqlalchemy.types.String)

    tags = sqlalchemy.orm.relationship('DBTag', secondary=DBmessage_tag, backref='messages')

    def __init__(self, channel, person, message, ts=None):
        self.channel = channel
        self.person = person
        self.message = message
        self.ts = ts

    def tag(self, session, tags=None):
        if tags is None:
            tags = re.findall('#[a-zA-Z0-9_+/-]+', self.message)

        done = {}
        for t in tags:
            if t in done: continue
            done[t] = True

            rows = session.query(DBTag).filter_by(tag=t)[0:1]
            if len(rows) > 0:
                self.tags.append(rows[0])
            else:
                self.tags.append(DBTag(t))


if __name__ == "__main__":
    import os
    engine = sqlalchemy.create_engine(os.getenv('CONNECT_STRING'))
    engine.execute('select 1').scalar()
    Session = sqlalchemy.orm.sessionmaker(bind=engine)

    session = Session()
    m = DBMessage('#test', 'weasel', 'bla #123 #blubb #fa asdf ')
    session.add(m)
    m.tag(session)
    session.commit()

