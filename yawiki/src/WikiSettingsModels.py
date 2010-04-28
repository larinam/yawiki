'''
Created on 28.04.2010

@author: alarin
'''
from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.db import djangoforms
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
import cgi
import os

class PageNestingSetting(db.Model):
    value = db.IntegerProperty(default=1)
    
class PageNestingSettingForm(djangoforms.ModelForm):
    class Meta:
        model = PageNestingSetting
        exclude = []
        
class PageFormattingSetting(db.Model):
    pattern = db.StringProperty(multiline=False)
    target = db.StringProperty(multiline=False)
    
class PageFormattingSettingForm(djangoforms.ModelForm):
    class Meta:
        model = PageFormattingSetting
        exclude = []
    
class PageMacrosSetting(db.Model):
    label = db.StringProperty(multiline=False)
    macros = db.StringProperty(multiline=True)
    
class PageMacrosSettingForm(djangoforms.ModelForm):
    class Meta:
        model = PageMacrosSetting
        exclude = []