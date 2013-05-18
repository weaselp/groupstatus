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

from django.http import HttpResponse
from django.shortcuts import render
from django.http import Http404

import models
import sqlalchemy, sqlalchemy.orm

from models import DBMessage, DBTag

session = models.Session()

def home(request):
    try:
        m = session.query(DBMessage).order_by(DBMessage.ts.desc()).all()
        return render(request, 'home.html',
            { 'msgs': m }
            )
    finally:
        session.rollback()

def tag(request, tagname):
    try:
        tagname = '#' + tagname
        rows = session.query(DBTag).filter_by(tag=tagname)[0:1]
        if len(rows) == 0:
            raise Http404
        t = rows[0]
        m = session.query(DBMessage).filter(DBMessage.tags.any(tag=tagname)).order_by(DBMessage.ts.desc()).all()
        return render(request, 'tag.html',
            { 'tag': t, 'msgs': m }
            )
    finally:
        session.rollback()

def person(request, personname):
    try:
        m = session.query(DBMessage).filter_by(person=personname).order_by(DBMessage.ts.desc()).all()
        if len(m) == 0:
            raise Http404
        return render(request, 'person.html',
            { 'msgs': m, 'person': personname }
            )
    finally:
        session.rollback()
