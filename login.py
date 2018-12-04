import webapp2
import jinja2
import os
from google.appengine.api import users
from displayrooms import DisplayRooms
from addroom import AddRoom
from addbooking import AddBooking
from displayeach import DisplayEach
from filterbydate import FilterByDate

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class Login(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        url = ''
        url_string = ''
        user = users.get_current_user()

        if user:
            self.redirect('/displayrooms')
            logout = users.create_logout_url(self.request.uri)
            template_values = {
                'logout': logout
            }
            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
        else:
            self.redirect(users.create_login_url(self.request.uri))


app = webapp2.WSGIApplication([
    ('/', Login),
    ('/displayrooms', DisplayRooms),
    ('/addroom', AddRoom),
    ('/addbooking', AddBooking),
    ('/displayeach', DisplayEach),
    ('/filterbydate', FilterByDate)
], debug=True)
