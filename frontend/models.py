from django.db import models

# Create your models here.
class Packages(models.Model):
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    video = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

