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
import math



# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def freeboardproject(request):
    return render(request, 'research.html')    

def disclaimer(request):
    return render(request, 'disclaimer.html') 

def gotomap(request): 
    location = request.GET.get('location', 'default')   
    print("my location: ", location)
    locationList=location.split(' ')
    locationList = list(map(str.strip, locationList))
    streetlist = locationList[1:]
##Error message---------------------
    if (len(locationList)==1):
        queryset = FreeboardConstructionCost.objects.filter(Q(address__istartswith = locationList[0]) | (Q(street__icontains = locationList[0]))  ).all()[:10]
    elif (len(locationList)==2):
        queryset = FreeboardConstructionCost.objects.filter((Q(address__istartswith = locationList[0]) | (Q(street__icontains = locationList[0]))), (Q(street__icontains = locationList[1]))  ).all()[:10]
    elif (len(locationList)==3):
        queryset = FreeboardConstructionCost.objects.filter((Q(address__istartswith = locationList[0]) | (Q(street__icontains = locationList[0]))), (Q(street__icontains = locationList[1])), (Q(street__icontains = locationList[1]))).all()[:10]
    else:
        queryset = FreeboardConstructionCost.objects.filter((Q(address__istartswith = locationList[0]) | (Q(street__icontains = locationList[0]))), (Q(street__icontains = locationList[1])), (Q(street__icontains = locationList[1]))).all()[:10]

    mylist = []        
    if len(queryset)<=0:
        #mylist = ["Enter a valid address!"]
        messages.error(request, 'Enter a valid address!')

        return render(request, 'index.html')
    else:
        mylist = ["valid address"]  

##Error message ends-------------------------------
    
    
    location_json_list = simplejson.dumps(location)   
    data_dict = {"location": location_json_list}
    return render(request, 'map.html', data_dict)


def decisionmakingmap(request): 
    return render(request, 'map.html')

def nodisc(request): 
    return render(request, 'nodisc.html')

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
    if len(queryset)>0:

        mylist += [x.address+" "+x.street for x in queryset]
    else:
        mylist = ["No results found"]    
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

    No_Floors = request.GET['stories']
    print("accepted floors:", No_Floors)

## Error message---------------------
    if (len(locationList)==1):
        queryset = FreeboardConstructionCost.objects.filter(Q(address__istartswith = locationList[0]) | (Q(street__icontains = locationList[0]))  ).all()[:10]
    elif (len(locationList)==2):
        queryset = FreeboardConstructionCost.objects.filter((Q(address__istartswith = locationList[0]) | (Q(street__icontains = locationList[0]))), (Q(street__icontains = locationList[1]))  ).all()[:10]
    elif (len(locationList)==3):
        queryset = FreeboardConstructionCost.objects.filter((Q(address__istartswith = locationList[0]) | (Q(street__icontains = locationList[0]))), (Q(street__icontains = locationList[1])), (Q(street__icontains = locationList[1]))).all()[:10]
    else:
        queryset = FreeboardConstructionCost.objects.filter((Q(address__istartswith = locationList[0]) | (Q(street__icontains = locationList[0]))), (Q(street__icontains = locationList[1])), (Q(street__icontains = locationList[1]))).all()[:10]

    mylist = []        
    if len(queryset)<=0:
        #mylist = ["Enter a valid address!"]
        messages.error(request, 'Enter a valid address!')

        return render(request, 'index.html')
    else:
        mylist = ["valid address"]  

##Error message ends-------------------------------


##autocomplete-------------------------------------
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
    
    print("addressvalue: ", addressvalue, "type: ", type(addressvalue))
