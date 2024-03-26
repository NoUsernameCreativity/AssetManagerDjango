from pyexpat import model
from django.db import models

# Create your models here.
class teacher(models.Model):
    Name = models.CharField(max_length=25)
    Area = models.CharField(max_length=30)

class asset(models.Model):
    Name = models.CharField(max_length=25, default="some asset")
    Location = models.CharField(max_length=30, default="IT room")
    Subject = models.CharField(max_length=25, default = 'IT')
    Value = models.FloatField(default=1)
    LastUpdated = models.DateTimeField(auto_now=True)
    AssetImage = models.ImageField(upload_to='images/assets', default='/images/defaultImage.jpg')