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
