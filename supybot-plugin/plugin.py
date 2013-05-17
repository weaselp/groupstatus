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

import re

class GroupStatusDB():
    def __init__(self):
        pass

    def add(self, tgt, nick, payload):
        print "Adding %s,%s,%s"%(tgt, nick, payload)

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
            if not re.match('status:', payload, re.IGNORECASE): return
            if not self._checkAuthed(irc, nick):
                irc.error("You need to be in one of the authentication channels for your message to get recorded.  Please ask the bot operator which channels these are.")
            else:
                self.db.add(tgt, nick, payload)

Class = GroupStatus
