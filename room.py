from google.appengine.ext import ndb
from booking import Bookings


class Rooms(ndb.Model):
    bookings = ndb.StructuredProperty(Bookings, repeated=True)
