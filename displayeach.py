import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb
from room import Rooms

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class DisplayEach(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        action = self.request.get('button')
        if action == 'delete':
            room_id = self.request.get('room_id')
            booking_reference = self.request.get('booking_reference')
            key = ndb.Key('Rooms', room_id)
            room = key.get()
            logout = users.create_logout_url('/')
            for index, eachbooking in enumerate(room.bookings):
                if eachbooking.reference == booking_reference:
                    del room.bookings[index]
                    room.put()
                    template_values = {
                        'room': room,
                        'logout': logout,
                        'bookings': room.bookings
                    }

                    template = JINJA_ENVIRONMENT.get_template('displayeach.html')
                    self.response.write(template.render(template_values))
        else:
            name = self.request.get('name')
            key = ndb.Key('Rooms', name)
            room = key.get()
            list_of_bookings = room.bookings
            starts = [eachbooking.startdate for eachbooking in room.bookings]
            bookings = [x for y, x in sorted(zip(starts, list_of_bookings))]
            logout = users.create_logout_url('/')

            template_values = {
                'room': room,
                'logout': logout,
                'bookings': bookings

            }

            template = JINJA_ENVIRONMENT.get_template('displayeach.html')
            self.response.write(template.render(template_values))
