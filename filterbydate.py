import webapp2
import jinja2
import os
from google.appengine.api import users
from room import Rooms
from google.appengine.ext import ndb
import datetime
import logging

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class FilterByDate(webapp2.RequestHandler):

  
    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        current_date_string = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")

        logout = users.create_logout_url('/')
        action = self.request.get('button')
        room_list = []
        booking_list = []
        start_list = []
        end_list = []
        error = ''
        if action == 'Filter By Date':
            template_values = {
                'current_date_string': current_date_string,
                'logout': logout,
                'room_list': room_list,
                'booking_list': booking_list,
                'start_list': start_list,
                'end_list': end_list,
                'error': error

            }

            template = JINJA_ENVIRONMENT.get_template('filterbydate.html')
            self.response.write(template.render(template_values))


        elif action == 'filter':

            filter_date = self.request.get('filter_date')

            filter_date = datetime.datetime.strptime(filter_date,"%Y-%m-%d")
            filter_date = filter_date.date()
            error = "There are no bookings for this date"
            room_list = []
            booking_list = []
            start_list = []
            end_list = []
            allrooms = Rooms.query().fetch()
            for room_index, eachroom in enumerate(allrooms):
                for booking_index, eachbooking in enumerate(eachroom.bookings):
                    start = eachbooking.startdate
                    start_d = start.date()
                    end = eachbooking.enddate
                    end_d = end.date()
                    if ((start_d < filter_date) & (end_d >= filter_date) | (start_d== filter_date)):
                        room_list.append(eachroom.key.id())
                        booking_list.append(eachbooking.reference)
                        start_list.append(start)
                        end_list.append(end)
                        error = ''

            all_lists = sorted(zip(start_list,room_list,booking_list,end_list))
            start_list1 = []
            room_list1 = []
            booking_list1 = []
            end_list1 = []
            for st,r,b,e in all_lists:
                start_list1.append(st.strftime("%d-%m-%Y %H:%M"))
                room_list1.append(r)
                booking_list1.append(b)
                end_list1.append(e.strftime("%d-%m-%Y %H:%M"))

            current_date_string = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
            
            template_values = {
                'allrooms': allrooms,
                'logout': logout,
                'room_list':room_list1,
                'booking_list':booking_list1,
                'start_list': start_list1,
                'end_list':end_list1,
                'current_date_string':current_date_string,
                'error': error
            }

            template = JINJA_ENVIRONMENT.get_template('filterbydate.html')
            self.response.write(template.render(template_values))


