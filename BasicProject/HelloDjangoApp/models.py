from django.db import models

class Event(models.Model):
    occurrence_time = models.DateTimeField()
    event_name = models.CharField(max_length=255)
    event_id = models.IntegerField(unique=True)
    severity = models.CharField(max_length=50)

