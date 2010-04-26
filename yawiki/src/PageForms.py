from Page import Page
from google.appengine.api import users
from google.appengine.ext import db, db, webapp, webapp
from google.appengine.ext.db import djangoforms
from google.appengine.ext.webapp import template, template
from google.appengine.ext.webapp.util import run_wsgi_app, run_wsgi_app
import cgi
import os


'''
Created on 26.04.2010

@author: alarin
'''
class PageEditForm(djangoforms.ModelForm):
    class Meta:
        model = Page
        exclude = ['children']