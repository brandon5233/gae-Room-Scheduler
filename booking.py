from google.appengine.ext import ndb


class Bookings(ndb.Model):
    reference = ndb.StringProperty()
    startdate = ndb.DateTimeProperty()
    enddate = ndb.DateTimeProperty()
