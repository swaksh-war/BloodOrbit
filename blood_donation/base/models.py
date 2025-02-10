from django.db import models

class Donor(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    long_term_disease = models.CharField(max_length=1000, blank=True, null=True)
    blood_group = models.CharField(max_length=3)
    latitude = models.FloatField()
    longitude = models.FloatField()
    contact_number = models.BigIntegerField()
    last_time_donated = models.DateTimeField(auto_now_add=True)
    registered_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.blood_group})"

