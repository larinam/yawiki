import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import re
from Page import Page
from PageForms import PageEditForm
from google.appengine.api import users
from google.appengine.ext import db, db, webapp, webapp
from google.appengine.ext.db import djangoforms
from google.appengine.ext.webapp import template, template
from google.appengine.ext.webapp.util import run_wsgi_app, run_wsgi_app
import cgi
from WikiSettings import WikiSettings, WikiPageNestingSetting, WikiPageFormattingSetting, WikiPageMacrosSetting, WikiPageMacrosSettingDel
from WikiSettingsModels import PageNestingSetting, PageMacrosSetting, PageFormattingSetting


def filterPagesLevel(pages, current_level):
    new_pages = []
    for i in pages:
        if i.level >= current_level + 1 and i.level < current_level + 1 + PageNestingSetting.all().get().value:
            new_pages.append(i)
    return new_pages

def replace_words(text, word_dic):
    """
    take a text and replace words that match a key in a dictionary with
    the associated value, return the changed text
    """
    rc = re.compile('|'.join(map(re.escape, word_dic)))
    def translate(match):
        return word_dic[match.group(0)]
    return rc.sub(translate, text)

def applyMacroses(s):
    macroses = PageMacrosSetting.all()
    word_dic = {}
    for m in macroses:
        word_dic.update({m.label:str(eval(m.macros))})
    if word_dic: 
        return replace_words(s, word_dic) 
    else: 
        return s

def applyFormatting(s):
    formats = PageFormattingSetting.all()
    return s
    
def applySettingsToContent(s):
    s = applyMacroses(s)
    s = applyFormatting(s)
    return s

class MainPage(webapp.RequestHandler):
    def get(self, p):
        if p=="":
            nestingSetting = PageNestingSetting.all().get()
            if not nestingSetting:
                nestingSetting = 1
            template_values = {"pages":db.GqlQuery("SELECT * FROM Page WHERE level<%d" % (nestingSetting)), "title":""}
            path = os.path.join(os.path.dirname(__file__), os.sep.join(['templates','wikimain.html']))
            self.response.out.write(template.render(path, template_values))
        else:
            if p[-1]=='/':p = p[:-1]
            page = db.GqlQuery("SELECT * FROM Page WHERE title='%s'" % (p)).get()
            if page == None:
                self.redirect("/add_page/?title=%s" % (p))
            else:
                up = page.title.rsplit('/',1)
                if len(up) == 1:
                    up = '#'
                else:
                    up = page.title.rsplit('/',1)[0]
                template_values = {"pages":filterPagesLevel(db.GqlQuery("SELECT * FROM Page WHERE title>='%s' and title<'%s'" % (p,p+ u"\ufffd")), page.level),
                                   "content":applySettingsToContent(page.content), "title":page.title, 'up':up}
                path = os.path.join(os.path.dirname(__file__), os.sep.join(['templates','wikimain.html']))
                self.response.out.write(template.render(path, template_values))
            
class AddPage(webapp.RequestHandler):
    def get(self, p):
        if p and p[-1]=='/':
            p = p[:-1]
        page = db.GqlQuery("SELECT * FROM Page WHERE title='%s'" % (p)).get()
        instance = None
        if page != None:
            instance = page
        initial = {}
        if self.request.get('title', ""):
            initial.update(dict(title=self.request.get('title', "")));
            
        template_values = {"page_edit_form":PageEditForm(initial=initial, instance=instance)}
        path = os.path.join(os.path.dirname(__file__), os.sep.join(['templates','wikiedit.html']))
        self.response.out.write(template.render(path, template_values))
        
    def post(self, p):
        if p and p[-1]=='/':
            p = p[:-1]
        page = db.GqlQuery("SELECT * FROM Page WHERE title='%s'" % (p)).get()
        instance = None
        if page != None:
            instance = page
        data_dict = self.request.POST
        data_dict.update({'level':data_dict.get('title','').count('/')})
        data = PageEditForm(data=data_dict, instance=instance)
        if data.is_valid():
            # Save the data, and redirect to the view page
            entity = data.save(commit=True)
            self.redirect('/'+self.request.POST.get("title"))
        else:
            template_values = {"page_edit_form":data}
            path = os.path.join(os.path.dirname(__file__), os.sep.join(['templates','wikiedit.html']))
            self.response.out.write(template.render(path, template_values))
            
class DeletePage(webapp.RequestHandler):
    def get(self, p):
        if p and p[-1]=='/':
            p = p[:-1]
        subpages = db.GqlQuery("SELECT * FROM Page WHERE title>='%s' and title<'%s'" % 
                                                       (p, p+ u"\ufffd"))
        page = db.GqlQuery("SELECT * FROM Page WHERE title='%s'" % (p)).get()
        page.delete()
        for p in subpages:
            p.delete()
        self.redirect('/')
        
application = webapp.WSGIApplication([(r'^/add_page/(.*)$', AddPage),
                                      (r'/del_page/(.*)$', DeletePage),
                                      (r'/settings/$', WikiSettings),
                                      (r'/settings/nesting/$', WikiPageNestingSetting),
                                      (r'/settings/format/$', WikiPageFormattingSetting),
                                      (r'/settings/macros/$', WikiPageMacrosSetting),
                                      (r'/settings/macros/del/(\d*)$', WikiPageMacrosSettingDel),
                                      (r'/settings/$', WikiSettings),
                                      (r'/(.*)', MainPage),
                                      ],
                                      debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
