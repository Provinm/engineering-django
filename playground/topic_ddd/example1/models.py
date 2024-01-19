from django.db import models


class PollRecord(models.Model):
    user_email = models.CharField(max_length=20)
    car_brand = models.CharField(max_length=100)
    created_time = models.DateTimeField(auto_now_add=True)
