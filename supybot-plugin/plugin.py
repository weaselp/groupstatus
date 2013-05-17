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

import supybot.utils as utils
from supybot.commands import *
import supybot.conf as conf
import supybot.plugins as plugins
import supybot.ircmsgs as ircmsgs
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks

import sqlalchemy
import sqlalchemy.orm

import re

import statusdb
reload(statusdb)

class GroupStatusDB():
    def init_db(self, irc):
        if self.db_initialized: return True

        cs = str(conf.supybot.plugins.GroupStatus.get('databaseConnectString'))
        if cs == "":
            irc.error("No databaseConnectString configured yet")
            return False
        try:
            engine = sqlalchemy.create_engine(cs)
            engine.execute('select 1').scalar()
            self.Session = sqlalchemy.orm.sessionmaker(bind=engine)
        except Exception, e:
            print e
            irc.error("An error occurred connecting to the db.  There might be something on the console.")
            return False
        self.db_initialized = True
        return True

    def __init__(self):
        self.db_initialized = False

    def add(self, irc, tgt, nick, payload):
        if not self.init_db(irc): return

        try:
            m = statusdb.DBMessage(tgt, nick, payload)
            session = self.Session()
            session.add(m)
            m.tag(session)
            session.commit()
        except Exception, e:
            print e
            irc.error("An error occurred.  There might be something on the console.")

class GroupStatus(callbacks.Plugin):
    def __init__(self, irc):
        self.__parent = super(GroupStatus, self)
        self.__parent.__init__(irc)
        self.db = GroupStatusDB()

    def _checkAuthed(self, irc, nick):
        ac = str(conf.supybot.plugins.GroupStatus.get('authChannel')).split()
        for c in ac:
            if nick in irc.state.channels[c].users: return True
        return False

    def doPrivmsg(self, irc, msg):
        if irc.isChannel(msg.args[0]):
            (tgt, payload) = msg.args
            nick = msg.nick
            m = re.match('status:\s*(.*)', payload, re.IGNORECASE)
            if m is None: return
            if not self._checkAuthed(irc, nick):
                irc.error("You need to be in one of the authentication channels for your message to get recorded.  These are: %s"%(str(conf.supybot.plugins.GroupStatus.get('authChannel')),))
            else:
                self.db.add(irc, tgt, nick, m.group(1))

Class = GroupStatus
