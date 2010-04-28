'''
Created on 28.04.2010

@author: alarin
'''
from Page import Page
from WikiSettingsModels import *
from google.appengine.api import users
from google.appengine.ext import db, webapp
from google.appengine.ext.db import djangoforms
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
import cgi

import os

class WikiSettings(webapp.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), os.sep.join(['templates','wikisettings.html']))
        self.response.out.write(template.render(path, template_values))
        
class WikiPageNestingSetting(webapp.RequestHandler):
    def get(self):
        setting = db.GqlQuery("SELECT * FROM PageNestingSetting" ).get()
        template_values = {"page_edit_form":PageNestingSettingForm(instance=setting)}
        path = os.path.join(os.path.dirname(__file__), os.sep.join(['templates','wikiedit.html']))
        self.response.out.write(template.render(path, template_values))
        
    def post(self):
        setting = db.GqlQuery("SELECT * FROM PageNestingSetting" ).get()
        instance = None
        if setting:
            instance = setting
        data_dict = self.request.POST
        data = PageNestingSettingForm(data=data_dict, instance=instance)
        if data.is_valid():
            entity = data.save(commit=True)
            self.redirect("/settings/nesting/")
        else:
            template_values = {"page_edit_form":data}
            path = os.path.join(os.path.dirname(__file__), os.sep.join(['templates','wikiedit.html']))
            self.response.out.write(template.render(path, template_values))
        
class WikiPageFormattingSetting(webapp.RequestHandler):
    def get(self):
        settings = PageFormattingSetting.all()
        template_values = {"formats":settings, "format_add_form":PageFormattingSettingForm()}
        path = os.path.join(os.path.dirname(__file__), os.sep.join(['templates','wikiformat.html']))
        self.response.out.write(template.render(path, template_values))
        
    def post(self):
        data = PageFormattingSettingForm(data=self.request.POST)
        if data.is_valid():
            entity = data.save(commit=True)
            self.redirect("/settings/format/")
        else:
            template_values = {"format_add_form":data}
            path = os.path.join(os.path.dirname(__file__), os.sep.join(['templates','wikiformat.html']))
            self.response.out.write(template.render(path, template_values))