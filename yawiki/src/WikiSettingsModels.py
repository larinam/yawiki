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

class PageMacrosSettingMacrosValidator:
    def __call__(self, value):
        try:
            eval(value)
        except:
            raise ValueError('Item content "%s" is not acceptable. Shold be evaluated with "eval" function.' % value)


class PageNestingSetting(db.Model):
    value = db.IntegerProperty(default=1, required=True)
    
class PageNestingSettingForm(djangoforms.ModelForm):
    class Meta:
        model = PageNestingSetting
        exclude = []
        
class PageFormattingSetting(db.Model):
    pattern = db.StringProperty(multiline=False, required=True) #human readable 
    regex_pattern = db.StringProperty(multiline=False, required=True) #regex pattern
    target = db.StringProperty(multiline=False, required=True) #target replacement
    
class PageFormattingSettingForm(djangoforms.ModelForm):
    class Meta:
        model = PageFormattingSetting
        exclude = []
    
class PageMacrosSetting(db.Model):
    label = db.StringProperty(multiline=False, required=True)
    macros = db.StringProperty(multiline=True, validator=PageMacrosSettingMacrosValidator())
    
class PageMacrosSettingForm(djangoforms.ModelForm):
    class Meta:
        model = PageMacrosSetting
        exclude = []