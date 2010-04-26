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
            page = db.GqlQuery("SELECT * FROM Page WHERE title='%s'" % (p))
            template_values = {"pages":db.GqlQuery("SELECT * FROM Page WHERE level=0"), "content":page.get().content}
            path = os.path.join(os.path.dirname(__file__), os.sep.join(['templates','wikimain.html']))
            self.response.out.write(template.render(path, template_values))

class AddPage(webapp.RequestHandler):
    def get(self):
        template_values = {"page_edit_form":PageEditForm()}
        path = os.path.join(os.path.dirname(__file__), os.sep.join(['templates','wikiedit.html']))
        self.response.out.write(template.render(path, template_values))
        
    def post(self):
        data = PageEditForm(data=self.request.POST)
        if data.is_valid():
            # Save the data, and redirect to the view page
            entity = data.save(commit=True)
            #entity.added_by = users.get_current_user()
            #entity.put()
            self.redirect('/')
        else:
            template_values = {"page_edit_form":data}
            path = os.path.join(os.path.dirname(__file__), os.sep.join(['templates','wikiedit.html']))
            self.response.out.write(template.render(path, template_values))
        
application = webapp.WSGIApplication([('/add_page/', AddPage),
                                      (r'/(.*)', MainPage),
                                      ],
                                      debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
