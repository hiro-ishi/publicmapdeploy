from django.db.models import Model
from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models
from django.core import validators

class CustomUser(AbstractUser):

    def __str__(self):
        return self.email

class Post(models.Model):
    title = models.CharField(max_length=13)
    number = models.IntegerField(
    validators = [validators.MinValueValidator(0),
                validators.MaxValueValidator(999)]
    )
    location = models.PointField(srid=4326)
    memo = models.CharField(max_length=100)

    def __str__(self):
        return self.title
