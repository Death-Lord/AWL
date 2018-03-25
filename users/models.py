from django.db import models
from django.core.exceptions import ValidationError

class users(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    user_name = models.CharField(max_length=20)
    password = models.CharField(max_length=32)
    profile_pic = models.ImageField(upload_to='staticFiles/profile_pic/', null=True, blank = True)

    def __str__(self):
        return self.first_name + " " + self.last_name

class forum(models.Model):
    post = models.CharField(max_length=1000)
    user = models.CharField(max_length=200)
    url = models.CharField(max_length=200)

class analyse_image(models.Model):
    image = models.ImageField(upload_to='staticFiles/analyse_image/', null=True, blank=True)
    location = models.CharField(max_length = 100, null=True, blank=True)
    pollution_data = models.CharField(max_length = 100, null=True, blank=True)

class chatbot_save(models.Model):
    message = models.CharField(max_length=500)
    by = models.CharField(max_length=100)
    url = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.message
class vehicle(models.Model):
    name=models.CharField(max_length=200)
    reg_no=models.CharField(max_length=200)
    date=models.DateField()
