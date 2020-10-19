from django.shortcuts import render, HttpResponse
from rootApp.models import Contact, FreeboardConstructionCost, Sampledata
from datetime import datetime
from django.contrib import messages
from django.db.models import Q
from functools import reduce
import operator
from django.http import JsonResponse
import json as simplejson
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import HoverTool, LassoSelectTool, WheelZoomTool, PointDrawTool, ColumnDataSource, FactorRange
from bokeh.palettes import Category20c, Spectral6
from bokeh.transform import cumsum, factor_cmap, dodge
from bokeh.core.validation import silence
from bokeh.core.validation.warnings import EMPTY_LAYOUT



# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def freeboardproject(request):
    return render(request, 'research.html')    

def decisionmakingmap(request):    
    return render(request, 'map.html')

def survey(request):
    return render(request, 'survey.html')  

def dosurvey(request):
    return render(request, 'dosurvey.html')      

def autosuggest(request): 
    print(request.GET)  
    query_original = request.GET.get('term')

    query_originalList=query_original.split(' ')

    # if query_original:
    #     query_originalList=query_original.split(' ')
    #     query_originalList = list(map(str.strip, query_original))

    #     fields = ["address__istartswith", "street__icontains"]

    #     q_expression = [Q(f,w) for f in fields for w in query_originalList]
    #     queryset = queryset.filter(reduce(operator.or_, q_expression)).distinct()

    #queryset = Sampledata.objects.filter(reduce(operator.and_, (Q(street__icontains=x) for x in query_originalList) ))
    #Q(address__istartswith = query_originalList[0]) | Q(street__icontains = query_originalList[1:]))
    if (len(query_originalList)==1):
        queryset = FreeboardConstructionCost.objects.filter(Q(address__istartswith = query_originalList[0]) | (Q(street__icontains = query_originalList[0]))  ).all()[:10]
    elif (len(query_originalList)==2):
        queryset = FreeboardConstructionCost.objects.filter((Q(address__istartswith = query_originalList[0]) | (Q(street__icontains = query_originalList[0]))), (Q(street__icontains = query_originalList[1]))  ).all()[:10]
    elif (len(query_originalList)==3):
        queryset = FreeboardConstructionCost.objects.filter((Q(address__istartswith = query_originalList[0]) | (Q(street__icontains = query_originalList[0]))), (Q(street__icontains = query_originalList[1])), (Q(street__icontains = query_originalList[1]))).all()[:10]
    else:
        queryset = FreeboardConstructionCost.objects.filter((Q(address__istartswith = query_originalList[0]) | (Q(street__icontains = query_originalList[0]))), (Q(street__icontains = query_originalList[1])), (Q(street__icontains = query_originalList[1]))).all()[:10]
        

    mylist = []
    mylist += [x.address+" "+x.street for x in queryset]
    return JsonResponse(mylist, safe=False)