##autocomplete ends--------------------------------------------------
                
    #zonevalue = []
    zonevalue = ""
    for data in addressvalue:
        #zonevalue.append(data.floodzone)
        zonevalue = data.floodzone
        parishvalue = data.parish

    ##by the average % increase table, and premium table
    ## zone AE and zone X protected by levee are A zone
    ## for other zones, an average value for all zones are calculated  (to be changed later)
    AverageIncrease_zoneA = [0, 0.023,0.045,0.068,0.091]
    AverageIncrease_zoneCoastal = [0, 0.039,0.048,0.061,0.081]
    AverageIncrease_zoneV = [0, 0.018,0.036,0.054,0.072]
    Premium_zoneA = [1819, 920, 585, 476, 441]
    Premium_zoneV = [8158, 6549, 5208, 4107, 3533]
    AAL_BFE_LC_story1 = [0.03, 0.02, 0.015, 0.01, 0]
    AAL_BFE_LC_story2 = [0.035, 0.03, 0.02, 0.015, 0]

    AverageIncrease = []
    totalZones = ["A", "CoastalV", "V"]
    totalBFE = [0, 1, 2, 3, 4]
    primiumZones = ["A", "V"]
    premium = []
    AAL_BFE_losspercent = []



    if No_Floors=="1":
        AAL_BFE_losspercent = AAL_BFE_LC_story1
        print("No_Floors:",No_Floors)
    elif No_Floors=="2":
        AAL_BFE_losspercent = AAL_BFE_LC_story2
        print("No_Floors:",No_Floors)
    else:
        pass

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
        construction_cost_BFE.append(round(Building_cost * Square_footage * AverageIncrease[i],2)) 


    AAL_BFE=[]    
    for i in range(len(AAL_BFE_losspercent)):
        AAL_BFE.append(round(Building_cost * Square_footage * AAL_BFE_losspercent[i],3)) 
        #print(AAL_BFE[i])

    totalcost = []
    for i in range(len(AAL_BFE)):
        totalcost.append(round((AAL_BFE[i]+premium[i])*12+construction_cost_BFE[i],3))    #discounted present value, estimated from:   1(1+R_D )^t = 12  for 7% real discount rate
        #print(totalcost[i])

  
    #Net benefit (NB) is determined by subtracting the total cost of the freeboard scenario (step 10) 
    #from the total cost of the no action scenario.
    netbenefit = []
    for i in range(len(totalcost)):
       netbenefit.append(round(totalcost[0]-totalcost[i],2))
       #print(netbenefit[i])


    #Net benefit to cost ratio (NBCR) for each freeboard is the total net benefit of the freeboard scenario divided by its total cost.  

    NBcostRatio = []
    for i in range(len(totalcost)):
        if i==0:
            NBcostRatio.append(0)
        else:    
            NBcostRatio.append(math.trunc(netbenefit[i]/construction_cost_BFE[i]))
        print(NBcostRatio[i])

    location_json_list = simplejson.dumps(location)    

    data_dict = {"location": location_json_list, "street": streetlist, "SquareFootage":Square_footage, "zone_value" : zonevalue , "Parish_value" : parishvalue, "AverageIncrease_BFE1" : AverageIncrease[1],"AverageIncrease_BFE2" : AverageIncrease[2],"AverageIncrease_BFE3" : AverageIncrease[3],"AverageIncrease_BFE4" : AverageIncrease[4] ,"construction_cost_BFE1": construction_cost_BFE[1], "construction_cost_BFE2": construction_cost_BFE[2], "construction_cost_BFE3": construction_cost_BFE[3], "construction_cost_BFE4": construction_cost_BFE[4], "Premium_BFE0": premium[0], "Premium_BFE1": premium[1], "Premium_BFE2": premium[2], "Premium_BFE3": premium[3], "Premium_BFE4": premium[4], "vegetable" : ['alu', 'potol']}
