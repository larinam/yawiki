import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from Page import Page
from PageForms import PageEditForm
from google.appengine.api import users
from google.appengine.ext import db, db, webapp, webapp
from google.appengine.ext.db import djangoforms
from google.appengine.ext.webapp import template, template
from google.appengine.ext.webapp.util import run_wsgi_app, run_wsgi_app
import cgi




class MainPage(webapp.RequestHandler):
    
    
    def get(self, p):
        if p=="":
            template_values = {"pages":db.GqlQuery("SELECT * FROM Page WHERE level=0")}
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
                template_values = {"pages":db.GqlQuery("SELECT * FROM Page WHERE level=%d" % ((page.level or 0) + 1)),
                                   "content":page.content, "title":page.title, 'up':up}
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
        data_dict.update({'level':p.count('/')})
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
        page = db.GqlQuery("SELECT * FROM Page WHERE title='%s'" % (p)).get()
        page.delete()
        self.redirect('/')
        
application = webapp.WSGIApplication([(r'^/add_page/(.*)$', AddPage),
                                      (r'/del_page/(.*)$', DeletePage),
                                      (r'/(.*)', MainPage),
                                      ],
                                      debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
