from django.db import models


class Card(models.Model):
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=12)
    topic = models.CharField(max_length=255)
    text = models.TextField()
