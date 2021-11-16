from django.contrib import admin
from rootApp.models import Contact
from rootApp.models import FreeboardConstructionCost, Sampledata, Sample, dataAll

from django.contrib.gis import admin
from rootApp.models import JeffersonbuildingdataFSH, JeffersonAddress

admin.site.register(JeffersonbuildingdataFSH, admin.GeoModelAdmin)
admin.site.register(JeffersonAddress, admin.GeoModelAdmin) 
admin.site.register(Contact)

class FreeboardConstructionCostAdmin(admin.ModelAdmin):
    list_display = ("address", "street", "floodzone", "parish", "no_floors",)

class SampledataAdmin(admin.ModelAdmin):
    list_display = ("address", "street", "floodzone", "parish", "no_floors")

class SampleAdmin(admin.ModelAdmin):
    list_display = ("FID_1", "BLDG_ID","HEIGHT", "FOOTPRINT" , "address", "street", "no_floors", "DATA_YEAR", "SFT", "Area_SqMet", "FloodDepth10Year", "FloodDepth50Year", "FloodDepth100Year", "FloodDepth500Year", "ElevationUSGS2017", "Elevation_Jefferson", "Elevatio_2019USGS","parish","floodzone","Source", "u_intercept", "a_slope"  )

class dataAllAdmin(admin.ModelAdmin):
    list_display = ("FID_1", "BLDG_ID","HEIGHT", "FOOTPRINT" , "address", "street", "no_floors", "DATA_YEAR", "SFT", "Area_SqMet", "FloodDepth10Year", "FloodDepth50Year", "FloodDepth100Year", "FloodDepth500Year", "ElevationUSGS2017", "Elevation_Jefferson", "Elevatio_2019USGS","parish","floodzone","Source", "u_intercept", "a_slope"  )

class JeffersonAddressAdmin(admin.ModelAdmin):
    list_display = ("ADDRESS", "STREET","SUITE", "ZIP" , "AREA_NAME", "STREET_NAM", "ST_TYPE", "WO_AREA", "a_Slope", "u_Intercep", "FD100Year", "FD500Year", "FLD_ZONE", "BFE", "Latitude", "Longitude", "WSF1","WSF2" )


# Register your models here.
#admin.site.register(Contact)
admin.site.register(FreeboardConstructionCost, FreeboardConstructionCostAdmin)
admin.site.register(Sampledata)
admin.site.register(Sample, SampleAdmin) 
admin.site.register(dataAll, dataAllAdmin) 