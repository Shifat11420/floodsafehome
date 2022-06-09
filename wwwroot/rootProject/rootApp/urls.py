from django.contrib import admin
from django.urls import path
from rootApp import views

from django.contrib.gis import admin
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns = [
    path("", views.index, name='Home'),
    path("about", views.about, name='About'),
    path("freeboardproject", views.freeboardproject, name='Freeboard Project'),
    path("map", views.decisionmakingmap, name='Decision Making Map'),
    path("gotomap", views.gotomap, name='Decision Making Map'),
    path("survey", views.survey, name='Survey'),
    path("helpcenter", views.helpcenter, name='Help Center'),
    path("search", views.search, name='Search'),
    path("dosurvey", views.dosurvey, name='dosurvey'),
    path("autosuggest", views.autosuggest, name='autosuggest'),
    path("starter", views.starter, name="starter"),
    path("nodisc", views.nodisc, name="nodisc"),
    path("disclaimer", views.disclaimer, name="disclaimer"),
    path("exportfile", views.exportfile, name="exportfile"),
    #path("exportpdf", views.exportpdf, name="exportpdf"),   
    path("exportshp", views.exportshp, name="exportshp"),
    path("report", views.report, name="report"),   
    ]
