from django.db import models
from django import forms


# Create your models here.

class Contact(models.Model):
    name=models.CharField(max_length=122)
    email=models.CharField(max_length=122)
    desc=models.TextField(max_length=122)
    date=models.DateField()

    def __str__(self):
        return self.name
    

class FreeboardConstructionCost(models.Model):
    address=models.CharField(max_length=100)
    street=models.CharField(max_length=200)
    floodzone=models.CharField(max_length=100)
    parish=models.CharField(max_length=100)
    no_floors=models.CharField(max_length=10)

    # class Meta:
    #        ordering = ('address',)
    
    def __str__(self):
        return self.address+" , "+self.street