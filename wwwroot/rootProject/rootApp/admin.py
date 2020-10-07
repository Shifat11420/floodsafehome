from django.contrib import admin
from rootApp.models import Contact
from rootApp.models import FreeboardConstructionCost, Sampledata

class FreeboardConstructionCostAdmin(admin.ModelAdmin):
    list_display = ("address", "street", "floodzone", "parish", "no_floors",)

class FreeboardConstructionCostAdmin(admin.ModelAdmin):
    list_display = ("address", "street", "floodzone", "parish", "no_floors")

# Register your models here.
admin.site.register(Contact)
admin.site.register(FreeboardConstructionCost, FreeboardConstructionCostAdmin)
admin.site.register(Sampledata)