def helpcenter(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        desc = request.POST.get('desc')
        contact = Contact(name=name, email=email, desc=desc, date=datetime.today()) 
        contact.save()
        messages.success(request, 'Your message has been sent!')

    return render(request, 'contact.html')    

def search(request):
    location = request.GET.get('location', 'default')
    locationList=location.split(' ')
    locationList = list(map(str.strip, locationList))
    streetlist = locationList[1:]

    if (len(streetlist)==1):
        addressvalue = FreeboardConstructionCost.objects.filter(
         Q(address__icontains=locationList[0]) ,  Q(street__icontains=locationList[1])).all()
    elif (len(streetlist)==2):
        addressvalue = FreeboardConstructionCost.objects.filter(
         Q(address__icontains=locationList[0]) ,  Q(street__icontains=locationList[1]), Q(street__icontains=locationList[2])).all()
    elif (len(streetlist)==3):
        addressvalue = FreeboardConstructionCost.objects.filter(
            Q(address__icontains=locationList[0]) ,  Q(street__icontains=locationList[1]), Q(street__icontains=locationList[2]), Q(street__icontains=locationList[3])).all()
    else:  
        addressvalue = FreeboardConstructionCost.objects.filter(
             Q(address__icontains=locationList[0]) ,  Q(street__icontains=locationList[1]), Q(street__icontains=locationList[2]), Q(street__icontains=locationList[3]), Q(street__icontains=locationList[4])).all()
    #zonevalue = []
    zonevalue = ""
    for data in addressvalue:
        #zonevalue.append(data.floodzone)
        zonevalue = data.floodzone
        parishvalue = data.parish

    ##by the average % increase table
    ## zone AE and zone X protected by levee are A zone
    ## for other zones, an average value for all zones are calculated  (to be changed later)
    AverageIncrease_zoneA = [0, 0.023,0.045,0.068,0.091]
    AverageIncrease_zoneCoastal = [0, 0.039,0.048,0.061,0.081]
    AverageIncrease_zoneV = [0, 0.018,0.036,0.054,0.072]
    Premium_zoneA = [1819, 920, 585, 476, 441]
    Premium_zoneV = [8158, 6549, 5208, 4107, 3533]

    AverageIncrease = []
    totalZones = ["A", "CoastalV", "V"]
    totalBFE = [0, 1, 2, 3, 4]
    primiumZones = ["A", "V"]
    premium = []

    ##for zone A
    if zonevalue == "AE" or zonevalue == "X PROTECTED BY LEVEE":
        # AverageIncrease_BFE1 = 1.3
        # AverageIncrease_BFE2 = 2.4
        # AverageIncrease_BFE3 = 3.8
        # AverageIncrease_BFE4 = 5.0
        AverageIncrease = AverageIncrease_zoneA
        premium = Premium_zoneA
    ##for other zones
    else:
        # AverageIncrease_BFE1 = (1.1+2.2+1.3)/3
        # AverageIncrease_BFE2 = (2.2+2.8+2.4)/3
        # AverageIncrease_BFE3 = (3.4+3.6+3.8)/3
        # AverageIncrease_BFE4 = (4.5+4.8+5.0)/3
        for i in range(len(totalBFE)):
            AverageIncrease.append(round((AverageIncrease_zoneA[i]+AverageIncrease_zoneCoastal[i]+ AverageIncrease_zoneV[i])/len(totalZones),3))
            premium.append((Premium_zoneA[i]+Premium_zoneV[i])/len(primiumZones))

    ## building cost, parishwise constant value 
    if parishvalue == "Jefferson":
        Building_cost = 92.47
    else:
        pass

    ## Square footage comes from user input
    Square_footage = float(request.GET.get('sqft', 'default'))

    # construction_cost_BFE1= Building_cost * Square_footage * AverageIncrease[1] 
    # construction_cost_BFE2= Building_cost * Square_footage * AverageIncrease[2] 
    # construction_cost_BFE3= Building_cost * Square_footage * AverageIncrease[3] 
    # construction_cost_BFE4= Building_cost * Square_footage * AverageIncrease[4] 

    construction_cost_BFE = []
    for i in range(len(AverageIncrease)):
        construction_cost_BFE.append(round(Building_cost * Square_footage * AverageIncrease[i],3)) 
        

    location_json_list = simplejson.dumps(location)    

    data_dict = {"location": location_json_list, "street": streetlist, "SquareFootage":Square_footage, "zone_value" : zonevalue , "Parish_value" : parishvalue, "AverageIncrease_BFE1" : AverageIncrease[1],"AverageIncrease_BFE2" : AverageIncrease[2],"AverageIncrease_BFE3" : AverageIncrease[3],"AverageIncrease_BFE4" : AverageIncrease[4] ,"construction_cost_BFE1": construction_cost_BFE[1], "construction_cost_BFE2": construction_cost_BFE[2], "construction_cost_BFE3": construction_cost_BFE[3], "construction_cost_BFE4": construction_cost_BFE[4], "Premium_BFE0": premium[0], "Premium_BFE1": premium[1], "Premium_BFE2": premium[2], "Premium_BFE3": premium[3], "Premium_BFE4": premium[4], "vegetable" : ['alu', 'potol']}
   # data_dict = {"zone_value" : zonevalue , "Parish_value" : parishvalue, "AverageIncrease" : AverageIncrease ,"construction_cost_BFE1": construction_cost_BFE1, "construction_cost_BFE2": construction_cost_BFE2, "construction_cost_BFE3": construction_cost_BFE3, "construction_cost_BFE4": construction_cost_BFE4, "vegetable" : ['alu', 'potol']}


    ##barchart
    benefits = ['Construction Cost', 'Insuracne ']
    nofStories = ['Zero_Ins','+ 1 story_Ins', '+ 2 story_Ins']

    data = {'benefits' : benefits,
            'Zero_Ins'   : [premium[0]],
            '+ 1 story_Ins'   : [premium[1]],
            '+ 2 story_Ins'   : [premium[2]],
            '+ 3 story_Ins'   : [premium[3]],
            '+ 4 story_Ins'   : [premium[4]],
            '+ 1 story_const'   :[construction_cost_BFE[1]],
            '+ 2 story_const'   :[construction_cost_BFE[2]],
            '+ 3 story_const'   :[construction_cost_BFE[3]],
            '+ 4 story_const'   :[construction_cost_BFE[4]]}

    x_values = [nofStories]
    counts = sum(zip(data['Zero_Ins'], data['+ 1 story_Ins'],data['+ 2 story_Ins']), ()) # like an hstack
    
    source = ColumnDataSource(data=data)

    p = figure(x_range=benefits, y_range=(0, 10000), plot_height=350, plot_width=500, 
            toolbar_location="below", tools="save, pan, wheel_zoom, box_zoom, reset, hover, tap, crosshair")

    p.vbar(x=dodge('benefits', -0.25, range=p.x_range), top='Zero_Ins', width=0.2, source=source,
        color="#c9d9d3", legend_label="+Zero_Ins")

    p.vbar(x=dodge('benefits',  0.0,  range=p.x_range), top='+ 1 story_Ins', width=0.2, source=source,
        color="#718dbf", legend_label="++ 1 story_Ins")

    p.vbar(x=dodge('benefits',  0.25, range=p.x_range), top='+ 2 story_Ins', width=0.2, source=source,
        color="#e84d60", legend_label="+ 2 story_Ins")
    
    p.x_range.range_padding = 0.1
    p.xgrid.grid_line_color = None
    p.legend.location = "top_left"
    p.legend.orientation = "horizontal"

    script, div = components(p)

    data_dictionary = {"location": location_json_list, "SquareFootage":Square_footage, 'script': script, 'div':div}

    #barchart ends


    return render(request, 'map.html', data_dictionary)


def starter(request):
    benefits = ['Construction Cost', 'Insuracne ']
    nofStories = ['Zero','+ 1 story', '+ 2 stories', '+ 3 stories', '+ 4 stories']

    data = {'benefits' : benefits,
            'Zero'   : [8,3,4,5,6,3,4],
            '+ 1 story'   : [5, 3, 3, 2, 4, 6],
            '+ 2 stories'   : [5, 3, 3, 2, 4, 6]}

    x_values = [nofStories]
    counts = sum(zip(data['Zero'], data['+ 1 story'],data['+ 2 stories']), ()) # like an hstack
    
    source = ColumnDataSource(data=data)

    p = figure(x_range=benefits, y_range=(0, 10), plot_height=350, title="Freeboard and Benefit Graph",
            toolbar_location="right", tools="save, pan, wheel_zoom, box_zoom, reset, hover, tap, crosshair")

    p.vbar(x=dodge('benefits', -0.25, range=p.x_range), top='Zero', width=0.2, source=source,
        color="#c9d9d3", legend_label="+Zero")

    p.vbar(x=dodge('benefits',  0.0,  range=p.x_range), top='+ 1 story', width=0.2, source=source,
        color="#718dbf", legend_label="+1 story")

    p.vbar(x=dodge('benefits',  0.25, range=p.x_range), top='+ 2 stories', width=0.2, source=source,
        color="#e84d60", legend_label="+2 stories")
    
    p.x_range.range_padding = 0.1
    p.xgrid.grid_line_color = None
    p.legend.location = "top_left"
    p.legend.orientation = "horizontal"

    script, div = components(p)
    return render(request, 'map.html' , {'script': script, 'div':div})

