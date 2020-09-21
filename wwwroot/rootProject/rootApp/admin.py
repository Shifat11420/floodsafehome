from django.contrib import admin
from rootApp.models import Contact
from rootApp.models import FreeboardConstructionCost

class FreeboardConstructionCostAdmin(admin.ModelAdmin):
    list_display = ("address", "street", "floodzone", "parish", "no_floors",)

# Register your models here.
admin.site.register(Contact)
admin.site.register(FreeboardConstructionCost, FreeboardConstructionCostAdmin)