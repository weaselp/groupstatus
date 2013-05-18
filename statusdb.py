#!/usr/bin/python

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
    ts = sqlalchemy.Column(sqlalchemy.types.DateTime, default=datetime.datetime.utcnow)
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

