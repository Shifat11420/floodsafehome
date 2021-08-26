from django.db import models
from django import forms
from django.contrib.gis.db import models


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



class Sampledata(models.Model):
    address=models.CharField(max_length=100)
    street=models.CharField(max_length=200)
    floodzone=models.CharField(max_length=100)
    parish=models.CharField(max_length=100)
    no_floors=models.CharField(max_length=10)

    # class Meta:
    #        ordering = ('address',)
    
    def __str__(self):
        return self.address+" , "+self.street        

class Sample(models.Model):
    FID_1=models.CharField(max_length=10)
    BLDG_ID= models.CharField(max_length=10)
    HEIGHT= models.CharField(max_length=10)
    FOOTPRINT= models.CharField(max_length=30)            ##FOOTPRINT_
    address=models.CharField(max_length=100)              ##ADDRESS
    street=models.CharField(max_length=200)               ##STREET
    no_floors=models.CharField(max_length=10)             ##NO_FLOORS
    DATA_YEAR= models.CharField(max_length=10)
    SFT= models.CharField(max_length=10)
    Area_SqMet= models.CharField(max_length=30)
    FloodDepth10Year= models.CharField(max_length=10)
    FloodDepth50Year= models.CharField(max_length=10)
    FloodDepth100Year= models.CharField(max_length=10)
    FloodDepth500Year= models.CharField(max_length=10)
    ElevationUSGS2017= models.CharField(max_length=30)
    Elevation_Jefferson= models.CharField(max_length=30)
    Elevatio_2019USGS= models.CharField(max_length=30)
    parish=models.CharField(max_length=100)                   ##Name
    floodzone=models.CharField(max_length=100)                ##Zone
    Source= models.CharField(max_length=10)
    u_intercept= models.CharField(max_length=30)
    a_slope= models.CharField(max_length=30)
    

    
    def __str__(self):
        return self.address+" , "+self.street                


class dataAll(models.Model):
    FID_1=models.CharField(max_length=10)
    BLDG_ID= models.CharField(max_length=10)
    HEIGHT= models.CharField(max_length=10)
    FOOTPRINT= models.CharField(max_length=30)            ##FOOTPRINT_
    address=models.CharField(max_length=100)              ##ADDRESS
    street=models.CharField(max_length=200)               ##STREET
    no_floors=models.CharField(max_length=10)             ##NO_FLOORS
    DATA_YEAR= models.CharField(max_length=10)
    SFT= models.CharField(max_length=10)
    Area_SqMet= models.CharField(max_length=30)
    FloodDepth10Year= models.CharField(max_length=10)
    FloodDepth50Year= models.CharField(max_length=10)
    FloodDepth100Year= models.CharField(max_length=10)
    FloodDepth500Year= models.CharField(max_length=10)
    ElevationUSGS2017= models.CharField(max_length=30)
    Elevation_Jefferson= models.CharField(max_length=30)
    Elevatio_2019USGS= models.CharField(max_length=30)
    parish=models.CharField(max_length=100)                   ##Name
    floodzone=models.CharField(max_length=100)                ##Zone
    Source= models.CharField(max_length=10)
    u_intercept= models.CharField(max_length=30)
    a_slope= models.CharField(max_length=30)
    

    
    def __str__(self):
        return self.address+" , "+self.street          


class JeffersonbuildingdataFSH(models.Model):
    # Regular Django fields corresponding to the attributes in the
    # JeffersonBUILDING shapefile.
  
    FID_1 = models.BigIntegerField()
    BLDG_ID = models.CharField(max_length=10, null =True)
    HEIGHT = models.FloatField()
    FOOTPRINT = models.FloatField()           #
    address = models.CharField(max_length=100, null =True)
    street = models.CharField(max_length=200, null =True)
    no_floors = models.FloatField()
    DATA_YEAR = models.CharField(max_length=10, null =True)
    SFT = models.FloatField()
    Area_SqMet = models.FloatField()
    FloodDepth = models.FloatField()
    FloodDep_1 = models.FloatField()
    FloodDep_2 = models.FloatField()
    FloodDep_3 = models.FloatField()
    ElevationU = models.FloatField()
    Elevation = models.FloatField()      #
    Elevatio_1 = models.FloatField()
    FID_2 = models.BigIntegerField()
    Source = models.CharField(max_length=50, null =True)
    u_intercept = models.FloatField()
    a_slope = models.FloatField()
    Latitude = models.FloatField()
    Longitude = models.FloatField()
    FloodZone = models.CharField(max_length=100, null =True)
    Parish = models.CharField(max_length=50, null =True)


    # GeoDjango-specific: a geometry field (PointField)
    mpoint = models.MultiPointField()

    # Returns the string representation of the model.
    def __str__(self):
        return str(self.address)+" , "+str(self.street)                