# data_dict = {"zone_value" : zonevalue , "Parish_value" : parishvalue, "AverageIncrease" : AverageIncrease ,"construction_cost_BFE1": construction_cost_BFE1, "construction_cost_BFE2": construction_cost_BFE2, "construction_cost_BFE3": construction_cost_BFE3, "construction_cost_BFE4": construction_cost_BFE4, "vegetable" : ['alu', 'potol']}
    
   
    ##barchart-------------------------------
    benefits = ['Construction Cost', 'Insurance ', 'AAL', 'Total Cost', 'Net Benefit']
    nofStories = ['BFE + 0ft','BFE + 1ft', 'BFE + 2ft','BFE + 3ft','BFE + 4ft']

    data = {'benefits' : benefits,
            'BFE + 0ft'   : [0, premium[0], AAL_BFE[0], totalcost[0], netbenefit[0]],
            'BFE + 1ft'   : [construction_cost_BFE[1], premium[1], AAL_BFE[1], totalcost[1], netbenefit[1]],
            'BFE + 2ft'   : [construction_cost_BFE[2], premium[2], AAL_BFE[2], totalcost[2], netbenefit[2]],
            'BFE + 3ft'   : [construction_cost_BFE[3], premium[3], AAL_BFE[3], totalcost[3], netbenefit[3]],
            'BFE + 4ft'   : [construction_cost_BFE[4], premium[4], AAL_BFE[4], totalcost[4], netbenefit[4]]}

    x = [nofStories]
    counts = sum(zip( data['BFE + 0ft'],data['BFE + 1ft'],data['BFE + 2ft'], data['BFE + 3ft'],data['BFE + 4ft']), ()) # like an hstack
    
    source = ColumnDataSource(data=data)

    p = figure(x_range=benefits, plot_height=350, plot_width=500, 
            toolbar_location="below", tools="save, pan, wheel_zoom, box_zoom, reset, tap, crosshair")

    p.vbar(x=dodge('benefits',  -0.30,  range=p.x_range), top='BFE + 0ft', width=0.1, source=source,
        color="#253494", legend_label="BFE + 0ft")

    p.vbar(x=dodge('benefits',  -0.15,  range=p.x_range), top='BFE + 1ft', width=0.1, source=source,
        color="#2c7fb8", legend_label="BFE + 1ft")

    p.vbar(x=dodge('benefits',  0.00, range=p.x_range), top='BFE + 2ft', width=0.1, source=source,
        color="#41b6c4", legend_label="BFE + 2ft")
    
    p.vbar(x=dodge('benefits', 0.15, range=p.x_range), top='BFE + 3ft', width=0.1, source=source,
        color="#a1dab4", legend_label="BFE + 3ft")

    p.vbar(x=dodge('benefits', 0.30, range=p.x_range), top='BFE + 4ft', width=0.1, source=source,
        color="#ffffcc", legend_label="BFE + 4ft")
    
    p.y_range.start = 0
    p.xgrid.grid_line_color = None
    p.legend.location = "top_left"
    p.legend.orientation = "horizontal"
    
    # tooltip
    p.add_tools(HoverTool(
    tooltips=[
        ("Type", "@benefits"),
        ("Cost", "@count")
    ],

    # display a tooltip whenever the cursor is vertically in line with a glyph
    mode='vline'
    ))
    script, div = components(p)

    ##data_dictionary = {"location": location_json_list, "SquareFootage":Square_footage,"construction_cost_BFE1": construction_cost_BFE[1], "construction_cost_BFE2": construction_cost_BFE[2], "construction_cost_BFE3": construction_cost_BFE[3], "construction_cost_BFE4": construction_cost_BFE[4], "Premium_BFE0": premium[0], "Premium_BFE1": premium[1], "Premium_BFE2": premium[2], "Premium_BFE3": premium[3], "Premium_BFE4": premium[4], "AAL_BFE0":AAL_BFE[0], "AAL_BFE1":AAL_BFE[1], "AAL_BFE2":AAL_BFE[2], "AAL_BFE3":AAL_BFE[3], "AAL_BFE4":AAL_BFE[4], "netbenefit0" : netbenefit[0],"netbenefit1" : netbenefit[1],"netbenefit2" : netbenefit[2],"netbenefit3" : netbenefit[3], "netbenefit4" : netbenefit[4],"NBcostRatio1": NBcostRatio[1], "NBcostRatio2": NBcostRatio[2], "NBcostRatio3": NBcostRatio[3], "NBcostRatio4": NBcostRatio[4],  "No_Floors": No_Floors, 'script': script, 'div':div }
        
        #data_dictionary = {"location": location_json_list, "SquareFootage":Square_footage, 'script': script, 'div':div, 'AAL_BFE0' : AAL_BFE[0],'AAL_BFE1' : AAL_BFE[1],'AAL_BFE2' : AAL_BFE[2],'AAL_BFE3' : AAL_BFE[3],'AAL_BFE4' : AAL_BFE[4] }

        #barchart ends---------------------------------------
        
    ##New-------------------------------
    ##barchart for Net benefit to cost ratio-------------------------------
    ##benefits = ['1 foot freeboard', '2 feet freeboard', '3 feet freeboard', '4 feet freeboard']
    ##nofStories = ['Net benefit to cost ratio']
   
    data_dictionary = {"location": location_json_list, "SquareFootage":Square_footage,"construction_cost_BFE1": construction_cost_BFE[1], "construction_cost_BFE2": construction_cost_BFE[2], "construction_cost_BFE3": construction_cost_BFE[3], "construction_cost_BFE4": construction_cost_BFE[4], "Premium_BFE0": premium[0], "Premium_BFE1": premium[1], "Premium_BFE2": premium[2], "Premium_BFE3": premium[3], "Premium_BFE4": premium[4], "AAL_BFE0":AAL_BFE[0], "AAL_BFE1":AAL_BFE[1], "AAL_BFE2":AAL_BFE[2], "AAL_BFE3":AAL_BFE[3], "AAL_BFE4":AAL_BFE[4], "netbenefit0" : netbenefit[0],"netbenefit1" : netbenefit[1],"netbenefit2" : netbenefit[2],"netbenefit3" : netbenefit[3], "netbenefit4" : netbenefit[4],"NBcostRatio1": NBcostRatio[1], "NBcostRatio2": NBcostRatio[2], "NBcostRatio3": NBcostRatio[3], "NBcostRatio4": NBcostRatio[4],  "No_Floors": No_Floors, 'script': script, 'div':div }
    
    
    #New barchart ends---------------------------------------
    return render(request, 'nodisc.html', data_dictionary)


def starter(request):
  
    source = ColumnDataSource(data=dict(
    x=[1, 2, 3, 4, 5],
    y1=[500,1500,3500,4000,7000],
    y2=[300, 200,150, 100, ],
    ))
    p = figure(plot_width=400, plot_height=400)

    p.vline_stack(['y1', 'y2'], x='x', source=source)
    p.x_range.range_padding = 0.1
    p.xgrid.grid_line_color = None
    p.legend.location = "top_left"
    p.legend.orientation = "horizontal"

    script, div = components(p)
    return render(request, 'starter.html' , {'script': script, 'div':div})

