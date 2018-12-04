import os
import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.ext.ndb import metadata
from room import Rooms

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class AddRoom(webapp2.RequestHandler):

    def get(self):

        logout = users.create_logout_url('/')
        template_values = {
            'logout': logout,
            'error': '',
        }
        template = JINJA_ENVIRONMENT.get_template('addroom.html')
        self.response.write(template.render(template_values))

    def post(self):
        action = self.request.get('button')

        if action == 'add':
            room_name = self.request.get('name').lower()

            key = ndb.Key('Rooms', room_name)
            room = key.get()

            if room == None:
                room = Rooms(id=room_name)
                room.put()
                self.redirect('/displayrooms')

            else:
                logout = users.create_logout_url('/')
                template_values = {
                    'logout': logout,
                    'error': 'Sorry, a Room with that name exists..... Please use a unique name',
                }
                template = JINJA_ENVIRONMENT.get_template('addroom.html')
                self.response.write(template.render(template_values))
