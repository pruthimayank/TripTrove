from django.db import models

# Create your models here.
class Packages(models.Model):
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=1000)
    video = models.CharField(max_length=1000)
    description = models.TextField()
    price = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return self.name

class agent(models.Model):
    username=models.CharField(max_length=100)
    firstname=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    phone=models.IntegerField(null=True,blank=True)
    address=models.CharField(max_length=500)
    password=models.CharField(max_length=100)
    bookinghistory=models.JSONField(max_length=100,null=True,blank=True)

    def __str__(self):
        return f"{self.username}"