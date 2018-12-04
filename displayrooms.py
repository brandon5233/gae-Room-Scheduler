import webapp2
import jinja2
import os
from google.appengine.api import users
from room import Rooms
from google.appengine.ext import ndb
import datetime
from booking import Bookings

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class DisplayRooms(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        allrooms = Rooms.query().order(Rooms.key).fetch()
        logout = users.create_logout_url('/')
        current_time = datetime.datetime.now()
        current_date_string = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")

        deletedbookings = 0
        #SPECIAL FEATURE: AUTO_DELETE ELAPSED BOOKINGS
        for eachroom in allrooms:
            for index, eachbooking in enumerate(eachroom.bookings):
                if eachbooking.enddate < current_time:
                    del eachroom.bookings[index]
                    deletedbookings = deletedbookings+1
                    eachroom.put()


        template_values = {
            'allrooms': allrooms,
            'logout': logout,
            'error': '',
            'deletedbookings': deletedbookings,
            'current_date_string': current_date_string
        }

        template = JINJA_ENVIRONMENT.get_template('displayrooms.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        current_time = datetime.datetime.now()
        allrooms = Rooms.query().fetch()

        deletedbookings = 0
        # SPECIAL FEATURE: AUTO_DELETE ELAPSED BOOKINGS
        for eachroom in allrooms:
            for index, eachbooking in enumerate(eachroom.bookings):
                if eachbooking.enddate < current_time:
                    del eachroom.bookings[index]
                    deletedbookings = deletedbookings+1
                    eachroom.put()


        error = ''
        action = self.request.get('button')
        if action == 'delete room':
            room_id = self.request.get('room_id')
            room_key = ndb.Key('Rooms', room_id)
            room_in_question = room_key.get()

            if room_in_question.bookings == []:
                room_key.delete()
                self.redirect('/displayrooms')

            else:
                error = 'Cannot delete room while it contains bookings'

        logout = users.create_logout_url('/')
        allrooms = Rooms.query().order(Rooms.key).fetch()

        template_values = {
            'allrooms': allrooms,
            'logout': logout,
            'error': error,
            'deletedbookings': deletedbookings
        }

        template = JINJA_ENVIRONMENT.get_template('displayrooms.html')
        self.response.write(template.render(template_values))
