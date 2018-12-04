import os
import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import users
from room import Rooms
from booking import Bookings
import datetime
import logging

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class AddBooking(webapp2.RequestHandler):

    def post(self):
        action = self.request.get('button')
        rooms = Rooms.query().fetch()
        error = ''

        if action == 'Add Booking':
            room_id = self.request.get('room_id')


        if action == 'add':
            reference = self.request.get('booking_reference')
            reference = reference.lower()
            current_time_from_html = self.request.get("current_time_from_html")
            current_time_from_html = datetime.datetime.strptime(current_time_from_html,"%d-%m-%Y %H:%M")
            room_id = self.request.get('room_id')
            key = ndb.Key('Rooms', room_id)
            room = key.get()

            for eachbooking in room.bookings:
                if eachbooking.reference == reference:
                    error = "Booking already exists, please use a unique reference"

            if error == '':
                startdate = self.request.get('startdate')
                enddate = self.request.get('enddate')

                sdate = datetime.datetime.strptime(startdate, "%Y-%m-%dT%H:%M")
                if sdate < current_time_from_html:
                    error = "Start Date is before Current Date... Please choose a date and time in the future"
                else:
                    edate = datetime.datetime.strptime(enddate, "%Y-%m-%dT%H:%M")

                    if (sdate == edate):
                        error = "start and end date are the same"
                    else:
                        if sdate > edate:
                            error = "start date is after the end date"
                        else:
                            for eachbooking in room.bookings:
                                if (((eachbooking.startdate <= sdate) & (eachbooking.enddate >= sdate)) | (
                                        (eachbooking.startdate <= edate) & (eachbooking.enddate >= sdate))):
                                    error = "booking within this period already exists"

                            if error == '':
                                b = Bookings()
                                b.reference = self.request.get('booking_reference')
                                b.startdate = sdate
                                b.enddate = edate

                                room.bookings.append(b)
                                room.put()
                                self.redirect('/displayrooms')

        logout = users.create_logout_url('/')
        current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
        template_values = {
            'logout': logout,
            'error': error,
            'room_id': room_id,
            'current_time': current_time

        }
        template = JINJA_ENVIRONMENT.get_template('addbooking.html')
        self.response.write(template.render(template_values))
