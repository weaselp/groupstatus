import statusdb
from django.conf import settings
from django.utils.html import conditional_escape
from django.utils.http import urlquote

import sqlalchemy
import sqlalchemy.orm

import re

engine = sqlalchemy.create_engine(settings.DATABASE_ENGINE)
Session = sqlalchemy.orm.sessionmaker(bind=engine)


class DBTag(statusdb.DBTag):
    pass

class DBMessage(statusdb.DBMessage):
    def msgHTML(self):
        msg = conditional_escape(self.message)
        msg = re.sub('#([a-zA-Z0-9_+/-]+)', '<a href="/tag/\\1">\g<0></a>',
            msg)
        return msg

