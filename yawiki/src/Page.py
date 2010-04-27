from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import cgi


'''
Created on 26.04.2010

@author: alarin
'''

class Page(db.Model):
    '''wiki page'''
    
    title = db.StringProperty(multiline=False)
    content = db.StringProperty(multiline=True)
    children = db.ListProperty(db.Key)
    level = db.IntegerProperty(default=0)