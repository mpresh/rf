from django.db import models

class Person(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.CharField(max_length=50)

class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    event_date_time_start = models.DateTimeField('date time of event start')
    event_date_time_end = models.DateTimeField('date time of event end')
    capacity = models.IntegerField()
    venue = models.CharField(max_length=100)
    venue_address = models.CharField(max_length=300)
    organizer = models.ForeignKey(Person)
