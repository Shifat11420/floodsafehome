from django.shortcuts import redirect, render, HttpResponse
from rootApp.models import Contact, FreeboardConstructionCost, Sampledata, Sample, dataAll, JeffersonbuildingdataFSH
from rootApp.models import JeffersonAddress, TerrebonneAddress
from datetime import datetime
from django.contrib import messages
from django.db.models import Q
from django.core.mail import message, send_mail
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
from scipy.integrate import quad
from scipy import integrate as integrate
import numpy as np
import csv
import pandas as pd
import geopandas as gpd
from zipfile import ZipFile
import os
# import pdfkit
from django.http import HttpResponse
from django.views.generic import View
from django.template.loader import get_template

from rootProject.utils import render_to_pdf #created in step 4
# import imgkit
import re


# from django.template.loader import render_to_string
# from weasyprint import HTML
# import tempfile


datafile_list = [JeffersonAddress, TerrebonneAddress]
#datafile = JeffersonAddress #TerrebonneAddress #   #JeffersonbuildingdataFSH   #dataAll
 
 
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
    searchby = request.GET.get('select1', 'default')
    selectParish = request.GET.get('select2', 'default')

    ###  error message
    if searchby == '':
        print(" error searchby ", searchby)
        messages.error(request, 'Please choose how you want to search!')
        return render(request, 'index.html')
    else:
        print(" valid searchby ", searchby)

    if selectParish == '':
        print(" error selectParish ", selectParish)
        messages.error(request, 'Please choose a parish!')
        return render(request, 'index.html')
    else:
        print(" valid selectParish ", selectParish)    

    location = request.GET.get('location', 'default')   
    print("my location: ", location)
    stories = request.GET.get('stories', 'default')
    print("my stories: ", stories)         

    commasplit =location.split(',')
    beforecomma = commasplit[0]
    locationList= beforecomma.split(' ')
    locationList = list(map(str.strip, locationList))

    #locationList=location.split(' ')
    print("locationlist space split : ", locationList)
    locationList = list(map(str.strip, locationList))
    streetlist = locationList[1:]
##Error message---------------------
    mylist = []    
    for datafile in datafile_list:
        print("datafile in errmess : ", datafile)
        if (len(locationList)==1):
            queryset = datafile.objects.filter(Q(ADDRESS__istartswith = locationList[0]) | (Q(STREET__icontains = locationList[0]))  ).all()[:10]
        elif (len(locationList)==2):
            queryset = datafile.objects.filter((Q(ADDRESS__istartswith = locationList[0]) | (Q(STREET__icontains = locationList[0]))), (Q(ADDRESS__icontains = locationList[1]) | Q(STREET__icontains = locationList[1]))  ).all()[:10]
        elif (len(locationList)==3):
            queryset = datafile.objects.filter((Q(ADDRESS__istartswith = locationList[0]) | (Q(STREET__icontains = locationList[0]))), (Q(ADDRESS__icontains = locationList[1]) | Q(STREET__icontains = locationList[1])), (Q(STREET__icontains = locationList[2]))).all()[:10]
        else:
            print("lalalala")
            queryset = datafile.objects.filter((Q(ADDRESS__istartswith = locationList[0]) | (Q(STREET__icontains = locationList[0]))), (Q(ADDRESS__icontains = locationList[1]) | Q(STREET__icontains = locationList[1])), (Q(STREET__icontains = locationList[2]))).all()[:10]
        if queryset:
            break
            
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
    mylist = [] 
    for datafile in datafile_list:
        print("datafile ", datafile)
        if (len(query_originalList)==1):
            queryset = datafile.objects.filter(Q(ADDRESS__istartswith = query_originalList[0]) | (Q(STREET__icontains = query_originalList[0]))  ).all()[:10]
        elif (len(query_originalList)==2):
            queryset = datafile.objects.filter((Q(ADDRESS__istartswith = query_originalList[0]) | (Q(STREET__icontains = query_originalList[0]))), (Q(STREET__icontains = query_originalList[1]))  ).all()[:10]
        elif (len(query_originalList)==3):
            queryset = datafile.objects.filter((Q(ADDRESS__istartswith = query_originalList[0]) | (Q(STREET__icontains = query_originalList[0]))), (Q(STREET__icontains = query_originalList[1])), (Q(STREET__icontains = query_originalList[1]))).all()[:10]
        else:
            queryset = datafile.objects.filter((Q(ADDRESS__istartswith = query_originalList[0]) | (Q(STREET__icontains = query_originalList[0]))), (Q(STREET__icontains = query_originalList[1])), (Q(STREET__icontains = query_originalList[1]))).all()[:10]

        

               
        if len(queryset)>0:
            #mylist += [x.ADDRESS+" "+x.STREET+","+" "+x.Parish+ " Parish" for x in queryset]
            #mylist += [x.ADDRESS+" "+x.STREET+","+" "+x.AREA_NAME+","+" "+x.ZIP+","+" "+"Jefferson Parish" for x in queryset]
            mylist += [x.ADDRESS+" "+x.STREET+","+" "+x.AREA_NAME+","+" "+x.ZIP+","+" "+"LA" for x in queryset]

        else:
            mylist = ["No results found"]  

    print("my list in autosuggest : ", mylist)          
    return JsonResponse(mylist, safe=False)


def helpcenter(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')

        selecttype = request.POST.get('select-type','')
        if not selecttype:
            messages.error(request, 'Please select the following options')
            return redirect('/helpcenter')
        locationproblem = request.POST.get('locationproblem')
        detail = request.POST.get('detail')
        subject1 = request.POST.get('subject1')
        detailmethodse1 = request.POST.get('detail-method-or-se1')
        subject2 = request.POST.get('subject2')
        detailmethodse2 = request.POST.get('detail-method-or-se2')

        data = {
            'name' : name,
            'email' : email,
            'selecttype' : selecttype,
            'locationproblem' : locationproblem,
            'location_problem_detail' : detail,
            'subject_Ques_about_methodology' : subject1,
            'detail_Ques_about_methodology' : detailmethodse1,
            'subject_other_problem' : subject2,
            'detail_other_problem' : detailmethodse2
        }


        message = '''
        New message from : {}
        
        Problem type: {}

        Problem with location: {} 
        Details about location problem: {}

        Question about methodology- Subject : {}
        Question about methodology- Details : {}

        Other problem- Subject : {}
        Other problem- Details : {}

        '''.format(data['email'], data['selecttype'], data['locationproblem'], data['location_problem_detail'],data['subject_Ques_about_methodology'],data['detail_Ques_about_methodology'],data['subject_other_problem'],data['detail_other_problem'])
        send_mail(data['selecttype'], message, '', ['floodsafehome@gmail.com'])

        contact = Contact(name=name, email=email, selecttype=selecttype, locationproblem=locationproblem, detail=detail, subject1=subject1, detailmethodse1=detailmethodse1, subject2=subject2, detailmethodse2=detailmethodse2, date=datetime.today()) 
        contact.save()
        messages.success(request, 'Your message has been sent!')

    return render(request, 'contact.html', {})    



def search(request):
    

##---------user input---------------------------------
#   community level #
    total_monthly_saving_list_c = []
    total_optimal_saving_list_c = [] 
    total_optimal_freeboard_list_c = [] 
    freeboardCost_list_c = []
    total_annual_premium_list_c = []
    total_monthly_premium_list_c = []
    #AAL_absCurrency_list_c = []
    AAL_Total_list_c = []
    time_to_recover_FC_TB_list_c = []
    time_to_recover_FC_PS_list_c = []   
    avoided_monthly_loss_homeowner_list_c =[]
    avoided_monthly_loss_landlord_list_c = []
    avoided_monthly_loss_tenant_list_c = []   


    total_monthly_premium_saving_list_c = []
    annual_avoided_loss_list_c = []
    monthly_avoided_loss_list_c = []
    Amortized_FC_list_c = []
    total_savings_permonth_insurance_list_c = []

    latlon_c = []
    lattitude_c = []
    longitude_c = []
    

    buildinglist = []
    user_type = request.GET.get('chk')
    building_type = request.GET.get('selectBox')
    assessment_type = request.GET.get('chkYes2')
    buildinglocation_type = request.GET.get('select')
    selectParish = request.GET.get('select12', 'default')
    selectParish_homeOwener = request.GET.get('select2', 'default')
    selectParish_ComSingle = request.GET.get('select3', 'default')
    selectParish_ComSpatial = request.GET.get('select4', 'default')
    print("User type =", user_type)
    print("Building type =", building_type)
    print("Assessment type =", assessment_type)

    #print("Parish selected (homeowner) =", selectParish_homeOwener)
    #print("Parish selected (Com Single) =", selectParish_ComSingle)
    #print("Parish selected (Com Spatial) =", selectParish_ComSpatial)
    print("Parish selected =", selectParish)


    addr_list = request.GET.get('addr_list')
    print("Addr list = ", addr_list)
    if addr_list:
        #buildinglist = addr_list.split('$$')
        #buildinglist = addr_list.split(' Parish') ##

        #nozoneaddress = re.split(', Jefferson Parish|, Jefferson', addr_list)
        nozoneaddress = re.split(', LA', addr_list)
        print(nozoneaddress)

        for addr in nozoneaddress:
            #withzoneaddress = addr+', Jefferson Parish'
            withzoneaddress = addr+', LA'
            print(withzoneaddress)
            buildinglist.append(withzoneaddress)
        print("buildinglist", buildinglist)

        print("buildinglist before deleting last element : ", buildinglist)
        lenghofBlist = len(buildinglist)
        print(" length of  B list : ", lenghofBlist)
        buildinglist.remove(buildinglist[lenghofBlist-1])
    else:
        buildinglist = [ request.GET.get('location', 'default')]



    print("\n\n*************************************************\n\n")
    print(buildinglist)
    search.buildinglocation = buildinglist
    print("\n\n*************************************************\n\n")

    
    #with open(r'C:\inetpub\wwwroot\rootProject\output\results.csv', 'w', newline='') as output:           ##**********server copy  
    with open('output/results.csv', 'w', newline='') as output:                                            ##**********local copy  
        line_count=0
        fieldnames = ['Address', 'Lattitude', 'Longitude', 'Parish', 'Flood zone', 'Individual building optimal saving', 'Individual building recommended freeboard']
        output_data = csv.DictWriter(output, fieldnames=fieldnames)
        output_data.writeheader()


        zonelist = []
        for i in range(len(buildinglist)):
            line_count += 1      ##
            location = buildinglist[i]

            ##------location-----------------------
            #location = request.GET.get('location', 'default')
            commasplit =location.split(',')
            beforecomma = commasplit[0]
            locationList= beforecomma.split(' ')
            locationList = list(map(str.strip, locationList))
            streetlist = locationList[1:]

            ##-------number of stories------------------------
            No_Floors = request.GET.get('stories', 'default') #request.GET['stories']

            print("accepted floors:", No_Floors)
            #     ## error message
            # if No_Floors == 'default':
            #     messages.error(request, 'Please choose number of stories!')
            #     return render(request, 'nodisc.html')
    
            # else:
            #     mylist = ["valid stories"]  

            ##--------------square footage-----------------------
            Square_footage = float(request.GET.get('sqft1', 'default'))
            print ("square footage = ", Square_footage)
                
        ##----------user input ends---------------------------------------



        ##----------------------- Error message---------------------
            mylist = [] 
            for datafile in datafile_list:
                if (len(locationList)==1):
                    queryset = datafile.objects.filter(Q(ADDRESS__istartswith = locationList[0]) | (Q(STREET__icontains = locationList[0]))  ).all()[:10]
                elif (len(locationList)==2):
                    queryset = datafile.objects.filter((Q(ADDRESS__istartswith = locationList[0]) | (Q(STREET__icontains = locationList[0]))), (Q(STREET__icontains = locationList[1]))  ).all()[:10]
                elif (len(locationList)==3):
                    queryset = datafile.objects.filter((Q(ADDRESS__istartswith = locationList[0]) | (Q(STREET__icontains = locationList[0]))), (Q(ADDRESS__icontains = locationList[1]) | Q(STREET__icontains = locationList[1])), (Q(STREET__icontains = locationList[2]))).all()[:10]
                else:
                    queryset = datafile.objects.filter((Q(ADDRESS__istartswith = locationList[0]) | (Q(STREET__icontains = locationList[0]))), (Q(ADDRESS__icontains = locationList[1]) | Q(STREET__icontains = locationList[1])), (Q(STREET__icontains = locationList[2]))).all()[:10]
                if queryset:
                    break
                       
            if len(queryset)<=0:
                #mylist = ["Enter a valid address!"]
                messages.error(request, 'Enter a valid address!')

                return render(request, 'index.html')
            else:
                mylist = ["valid address"]  

            ##------------------Error message ends-------------------------------


            ##--------------------autocomplete-------------------------------------
            for datafile in datafile_list:
                if (len(streetlist)==1):
                    addressvalue = datafile.objects.filter(
                    Q(ADDRESS__icontains=locationList[0]) ,  (Q(ADDRESS__icontains=locationList[1]) | Q(STREET__icontains=locationList[1]))).all()
                elif (len(streetlist)==2):
                    addressvalue = datafile.objects.filter(
                    Q(ADDRESS__icontains=locationList[0]) ,  (Q(ADDRESS__icontains=locationList[1]) | Q(STREET__icontains=locationList[1])), Q(STREET__icontains=locationList[2])).all()        
                elif (len(streetlist)==3):
                    addressvalue = datafile.objects.filter(
                        Q(ADDRESS__icontains=locationList[0]) ,  (Q(ADDRESS__icontains=locationList[1]) | Q(STREET__icontains=locationList[1])), Q(STREET__icontains=locationList[2]), Q(STREET__icontains=locationList[3])).all()    
                else:  
                    addressvalue = datafile.objects.filter(
                        Q(ADDRESS__icontains=locationList[0]) ,  (Q(ADDRESS__icontains=locationList[1]) | Q(STREET__icontains=locationList[1])), Q(STREET__icontains=locationList[2]), Q(STREET__icontains=locationList[3]), Q(STREET__icontains=locationList[4])).all()
                print("addressvalue: ", addressvalue, "type: ", type(addressvalue))
                if addressvalue:
                    break 
        ##------------------autocomplete ends--------------------------------------------------
                        
        ##-----------queries------------------------------

            u = ""
            a = ""
            zonevalue = ""
            parishvalue = ""
            for data in addressvalue:
                zonevalue = data.FLD_ZONE
                zonelist.append(zonevalue)

                u = data.u_Intercep
                a = data.a_Slope
                if u == "Unknown" or u == -9999.0 or u == -9999:
                    u = 1.5218
                else:
                    u=float(u)    
                if a == "Unknown" or a == "Problematic" or a == -9999.0 or a == -9999:
                    a = 0.335   
                else:
                    a=float(a)       

                print("ZONE: ", zonevalue )
                print("u value: ", u )
                print("a value: ", a )
     
                parishvalue = selectParish
                # if user_type == "Homeowner":
                #     parishvalue = selectParish
                
                #     # parishvalue = selectParish_homeOwener
                # # elif user_type == "Tenant":
                # #     parishvalue = selectParish_tenant
                # # elif user_type == "Landlord":
                # #     parishvalue = selectParish_landlord

                # elif user_type == "Community official":
                #     parishvalue = selectParish
                    # if assessment_type == "Single_building":
                    #     parishvalue = selectParish_ComSingle
                    # elif assessment_type == "Spatial_scale":
                    #     parishvalue = selectParish_ComSpatial
                    # else:
                    #     parishvalue = selectParish_homeOwener
                    #     print("default assesment type case")
               # else:
                #    print("None of the user type!")
                 #   parishvalue = selectParish_homeOwener #"NONE"   #fix it later
                  #  print("parishvalue = ", parishvalue)


                print("Parish is : ", parishvalue)
                lat = data.Latitude
                lon =  data.Longitude

                latlon_pair = []
                lattitude_c.append(lat)
                longitude_c.append(lon)

                latlon_pair.append(buildinglist[0])
                latlon_pair.append(lat)
                latlon_pair.append(lon)

                latlon_c.append(latlon_pair)

                BFE = 0 #data.BFE
                print( "BFE : ", BFE) 
                if zonevalue == "X" or zonevalue == "X PROTECTED BY LEVEE" or zonevalue == "0.2 PCT ANNUAL CHANCE FLOOD HAZARD":# or BFE == -9999.0:
                    BFE = 0.5
                print( "BFE changed to : ", BFE)     
              
        ##--------queries end----------------------------


        ##--------------DEMO values-----------------TO BE CHANGED------
                       
            r = 0.03    # say, interest rate 3%
            n = 12       # no of payments per year
            t = 30      # loan term or number of years in the loan
            deductible_bldg = 1250   # demo-must be changed
            deductible_cont = 1250   # demo-must be changed

            
            coverage_lvl_bldg = 225000 #Building_value
            coverage_lvl_cont = 90000 #Building_value * 0.4
            
        ##---------demo values end--------------------


        ##------building cost, parishwise constant value and CRS------------- 
            if parishvalue == "Jefferson":
                Building_cost = 92.47
                CRS = 0.05                # demo-must be changed
                CRSpercent = CRS *100
            else:
                Building_cost = 100  
                CRS = 0.05   # for demo use
                pass

        ##----Building value----------------------------------

            Building_value = Building_cost * Square_footage
            Actual_construction_cost = int(0.023 * Building_value)

        ##-------BFE increments i---------------------------

            totalBFE = [0, 1, 2, 3, 4]
            #totalBFE = [-4, -3, -2, -1, 0, 1, 2, 3, 4]

        ##----------FFE (Ehab's method)-----------------------------
            FFE = []
            for i in range(len(totalBFE)):
                FFE.append(totalBFE[i]+BFE)   

        ##-----------freeboard construction cost-----------------

            freeboardCost = []
            for i in range(len(totalBFE)):
                if totalBFE[i] <=0:
                    freeboardCost.append(0)
                else:    
                    freeboardCost.append(int(totalBFE[i] * 0.023 * Building_value))
            freeboardCost_list_c.append(freeboardCost)   
            print("Freeboard cost : ", freeboardCost) 

            #freeboardCostnoBFE0 = freeboardCost.remove(freeboardCost[0])

            freeboardCost_json = simplejson.dumps(freeboardCost)  

            optimal_freeboardCost = max(freeboardCost)
            
            for k in range(len(freeboardCost)):
                if optimal_freeboardCost == freeboardCost[k]:
                    optimal_freeboard_freeboardCost = totalBFE[k]


            optimal_freeboardCost_json = simplejson.dumps(optimal_freeboardCost)  

                

        ##---------------AAL (Ehab's method)------------------------

        #     def integrand_Bldg(E):
        #         y = (E-u)/a
        #         term = -y - math.exp(-y)

        #         #### V zones functions for AAL building
        #         if zonevalue == "VE":
                    
        #             EminusF_bldg = [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
        #             damage_bldg = [0.215, 0.24, 0.29, 0.37, 0.54, 0.605, 0.645, 0.68, 0.7, 0.72, 0.74, 0.76, 0.78, 0.8, 0.815, 0.83, 0.84, 0.85, 0.86, 0.87]

        #             for i in range(len(EminusF_bldg)):
        #                 if EminusF_bldg[i] == math.floor(E-F):
        #                     loss_bldg_inftoneg1 = np.interp(E-F, EminusF_bldg, damage_bldg)
        #                 elif (E-F) < -1:
        #                     loss_bldg_inftoneg1 = 0                ### for now, check on the values
        #                 elif (E-F) > 18 :
        #                     loss_bldg_inftoneg1 = 0.87                 ### for now, check on the values
        #                 else:
        #                     pass    


        #         #### Not V zones functions for AAL building    
        #         else:    
        #             if No_Floors ==  "One story" : 
        #                 #loss_bldg_inftoneg1 = (0.0092 *((E-F)**3)- 0.5342 * ((E-F)**2) + 10.404 *(E-F) + 13.418 )
        #                 loss_bldg_inftoneg1 = (0.0092 *((E-F)**3)- 0.5362 * ((E-F)**2) + 10.419 *(E-F) + 13.39 )        
        #             elif No_Floors =="Two or more stories":
        #                 #loss_bldg_inftoneg1 = ( -0.0001 *((E-F)**3)- 0.1464 * ((E-F)**2) + 6.1207 *(E-F) + 9.2646 )
        #                 loss_bldg_inftoneg1 = ( -0.0001 *((E-F)**3)- 0.1466 * ((E-F)**2) + 6.1218 *(E-F) + 9.2626 )
        #             else:
        #                 pass  

        #         loss=(((1/a)* math.exp(term))*loss_bldg_inftoneg1)

        #         return loss

        #     def integrand_Cont(E):
        #         y = (E-u)/a
        #         term = -y - math.exp(-y)

        #         #### V zones functions for AAL content
        #         if zonevalue == "VE":
                    
        #             EminusF_cont = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
        #             damage_cont = [0.15, 0.23, 0.35, 0.5, 0.58, 0.63, 0.67, 0.7, 0.72, 0.78, 0.78, 0.78, 0.78, 0.78, 0.78, 0.78, 0.78, 0.78, 0.78]

        #             for i in range(len(EminusF_cont)):
        #                 if EminusF_cont[i] == math.floor(E-F):
        #                     loss_cont_infto0 = np.interp(E-F, EminusF_cont, damage_cont)
        #                 elif (E-F) < 0:
        #                     loss_cont_infto0 = 0                ### for now, check on the values
        #                 elif (E-F) > 18 :
        #                     loss_cont_infto0 = 0.78                 ### for now, check on the values
        #                 else:
        #                     pass   

        #         #### Not V zones functions for AAL content    
        #         else:    
        #             if No_Floors ==  "One story" :         
        #                 loss_cont_infto0 = ( 0.0049 *((E-F)**3)- 0.2996 * ((E-F)**2) + 5.5358 *(E-F) + 8.0402 )
        #             elif No_Floors == "Two or more stories" :        
        #                 loss_cont_infto0 = ( -0.0001 *((E-F)**3)- 0.1116 * ((E-F)**2) + 3.8257 *(E-F) + 4.9975 )
        #             else:
        #                 pass  

        #         loss=(((1/a)* math.exp(term))*loss_cont_infto0)

        #         return loss


        #     AAL_absCurrency = []
        #     AAL_B_ansNerr = []
        #     AAL_C_ansNerr = []
        #     for i in range(len(totalBFE)): 
        #         F= FFE[i]
        #         AAL_B_ansNerr.append(quad(integrand_Bldg, (F-1), math.inf))
        #         AAL_C_ansNerr.append(quad(integrand_Cont, F, math.inf))

         
        #     AAL_bldg = []
        #     AAL_cont = []
        #     for tuple in AAL_B_ansNerr:
        #         AAL_bldg.append(round(tuple[0],3))
        #     for tuple in AAL_C_ansNerr:  
        #         AAL_cont.append(round(tuple[0],3))

        #     print("\n")
        #     print("AAL_Building : ", AAL_bldg,"\n") 
        #     print("AAL_Content : ", AAL_cont,"\n") 

        #     ##--------Expected annual flood loss is AAL in absCurrency-------------------------
        #     AAL_percentValue=[]
        #     AAL_absCurrency=[]
        #     AAL_B_absCurrency=[]
        #     AAL_C_absCurrency=[]

        #     for i in range(len(totalBFE)): 
        #         AAL_B_absCurrency.append(int(AAL_bldg[i] * Building_value/100))
        #         AAL_C_absCurrency.append(int(AAL_cont[i] * Building_value/100))
        #         AAL_percentValue.append( round(AAL_bldg[i] + AAL_cont[i],3))
        #         AAL_absCurrency.append(int(AAL_percentValue[i] * Building_value/100))
        

        #     print("AAL_B_absCurrency : ", AAL_B_absCurrency)
        #     print("AAL_C_absCurrency : ", AAL_C_absCurrency)
        #     print("AAL_percentValue : ", AAL_percentValue)
        #     print("AAL_absCurrency : ", AAL_absCurrency)

        #     AAL_absCurrency_list_c.append(AAL_absCurrency)

        #     AAL_absCurrency_json = simplejson.dumps(AAL_absCurrency)  
        #     optimal_AAL_absCurrency = min(AAL_absCurrency)

        #     for k in range(len(AAL_absCurrency)):
        #         if optimal_AAL_absCurrency == AAL_absCurrency[k]:
        #             optimal_AAL_absCurrency_freeboard = totalBFE[k]

        #     optimal_AAL_absCurrency_json = simplejson.dumps(optimal_AAL_absCurrency)  


        # ##----------------------AAL (Ehab's method) ends ---------------------------------------


        ##----------------------AAL (Adil's method) ---------------------------------------
            print("****************     ##     ******************")        
            ## USER INPUT
            stories = No_Floors #stories = 1, 
            basement = "no"      # for Jefferson parish
            basement_Q2 = "N/A"   #for Jefferson parish
            #FFH = 3.1

            ## OTHER INPUT
            #u = 1.546, a = 0.3311  ##u and a are taken from database

            building_area = Square_footage  #2000   ##liveable square footage
            # Building_value = 200000
            
            
            #zonevalue = "A/AE"   # for TABLE 1,2,3,4,5,6
            #zonevalue = "V/VE"    # for TABLE 7

            ## calculation 

            # step 1

            ## TABLE 1: A/AE Zone, No Basement, Single Story, USACE

            dh1 = [-2,-1.5,-1,-0.5,0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10,10.5,11,11.5,12,12.5,13,13.5,14,14.5,15, 15.5, 16]
            structure_loss1 = [0,1.25,2.5,7.95,13.4,18.35,23.3,27.7,32.1,36.1,40.1,43.6,47.1,50.15,53.2,55.9,58.6,60.9,63.2,65.2,67.2,68.85,70.5,71.85,73.2,74.3,75.4,76.3,77.2,77.85,78.5,79,79.5,79.85,80.2,80.45,80.7]
            contents_loss1 = [0,1.2,2.4,5.25,8.1,10.7,13.3,15.6,17.9,19.95,22,23.85,25.7,27.25,28.8,30.15,31.5,32.65,33.8,34.75,35.7,36.45,37.2,37.8,38.4,38.8,39.2,39.45,39.7,39.85,40,40,40,40,40,40,40]
            Luse_homeowner1 = [0,0,0,0,9,9,9,9,9,9,9,9,12,12,12,12,12,12,12,12,15,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24]
            Luse_landlord1 = [0,0,0,0,10,10,10,10,10,10,10,10,13,13,13,13,13,13,13,13,16,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25]
            Luse_tenant1 = [0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]


            ## TABLE 2: A/AE Zone, No Basement, Two Story, USACE
            dh2 = [-2,-1.5,-1,-0.5,0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10,10.5,11,11.5,12,12.5,13,13.5,14,14.5,15, 15.5, 16]
            structure_loss2 = [0,1.5,3,6.15,9.3,12.25,15.2,18.05,20.9,23.6,26.3,28.85,31.4,33.8,36.2,38.45,40.7,42.8,44.9,46.85,48.8,50.6,52.4,54.05,55.7,57.2,58.7,60.05,61.4,62.6,63.8,64.85,65.9,66.8,67.7,68.45,69.2]
            contents_loss2 = [0,0.5,1,3,5,6.85,8.7,10.45,12.2,13.85,15.5,17,18.5,19.9,21.3,22.6,23.9,25.1,26.3,27.35,28.4,29.35,30.3,31.15,32,32.7,33.4,34.05,34.7,35.15,35.6,36,36.4,36.65,36.9,37.05,37.2]
            Luse_homeowner2 = [0,0,0,0,9,9,9,9,9,9,9,9,12,12,12,12,12,12,12,12,15,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24]
            Luse_landlord2 = [0,0,0,0,10,10,10,10,10,10,10,10,13,13,13,13,13,13,13,13,16,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25]
            Luse_tenant2 = [0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

            ## TABLE 3: A/AE Zone, Basement, Split level, USACE
            dh3 = [-2.0,-1.5,-1.0,-0.5,0.0,0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0,5.5,6.0,6.5,7.0,7.5,8.0,8.5,9.0,9.5,10.0,10.5,11.0,11.5,12.0,12.5,13.0,13.5,14.0,14.5,15.0,15.5,16.0]
            structure_loss3 = [0,3.2,6.4,6.8,7.2,8.3,9.4,11.15,12.9,15.15,17.4,20.1,22.8,25.85,28.9,32.2,35.5,38.9,42.3,45.75,49.2,52.65,56.1,59.35,62.6,65.6,68.6,71.25,73.9,76.15,78.4,80.05,81.7,82.75,83.8,84.1,84.4]
            contents_loss3 = [0,1.1,2.2,2.55,2.9,3.8,4.7,6.1,7.5,9.3,11.1,13.2,15.3,17.7,20.1,22.65,25.2,27.85,30.5,33.1,35.7,38.3,40.9,43.35,45.8,48,50.2,52.15,54.1,55.65,57.2,58.3,59.4,59.95,60.5,60.5,60.5]
            Luse_homeowner3 = [0,0,0,0,9,9,9,9,9,9,9,9,12,12,12,12,12,12,12,12,15,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24]
            Luse_landlord3 = [0,0,0,0,10,10,10,10,10,10,10,10,13,13,13,13,13,13,13,13,16,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25]
            Luse_tenant3 = [0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]


            ## TABLE 4: A/AE Zone, Basement, One Story, USACE
            dh4 = [-8,-7.5,-7,-6.5,-6,-5.5,-5,-4.5,-4,-3.5,-3,-2.5,-2,-1.5,-1,-0.5,0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10,10.5,11,11.5,12,12.5,13,13.5,14,14.5,15,15.5,16]
            structure_loss4 = [0,0.35,0.7,0.75,0.8,1.6,2.4,3.8,5.2,7.1,9,11.4,13.8,16.6,19.4,22.45,25.5,28.75,32,35.35,38.7,42.1,45.5,48.85,52.2,55.4,58.6,61.55,64.5,67.15,69.8,72,74.2,75.95,77.7,78.9,80.1,80.6,81.1,81.1,81.1,81.1,81.1,81.1,81.1,81.1,81.1,81.1,81.1]
            contents_loss4 = [0,0.4,0.8,1.45,2.1,2.9,3.7,4.7,5.7,6.85,8,9.25,10.5,11.85,13.2,14.6,16,17.45,18.9,20.35,21.8,23.25,24.7,26.05,27.4,28.7,30,31.2,32.4,33.45,34.5,35.4,36.3,37,37.7,38.15,38.6,38.85,39.1,39.1,39.1,39.1,39.1,39.1,39.1,39.1,39.1,39.1,39.1]
            Luse_homeowner4 = [9.0,9.0,9.0,9.0,9.0,9.0,9.0,9.0,12.0,12.0,12.0,12.0,12.0,12.0,12.0,12.0,15.0,15.0,15.0,15.0,15.0,15.0,15.0,15.0,15.0,15.0,15.0,15.0,18.0,24.0,24.0,24.0,24.0,24.0,24.0,24.0,24.0,24.0,24.0,24.0,24.0,24.0,24.0,24.0,24.0,24.0,24.0,24.0,24.0]
            Luse_landlord4 = [10.0,10.0,10.0,10.0,10.0,10.0,10.0,10.0,13.0,13.0,13.0,13.0,13.0,13.0,13.0,13.0,16.0,16.0,16.0,16.0,16.0,16.0,16.0,16.0,16.0,16.0,16.0,16.0,19.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0]
            Luse_tenant4 = [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0]


            ## TABLE 5: A/AE Zone, Basement, Two Story, USACE
            dh5 = [-8,-7.5,-7,-6.5,-6,-5.5,-5,-4.5,-4,-3.5,-3,-2.5,-2,-1.5,-1,-0.5,0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10,10.5,11,11.5,12,12.5,13,13.5,14,14.5,15,15.5,16]
            structure_loss5 = [0,0.85,1.7,1.8,1.9,2.4,2.9,3.8,4.7,5.95,7.2,8.7,10.2,12.05,13.9,15.9,17.9,20.1,22.3,24.65,27,29.45,31.9,34.4,36.9,39.4,41.9,44.4,46.9,49.35,51.8,54.1,56.4,58.6,60.8,62.8,64.8,66.6,68.4,69.9,71.4,72.55,73.7,74.55,75.4,75.9,76.4,76.4,76.4]
            contents_loss5 = [0,0.5,1,1.65,2.3,3,3.7,4.45,5.2,6,6.8,7.6,8.4,9.25,10.1,11,11.9,12.85,13.8,14.75,15.7,16.7,17.7,18.75,19.8,20.9,22,23.15,24.3,25.5,26.7,27.9,29.1,30.4,31.7,33.05,34.4,35.8,37.2,38.6,40,41.5,43,44.55,46.1,47.7,49.3,50.95,52.6]    
            Luse_homeowner5 = [9,9,9,9,9,9,9,9,12,12,12,12,12,12,12,12,15,15,15,15,15,15,15,15,15,15,15,15,18,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24]
            Luse_landlord5 = [10,10,10,10,10,10,10,10,13,13,13,13,13,13,13,13,16,16,16,16,16,16,16,16,16,16,16,16,19,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25]
            Luse_tenant5 = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

            ## TABLE 6: A/AE Zone, Basement, Split level, USACE
            dh6 = [-8.0,-7.5,-7.0,-6.5,-6.0,-5.5,-5.0,-4.5,-4.0,-3.5,-3.0,-2.5,-2.0,-1.5,-1.0,-0.5,0.0,0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0,5.5,6.0,6.5,7.0,7.5,8.0,8.5,9.0,9.5,10.0,10.5,11.0,11.5,12.0,12.5,13.0,13.5,14.0,14.5,15.0,15.5,16.0]
            structure_loss6 = [0,0,0,1.25,2.5,2.8,3.1,3.9,4.7,5.95,7.2,8.8,10.4,12.3,14.2,16.35,18.5,20.85,23.2,25.7,28.2,30.8,33.4,36,38.6,41.2,43.8,46.3,48.8,51.15,53.5,55.65,57.8,59.7,61.6,63.2,64.8,66,67.2,68,68.8,69.05,69.3,69.3,69.3,69.3,69.3,69.3,69.3]
            contents_loss6 = [0.6,0.65,0.7,1.05,1.4,1.9,2.4,3.1,3.8,4.6,5.4,6.35,7.3,8.35,9.4,10.5,11.6,12.7,13.8,14.95,16.1,17.15,18.2,19.2,20.2,21.15,22.1,22.85,23.6,24.25,24.9,25.35,25.8,26.05,26.3,26.3,26.3,26.3,26.3,26.3,26.3,26.3,26.3,26.3,26.3,26.3,26.3,26.3,26.3]    
            Luse_homeowner6 = [9.0,9.0,9.0,9.0,9.0,9.0,9.0,9.0,12.0,12.0,12.0,12.0,12.0,12.0,12.0,12.0,15.0,15.0,15.0,15.0,15.0,15.0,15.0,15.0,15.0,15.0,15.0,15.0,18.0,24.0,24.0,24.0,24.0,24.0,24.0,24.0,24.0,24.0,24.0,24.0,24.0,24.0,24.0,24.0,24.0,24.0,24.0,24.0,24.0]
            Luse_landlord6 = [10.0,10.0,10.0,10.0,10.0,10.0,10.0,10.0,13.0,13.0,13.0,13.0,13.0,13.0,13.0,13.0,16.0,16.0,16.0,16.0,16.0,16.0,16.0,16.0,16.0,16.0,16.0,16.0,19.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0,25.0]
            Luse_tenant6 = [1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0]


            ## Table 7. V/VE Zone, With Obstructions

            dh7 = [-8,-7,-6,-5,-4,-3,-2,-1.5,-1,-0.5,0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10,10.5,11,11.5,12,12.5,13,13.5,14,14.5,15,15.5,16]
            structure_loss7 = [0,0,0,0,0,0,20,20.75,21.5,22.75,24,26.5,29,33,37,45.5,54,57.25,60.5,62.5,64.5,66.25,68,69,70,71,72,73,74,75,76,77,78,79,80,80.75,81.5,82.25,83,83.5,84,84.5,85]
            contents_loss7 = [0,0,0,0,0,0,0,5.5,11,17.5,24,26.5,29,33,37,45.5,54,57.5,61,63,65,66.5,68,69.36,70.72,73.36,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76,76]    
            Luse_homeowner7 = [0,0,0,0,0,0,3.6,3.6,4,4,4.7,4.7,6,6,8.2,8.2,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12]
            Luse_landlord7 = [0,0,0,0,0,0,4.6,4.6,5,5,5.7,5.7,7,7,9.2,9.2,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13]
            Luse_tenant7 = [0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

            ###### General table for code **********multiple if conditions would go here
            if zonevalue == "A" or zonevalue == "AE":   # for TABLE 1,2,3,4,5,6
                # for TABLE 1
                if basement == "no" and stories == "One story":            
                    dh= dh1
                    structure_loss = structure_loss1
                    contents_loss = contents_loss1
                    Luse_homeowner = Luse_homeowner1
                    Luse_landlord =  Luse_landlord1
                    Luse_tenant =  Luse_tenant1
                    repair_cost = 110.35
                # for TABLE 2
                elif basement == "no" and stories == "Two or more stories":            
                    dh= dh2
                    structure_loss = structure_loss2
                    contents_loss = contents_loss2
                    Luse_homeowner = Luse_homeowner2
                    Luse_landlord =  Luse_landlord2
                    Luse_tenant =  Luse_tenant2   
                    repair_cost = 106.22
                # for TABLE 3
                elif basement == "no" and stories == "Split level":            
                    dh= dh3
                    structure_loss = structure_loss3
                    contents_loss = contents_loss3
                    Luse_homeowner = Luse_homeowner3
                    Luse_landlord =  Luse_landlord3
                    Luse_tenant =  Luse_tenant3   
                    repair_cost = 110.35  #145 
                # for TABLE 4
                elif basement == "yes" and stories == "One story":            
                    dh= dh4
                    structure_loss = structure_loss4
                    contents_loss = contents_loss4
                    Luse_homeowner = Luse_homeowner4
                    Luse_landlord =  Luse_landlord4
                    Luse_tenant =  Luse_tenant4
                    repair_cost = 110.35 #145
                # for TABLE 5
                elif basement == "yes" and stories == "Two or more stories":            
                    dh= dh5
                    structure_loss = structure_loss5
                    contents_loss = contents_loss5
                    Luse_homeowner = Luse_homeowner5
                    Luse_landlord =  Luse_landlord5
                    Luse_tenant =  Luse_tenant5
                    repair_cost = 106.22  #145
                # for TABLE 6
                elif basement == "yes" and stories == "Split level":            
                    dh= dh6
                    structure_loss = structure_loss6
                    contents_loss = contents_loss6
                    Luse_homeowner = Luse_homeowner6
                    Luse_landlord =  Luse_landlord6
                    Luse_tenant =  Luse_tenant6
                    repair_cost = 106.22  #145
                else:
                    print("Does not match a case for A/AE zones")
    
            elif zonevalue == "X" or zonevalue == "X PROTECTED BY LEVEE" or zonevalue == "0.2 PCT ANNUAL CHANCE FLOOD HAZARD":    # for X zones, use TABLE 1,2
                # for TABLE 1
                if basement == "no" and stories == "One story":            
                    dh= dh1
                    structure_loss = structure_loss1
                    contents_loss = contents_loss1
                    Luse_homeowner = Luse_homeowner1
                    Luse_landlord =  Luse_landlord1
                    Luse_tenant =  Luse_tenant1
                    repair_cost = 110.35
                # for TABLE 2
                elif basement == "no" and stories == "Two or more stories":            
                    dh= dh2
                    structure_loss = structure_loss2
                    contents_loss = contents_loss2
                    Luse_homeowner = Luse_homeowner2
                    Luse_landlord =  Luse_landlord2
                    Luse_tenant =  Luse_tenant2    
                    repair_cost = 106.22
                else:
                    print("Does not match a case for X zones")    
                
            
            elif zonevalue == "V" or zonevalue == "VE":    # for TABLE 7
                dh= dh7
                structure_loss = structure_loss7
                contents_loss = contents_loss7
                Luse_homeowner = Luse_homeowner7
                Luse_landlord =  Luse_landlord7
                Luse_tenant =  Luse_tenant7
                repair_cost = 110.35
            else:
                print("Does not match a zone")
                pass
            
            print("Repair cost : ", repair_cost)
            FFH = []
            for j in range(len(totalBFE)): 
                if zonevalue == "X" or zonevalue == "X PROTECTED BY LEVEE" or zonevalue == "0.2 PCT ANNUAL CHANCE FLOOD HAZARD":
                    FFH.append(BFE + totalBFE[j])
                elif zonevalue == "A" or zonevalue == "AE" or zonevalue == "V" or zonevalue == "VE":  
                    FFH.append(u-a*(np.log(-np.log(1-(1/100))))+totalBFE[j])
 
            AAL_Total_homeowner_list = [] 
            AAL_Total_landlord_list = []   
            AAL_Total_tenant_list = []
            AAL_Total_list = []

            for j in range(len(totalBFE)):  
                print("FFH : ", FFH[j])  

                # step 1
                print("             ******  step 1  *****             ")
                print("                  ")

                d = []
                for i in range(len(dh)):
                    d.append(dh[i]+FFH[j])
                #print("d = ", d)    


                # step 2
                print("                  ")
                print("             ******  step 2  *****             ")
                print("                  ")

                p = []
                for i in range(len(d)):
                    p.append(1-(math.exp(-math.exp(-(d[i]-u)/a))))
                #print("P = ", p)    

                # step 3
                print("                  ")
                print("             ******  step 3  *****             ")
                print("                  ")

                aStruct = []
                for i in range(len(p)-1):
                    aStruct.append((p[i]-p[i+1])*(structure_loss[i]+structure_loss[i+1])/2.0)
                aStruct.append(0)                                      
                # print("aStruct = ", aStruct)    
                # print("length of aStruct = ", len(aStruct))  

                aCont = []
                for i in range(len(p)-1):
                    aCont.append((p[i]-p[i+1])*(contents_loss[i]+contents_loss[i+1])/2.0)
                aCont.append(0)                                     
                # print("aCont = ", aCont)    
                # print("length of aCont = ", len(aCont))  

                aUse_homeowner = []
                for i in range(len(p)-1):
                    aUse_homeowner.append((p[i]-p[i+1])*(Luse_homeowner[i]+Luse_homeowner[i+1])/2.0)
                aUse_homeowner.append(0)                                     
                # print("aUse_homeowner = ", aUse_homeowner)    
                # print("length of aUse_homeowner = ", len(aUse_homeowner))  


                aUse_landlord = []
                for i in range(len(p)-1):
                    aUse_landlord.append((p[i]-p[i+1])*(Luse_landlord[i]+Luse_landlord[i+1])/2.0)
                aUse_landlord.append(0)                                     
                # print("aUse_landlord = ", aUse_landlord)    
                # print("length of aUse_landlord  = ", len(aUse_landlord))  


                aUse_tenant = []
                for i in range(len(p)-1):
                    aUse_tenant.append((p[i]-p[i+1])*(Luse_tenant[i]+Luse_tenant[i+1])/2.0)
                aUse_tenant.append(0)                                     
                # print("aUse_tenant = ", aUse_tenant)    
                # print("length of aUse_tenant = ", len(aUse_tenant))  


                # # step 4
                print("                  ")
                print("             ******  step 4  *****             ")
                print("                  ")

                AALStruct = 0.0
                AALCont = 0.0
                AALUse_homeowner = 0.0
                AALUse_landlord  = 0.0
                AALUse_tenant = 0.0

                for i in range(len(p)):
                    AALStruct = AALStruct + aStruct[i]
                    AALCont   = AALCont + aCont[i]
                    AALUse_homeowner    = AALUse_homeowner + aUse_homeowner[i]
                    AALUse_landlord    = AALUse_landlord + aUse_landlord[i]
                    AALUse_tenant    = AALUse_tenant + aUse_tenant[i]

                # print("AALStruct = ", AALStruct)
                # print("AALCont = ", AALCont)
                # print("AALUse_homeowner = ", AALUse_homeowner) 
                # print("AALUse_landlord = ", AALUse_landlord) 
                # print("AALUse_tenant = ", AALUse_tenant)    


                # # step 5 (careful with if conditions)
                print("                  ")
                print("             ******  step 5  *****             ")
                print("                  ")

                homeowner_AALstruct = round((AALStruct/100.0)* repair_cost * building_area,0)

                if zonevalue == "A" or zonevalue == "AE" or zonevalue == "X" or zonevalue == "X PROTECTED BY LEVEE" or zonevalue == "0.2 PCT ANNUAL CHANCE FLOOD HAZARD":
                    #for A/AE zone
                    homeowner_AALcont = round((AALCont/100.0)* repair_cost * building_area,0)

                elif zonevalue == "V" or zonevalue == "VE":
                    #for V/VE zone
                    homeowner_AALcont = round((AALCont/100.0)* repair_cost * building_area *0.5,0)
                else:
                    pass


                ## if building value is present
                homeowner_AALuse = round((AALUse_homeowner/84.0)* Building_value,0)       

                
                ###if no building value, use repair_cost * building_area 
                ##owner_occupant_use = round((AALUse_homeowner/84.0)* repair_cost * building_area,0)  

               # print("homeowner_AALstruct = ",homeowner_AALstruct, ",   homeowner_AALcont = ",homeowner_AALcont, ",   homeowner_AALuse = ",homeowner_AALuse)




                landlord_AALstruct = homeowner_AALstruct
                landlord_AALcont = 0
                landlord_AALuse = round((AALUse_landlord/84.0)* Building_value,0) 


                #print("landlord-AALstruct = ",landlord_AALstruct, ",   landlord-AALcont = ",landlord_AALcont, ",   landlord-AALuse = ",landlord_AALuse)


                tenant_AALstruct = 0
                tenant_AALcont = homeowner_AALcont
                tenant_AALuse = round(145 * 30 * AALUse_tenant, 0) 
                
                
                #print("tenant_AALstruct = ",tenant_AALstruct, ",   tenant_AALcont = ",tenant_AALcont, ",   tenant_AALuse= ",tenant_AALuse)




                # step 6
                print("                  ")
                print("             ******  step 6  *****             ")
                print("                  ")

                AAL_Total_homeowner = homeowner_AALstruct + homeowner_AALcont + homeowner_AALuse
                #print("AAL_Total_homeowner = ", AAL_Total_homeowner)
                AAL_Total_landlord = landlord_AALstruct + landlord_AALcont + landlord_AALuse
                #print("AAL_Total_landlord = ", AAL_Total_landlord)
                AAL_Total_tenant = tenant_AALstruct + tenant_AALcont + tenant_AALuse
                #print("AAL_Total_tenant = ", AAL_Total_tenant)

                AAL_Total_homeowner_list.append(AAL_Total_homeowner)
                AAL_Total_landlord_list.append(AAL_Total_landlord)
                AAL_Total_tenant_list.append(AAL_Total_tenant)

                ########################################################
                if user_type == "Homeowner":
                    AAL_Total = AAL_Total_homeowner
                elif user_type == "Tenant":
                    AAL_Total = AAL_Total_tenant
                elif user_type == "Landlord":
                    AAL_Total = AAL_Total_landlord
                # elif user_type == "Community official":
                #     AAL_Total == AAL_Total_CommunityOfficial
                else:
                    print("None of the user type!")
                    AAL_Total = AAL_Total_homeowner #"NONE"   #fix it later
                    print("AAL total = ", AAL_Total)

                print("                  ") 
                print("AAL total = ", AAL_Total)
                AAL_Total_list.append(AAL_Total)  

                print("**********          ###########          ***********")

            # print("AAL_Total_homeowner_list : ", AAL_Total_homeowner_list) 
            # print("AAL_Total_landlord_list : ", AAL_Total_landlord_list)   
            # print("AAL_Total_tenant_list : ", AAL_Total_tenant_list)
            AAL_Total_list_c.append(AAL_Total_list)
            # print("AAL_Total_list_c : ", AAL_Total_list_c)
            # print("                    ")

            #AAL_Total_listnoBFE0 = AAL_Total_list
            #AAL_Total_listnoBFE0 = AAL_Total_listnoBFE0.remove(AAL_Total_listnoBFE0[0])
            AAL_Total_list_json = simplejson.dumps(AAL_Total_list)  
            optimal_AAL_Total_list = min(AAL_Total_list)

            for k in range(len(AAL_Total_list)):
                if optimal_AAL_Total_list == AAL_Total_list[k]:
                    optimal_AAL_Total_list_freeboard = totalBFE[k]

            optimal_AAL_Total_list_json = simplejson.dumps(optimal_AAL_Total_list)  
            #

            avoided_annual_loss_homeowner= []
            avoided_annual_loss_landlord= []
            avoided_annual_loss_tenant= []
            avoided_monthly_loss_homeowner= []
            avoided_monthly_loss_landlord= []
            avoided_monthly_loss_tenant= []
            for k in range(len(totalBFE)):
                avoided_annual_loss_homeowner.append(AAL_Total_homeowner_list[0]- AAL_Total_homeowner_list[k])
                avoided_annual_loss_landlord.append(AAL_Total_landlord_list[0]- AAL_Total_landlord_list[k])
                avoided_annual_loss_tenant.append(AAL_Total_tenant_list[0]- AAL_Total_tenant_list[k])
                avoided_monthly_loss_homeowner.append(int(((AAL_Total_homeowner_list[0]- AAL_Total_homeowner_list[k])/12)))
                avoided_monthly_loss_landlord.append(int(((AAL_Total_landlord_list[0]- AAL_Total_landlord_list[k])/12)))
                avoided_monthly_loss_tenant.append(int(((AAL_Total_tenant_list[0]- AAL_Total_tenant_list[k])/12)))


            # print("avoided_annual_loss_homeowner : ", avoided_annual_loss_homeowner) 
            # print("avoided_annual_loss_landlord : ", avoided_annual_loss_landlord)   
            # print("avoided_annual_loss_tenant : ", avoided_annual_loss_tenant)
            # print("       ")
            # print("avoided_monthly_loss_homeowner : ", avoided_monthly_loss_homeowner) 
            # print("avoided_monthly_loss_landlord : ", avoided_monthly_loss_landlord)   
            # print("avoided_monthly_loss_tenant : ", avoided_monthly_loss_tenant)
            avoided_monthly_loss_homeowner_list_c.append(avoided_monthly_loss_homeowner)
            avoided_monthly_loss_landlord_list_c.append(avoided_monthly_loss_landlord)
            avoided_monthly_loss_tenant_list_c.append(avoided_monthly_loss_tenant)

              


            print("                  ")
            print("             ******  New AAL method ends  *****             ")
            print("                  ")

        ##----------------------AAL (Adil's method) ends ---------------------------------------

            ##
            annual_avoided_loss = []
            monthly_avoided_loss = []
            if user_type == "Homeowner":
                annual_avoided_loss = avoided_annual_loss_homeowner
                monthly_avoided_loss = avoided_monthly_loss_homeowner
            elif user_type == "Tenant":
                annual_avoided_loss = avoided_annual_loss_tenant
                monthly_avoided_loss = avoided_monthly_loss_tenant
                
            elif user_type == "Landlord":
                annual_avoided_loss = avoided_annual_loss_landlord
                monthly_avoided_loss = avoided_monthly_loss_landlord

            # elif user_type == "Community official":
            #     annual_avoided_loss = avoided_annual_loss_CommunityOfficial
            #     monthly_avoided_loss = avoided_monthly_loss_CommunityOfficial
            else:
                print("None of the user type!")
                annual_avoided_loss =  avoided_annual_loss_homeowner #"NONE"   #fix it later
                monthly_avoided_loss = avoided_monthly_loss_homeowner #"NONE"  #fix it later
                print("annual_avoided_loss = ", annual_avoided_loss)
                print("monthly_avoided_loss = ", monthly_avoided_loss)

            #annual_avoided_lossnoBFE0 = annual_avoided_loss.remove(annual_avoided_loss[0])
            #monthly_avoided_lossnoBFE0 = monthly_avoided_loss.remove(monthly_avoided_loss[0])
            
            annual_avoided_loss_json = simplejson.dumps(annual_avoided_loss)   
            monthly_avoided_loss_json = simplejson.dumps(monthly_avoided_loss[1:])     #**   

            print("                  ") 
            print("annual_avoided_loss = ", annual_avoided_loss)
            print("monthly_avoided_loss = ", monthly_avoided_loss)
            annual_avoided_loss_list_c.append(annual_avoided_loss)  
            monthly_avoided_loss_list_c.append(monthly_avoided_loss)
         


        ###----------------Insurance-----------------------------------------

            #------ coverage level--------------

            #coverage_lvl_bldg = Building_value
            #coverage_lvl_cont = Building_value * 0.4
            print("coverage_lvl_bldg", coverage_lvl_bldg)
            print("coverage_lvl_cont", coverage_lvl_cont)

            #--table--Zones AE, A, A1-A30------array values are BFE, BFE+1, BFE+2, BFE+3, BFE+5---- 
            if zonevalue == "AE" :
                #--one story
                BasicRate_1s_Bldg_BFE = [2.21,0.94,0.50,0.34,0.31]
                AddiRate_1s_Bldg_BFE = [0.26,0.17,0.11,0.09,0.08]
                BasicRate_1s_Cont_BFE = [1.02,0.53,0.38,0.38,0.38]
                AddiRate_1s_Cont_BFE = [0.12,0.12,0.12,0.12,0.12]
                print("one story")
                #--twostory
                BasicRate_2s_Bldg_BFE = [1.75,0.78,0.43,0.31,0.27]
                AddiRate_2s_Bldg_BFE = [0.08,0.08,0.08,0.08,0.08]
                BasicRate_2s_Cont_BFE = [0.75,0.40,0.38,0.38,0.38]
                AddiRate_2s_Cont_BFE = [0.12,0.12,0.12,0.12,0.12]
                print("two or more stories")

                # #--one story below+
                # BasicRate_1s_Bldg_BFE = [11.90, 9.85, 7.93, 5.37, 2.21,0.94,0.50,0.34,0.31]
                # AddiRate_1s_Bldg_BFE = [1.79, 1.19, 0.70, 0.36, 0.26,0.17,0.11,0.09,0.08]
                # BasicRate_1s_Cont_BFE = [6.53, 5.02, 3.69, 2.33, 1.02,0.53,0.38,0.38,0.38]
                # AddiRate_1s_Cont_BFE = [0.24, 0.24, 0.14, 0.12, 0.12,0.12,0.12,0.12,0.12]
                # print("one story below+")
                # #--twostory below+
                # BasicRate_2s_Bldg_BFE = [10.08, 8.17, 6.40, 4.31, 1.75,0.78,0.43,0.31,0.27]
                # AddiRate_2s_Bldg_BFE = [0.37, 0.22, 0.13, 0.08, 0.08,0.08,0.08,0.08,0.08]
                # BasicRate_2s_Cont_BFE = [5.02, 3.80, 2.75, 1.77, 0.75,0.40,0.38,0.38,0.38]
                # AddiRate_2s_Cont_BFE = [0.12, 0.12, 0.12, 0.12, 0.12,0.12,0.12,0.12,0.12]
                # print("two or more stories below+")
            #--table--Zones Unnumbered A------array values are BFE, BFE+1, BFE+2, BFE+3, BFE+5---- 
            elif zonevalue == "A" :                                  ####to be changed, what should go for zone unnumbered A?
                #--one story
                BasicRate_1s_Bldg_BFE = [2.67,2.67,0.57,0.57,0.57]
                AddiRate_1s_Bldg_BFE = [0.20,0.20,0.10,0.10,0.10]
                BasicRate_1s_Cont_BFE = [1.20,1.20,0.32,0.32,0.32]
                AddiRate_1s_Cont_BFE = [0.09,0.09,0.08,0.08,0.08]
                #--twostory
                BasicRate_2s_Bldg_BFE = [2.67,2.67,0.57,0.57,0.57]
                AddiRate_2s_Bldg_BFE = [0.20,0.20,0.10,0.10,0.10]
                BasicRate_2s_Cont_BFE = [1.20,1.20,0.32,0.32,0.32]
                AddiRate_2s_Cont_BFE = [0.09,0.09,0.08,0.08,0.08]

                # #--one story below+
                # BasicRate_1s_Bldg_BFE = [6.31, 6.31, 6.31, 6.31, 2.67,2.67,0.57,0.57,0.57]
                # AddiRate_1s_Bldg_BFE = [0.35, 0.35, 0.35, 0.35, 0.20,0.20,0.10,0.10,0.10]
                # BasicRate_1s_Cont_BFE = [2.71, 2.71, 2.71, 2.71, 1.20,1.20,0.32,0.32,0.32]
                # AddiRate_1s_Cont_BFE = [0.16, 0.16, 0.16, 0.16, 0.09,0.09,0.08,0.08,0.08]
                # #--twostory below+
                # BasicRate_2s_Bldg_BFE = [6.31, 6.31, 6.31, 6.31, 2.67,2.67,0.57,0.57,0.57]
                # AddiRate_2s_Bldg_BFE = [0.35, 0.35, 0.35, 0.35, 0.20,0.20,0.10,0.10,0.10]
                # BasicRate_2s_Cont_BFE = [2.71, 2.71, 2.71, 2.71, 1.20,1.20,0.32,0.32,0.32]
                # AddiRate_2s_Cont_BFE = [0.16, 0.16, 0.16, 0.16, 0.09,0.09,0.08,0.08,0.08]


            #--table--Zones V, V1-V30, VE------array values are BFE, BFE+1, BFE+2, BFE+3, BFE+5---- 
            elif  zonevalue == "VE":
                #--one story
                BasicRate_1s_Bldg_BFE = [3.28,2.67,2.18,1.79,1.51]
                AddiRate_1s_Bldg_BFE = [3.28,2.67,2.18,1.79,1.51]
                BasicRate_1s_Cont_BFE = [2.54,1.94,1.47,1.03,0.93]
                AddiRate_1s_Cont_BFE = [2.54,1.94,1.47,1.03,0.93]
                #--twostory
                BasicRate_2s_Bldg_BFE = [3.28,2.67,2.18,1.79,1.51]
                AddiRate_2s_Bldg_BFE = [3.28,2.67,2.18,1.79,1.51]
                BasicRate_2s_Cont_BFE = [2.54,1.94,1.47,1.03,0.93]
                AddiRate_2s_Cont_BFE = [2.54,1.94,1.47,1.03,0.93]

                # #--one story below+
                # BasicRate_1s_Bldg_BFE = [5.85, 5.85, 4.88, 4.04, 3.28, 2.67,2.18,1.79,1.51]
                # AddiRate_1s_Bldg_BFE = [5.85, 5.85, 4.88, 4.04, 3.28, 2.67,2.18,1.79,1.51]
                # BasicRate_1s_Cont_BFE = [5.09, 5.09, 4.14, 3.28, 2.54, 1.94,1.47,1.03,0.93]
                # AddiRate_1s_Cont_BFE = [5.09, 5.09, 4.14, 3.28, 2.54, 1.94,1.47,1.03,0.93]
                # #--twostory below+
                # BasicRate_2s_Bldg_BFE = [5.85, 5.85, 4.88, 4.04, 3.28,2.67,2.18,1.79,1.51]
                # AddiRate_2s_Bldg_BFE = [5.85, 5.85, 4.88, 4.04, 3.28,2.67,2.18,1.79,1.51]
                # BasicRate_2s_Cont_BFE = [5.09, 5.09, 4.14, 3.28, 2.54,1.94,1.47,1.03,0.93]
                # AddiRate_2s_Cont_BFE = [5.09, 5.09, 4.14, 3.28, 2.54,1.94,1.47,1.03,0.93]


            #--table--Zones X------array values are BFE, BFE+1, BFE+2, BFE+3, BFE+5---- 
            elif zonevalue == "X" or zonevalue == "X PROTECTED BY LEVEE" or zonevalue == "0.2 PCT ANNUAL CHANCE FLOOD HAZARD": 
                #--one story
                BasicRate_1s_Bldg_BFE = [1.11,1.11,1.11,1.11,1.11]
                AddiRate_1s_Bldg_BFE = [0.31,0.31,0.31,0.31,0.31]
                BasicRate_1s_Cont_BFE = [1.71,1.71,1.71,1.71,1.71]
                AddiRate_1s_Cont_BFE = [0.54,0.54,0.54,0.54,0.54]
                #--twostory
                BasicRate_2s_Bldg_BFE = [1.11,1.11,1.11,1.11,1.11]
                AddiRate_2s_Bldg_BFE = [0.31,0.31,0.31,0.31,0.31]
                BasicRate_2s_Cont_BFE = [1.71,1.71,1.71,1.71,1.71]
                AddiRate_2s_Cont_BFE = [0.54,0.54,0.54,0.54,0.54]

                # #--one story below+
                # BasicRate_1s_Bldg_BFE = [1.11,1.11,1.11,1.11,1.11,1.11,1.11,1.11,1.11]
                # AddiRate_1s_Bldg_BFE = [0.31,0.31,0.31,0.31,0.31,0.31,0.31,0.31,0.31]
                # BasicRate_1s_Cont_BFE = [1.71,1.71,1.71,1.71,1.71,1.71,1.71,1.71,1.71]
                # AddiRate_1s_Cont_BFE = [0.54,0.54,0.54,0.54,0.54,0.54,0.54,0.54,0.54]
                # #--twostory below+
                # BasicRate_2s_Bldg_BFE = [1.11,1.11,1.11,1.11,1.11,1.11,1.11,1.11,1.11]
                # AddiRate_2s_Bldg_BFE = [0.31,0.31,0.31,0.31,0.31,0.31,0.31,0.31,0.31]
                # BasicRate_2s_Cont_BFE = [1.71,1.71,1.71,1.71,1.71,1.71,1.71,1.71,1.71]
                # AddiRate_2s_Cont_BFE = [0.54,0.54,0.54,0.54,0.54,0.54,0.54,0.54,0.54]
            else:
                print("Flood zone does not match")

            ##---Premium fees----------------
            ICC_premium = 6
            Reserve_fund = 0.18
            HFIAA_surcharge = 25
            Federal_policy_fee = 50
            

            ##----insurance limits----------
            basic_bldg_insurance_limit = 0
            addi_bldg_insurance_amnt = 0
            basic_cont_insurance_limit = 0
            addi_cont_insurance_amnt = 0

            if coverage_lvl_bldg <= 60000:
                basic_bldg_insurance_limit  = coverage_lvl_bldg                 # demo-must be changed
                addi_bldg_insurance_amnt = 0                  # demo-must be changed
                print("building basic : ", basic_bldg_insurance_limit)
                print("building additional : ", addi_bldg_insurance_amnt)

            elif coverage_lvl_bldg > 60000 and coverage_lvl_bldg<= 250000:
                basic_bldg_insurance_limit  = 60000                  # demo-must be changed
                addi_bldg_insurance_amnt = coverage_lvl_bldg-60000                  # demo-must be changed
                print("building basic : ", basic_bldg_insurance_limit)
                print("building additional : ", addi_bldg_insurance_amnt)
            else:
                print("Building coverage level exceeds the limit")
                pass

            if coverage_lvl_cont <= 25000:
                basic_cont_insurance_limit = coverage_lvl_cont                  # demo-must be changed
                addi_cont_insurance_amnt = 0                  # demo-must be changed
                print("content basic : ", basic_cont_insurance_limit)
                print("content additional : ", addi_cont_insurance_amnt)
            elif coverage_lvl_cont > 25000 and coverage_lvl_cont <= 100000:
                basic_cont_insurance_limit = 25000                 # demo-must be changed
                addi_cont_insurance_amnt = coverage_lvl_cont-25000                  # demo-must be changed
                print("content basic : ", basic_cont_insurance_limit)
                print("content additional : ", addi_cont_insurance_amnt)
            else:
                print("Content coverage level exceeds the limit")
                pass


            ##----Premium deductible table------


            if deductible_bldg==1000 and deductible_cont==1000:
                fullrisk = 1.000

            elif deductible_bldg==1250 and deductible_cont==1000:
                fullrisk = 0.995
            elif deductible_bldg==1250 and deductible_cont==1250:
                fullrisk = 0.980

            elif deductible_bldg==1500 and deductible_cont==1000:
                fullrisk = 0.990
            elif deductible_bldg==1500 and deductible_cont==1250:
                fullrisk = 0.975
            elif deductible_bldg==1500 and deductible_cont==1500:
                fullrisk = 0.965

            elif deductible_bldg==2000 and deductible_cont==1000:
                fullrisk = 0.975
            elif deductible_bldg==2000 and deductible_cont==1250:
                fullrisk = 0.965
            elif deductible_bldg==2000 and deductible_cont==1500:
                fullrisk = 0.950
            elif deductible_bldg==2000 and deductible_cont==2000:
                fullrisk = 0.925

            elif deductible_bldg==3000 and deductible_cont==1000:
                fullrisk = 0.950
            elif deductible_bldg==3000 and deductible_cont==1250:
                fullrisk = 0.940
            elif deductible_bldg==3000 and deductible_cont==1500:
                fullrisk = 0.925
            elif deductible_bldg==3000 and deductible_cont==2000:
                fullrisk = 0.900
            elif deductible_bldg==3000 and deductible_cont==3000:
                fullrisk = 0.850

            elif deductible_bldg==4000 and deductible_cont==1000:
                fullrisk = 0.925
            elif deductible_bldg==4000 and deductible_cont==1250:
                fullrisk = 0.915
            elif deductible_bldg==4000 and deductible_cont==1500:
                fullrisk = 0.900
            elif deductible_bldg==4000 and deductible_cont==2000:
                fullrisk = 0.875
            elif deductible_bldg==4000 and deductible_cont==3000:
                fullrisk = 0.825
            elif deductible_bldg==4000 and deductible_cont==4000:
                fullrisk = 0.775

            elif deductible_bldg==5000 and deductible_cont==1000:
                fullrisk = 0.900
            elif deductible_bldg==5000 and deductible_cont==1250:
                fullrisk = 0.890
            elif deductible_bldg==5000 and deductible_cont==1500:
                fullrisk = 0.875
            elif deductible_bldg==5000 and deductible_cont==2000:
                fullrisk = 0.850
            elif deductible_bldg==5000 and deductible_cont==3000:
                fullrisk = 0.800
            elif deductible_bldg==5000 and deductible_cont==4000:
                fullrisk = 0.760
            elif deductible_bldg==5000 and deductible_cont==5000:
                fullrisk = 0.750

            elif deductible_bldg==10000 and deductible_cont==10000:
                fullrisk = 0.600    
            else:
                pass    

            total_bldg_BasicCoverage = []
            total_bldg_AddiCoverage = []
            total_cont_BasicCoverage = []
            total_cont_AddiCoverage = []    
            principle_premium = []
            deducted_premium = []
            total_annual_premium = []
            total_monthly_premium = []

            


            for i in range(len(totalBFE)):

                if No_Floors == "One story" :    
                    #print("one one one")
                    total_bldg_BasicCoverage.append( (( basic_bldg_insurance_limit )/100) * BasicRate_1s_Bldg_BFE[i])
                    total_bldg_AddiCoverage.append( (( addi_bldg_insurance_amnt )/100) * AddiRate_1s_Bldg_BFE[i])

                    total_cont_BasicCoverage.append( (( basic_cont_insurance_limit )/100) * BasicRate_1s_Cont_BFE[i])
                    total_cont_AddiCoverage.append( (( addi_cont_insurance_amnt )/100) * AddiRate_1s_Cont_BFE[i])
                    # print("basicrate_B : ", BasicRate_1s_Bldg_BFE[i])
                    # print("additionalraterate_B : ", AddiRate_1s_Bldg_BFE[i])
                    # print("basicrate_C : ", BasicRate_1s_Cont_BFE[i])
                    # print("additionalraterate_C : ", AddiRate_1s_Cont_BFE[i])
                    # print("total building basic cov : ",  total_bldg_BasicCoverage, "total building additional cov : ", total_bldg_AddiCoverage)
                    # print("total content basic cov : ",  total_cont_BasicCoverage, "total content additional cov : ", total_cont_AddiCoverage)
                elif No_Floors == "Two or more stories" : 
                    #print("two two two")
                    total_bldg_BasicCoverage.append( (( basic_bldg_insurance_limit )/100) * BasicRate_2s_Bldg_BFE[i])
                    total_bldg_AddiCoverage.append( (( addi_bldg_insurance_amnt )/100) * AddiRate_2s_Bldg_BFE[i])

                    total_cont_BasicCoverage.append( (( basic_cont_insurance_limit )/100) * BasicRate_2s_Cont_BFE[i])
                    total_cont_AddiCoverage.append( (( addi_cont_insurance_amnt )/100) * AddiRate_2s_Cont_BFE[i])
                else:
                    pass

                principle_premium.append(round(((total_bldg_BasicCoverage[i] + total_bldg_AddiCoverage[i]) + (total_cont_BasicCoverage[i] + total_cont_AddiCoverage[i])),0))

                #deductible factor d is fullrisk
                deducted_premium.append(round((principle_premium[i] * fullrisk),0))
                #print("Deducted premium : ", deducted_premium)

                #total_annual_premium.append( int(((deducted_premium[i] + ICC_premium - CRS) + Reserve_fund * (deducted_premium[i] + ICC_premium - CRS)) + HFIAA_surcharge + Federal_policy_fee))
                total_annual_premium.append( int(((deducted_premium[i] + ICC_premium - CRS*(deducted_premium[i] + ICC_premium)) + Reserve_fund * (deducted_premium[i] + ICC_premium - CRS*(deducted_premium[i] + ICC_premium))) + HFIAA_surcharge + Federal_policy_fee))
                total_monthly_premium.append( int((((deducted_premium[i] + ICC_premium - CRS*(deducted_premium[i] + ICC_premium)) + Reserve_fund * (deducted_premium[i] + ICC_premium - CRS*(deducted_premium[i] + ICC_premium))) + HFIAA_surcharge + Federal_policy_fee)/12))
       

                print("Total annual premium : ", total_annual_premium)
                print("Total monthly premium : ", total_monthly_premium)
                
                #total_annual_premiumnoBFE0 = total_annual_premium.remove(total_annual_premium[0])
                #total_monthly_premiumnoBFE0 = total_monthly_premium.remove(total_monthly_premium[0])
                total_annual_premium_json = simplejson.dumps(total_annual_premium)  
                total_monthly_premium_json = simplejson.dumps(total_monthly_premium) 

                optimal_total_annual_premium = min(total_annual_premium)
                optimal_total_monthly_premium = min(total_monthly_premium)
            
                for k in range(len(total_annual_premium)):
                    if optimal_total_annual_premium == total_annual_premium[k]:
                        optimal_total_annual_premium_freeboard = totalBFE[k]

                for k in range(len(total_monthly_premium)):
                    if optimal_total_monthly_premium == total_monthly_premium[k]:
                        optimal_total_monthly_premium_freeboard = totalBFE[k]  

            #optimal_total_annual_premiumnoBFE0 = optimal_total_annual_premium.remove(optimal_total_annual_premium[0])
            optimal_total_annual_premium_json = simplejson.dumps(optimal_total_annual_premium)  
            print("Deducted premium : ", deducted_premium)
            print("Total annual premium : ", total_annual_premium)
            total_annual_premium_list_c.append(total_annual_premium)

            #optimal_total_monthly_premiumnoBFE0 = optimal_total_monthly_premium.remove(optimal_total_monthly_premium[0])
            optimal_total_monthly_premium_json = simplejson.dumps(optimal_total_monthly_premium)  
            print("Deducted premium : ", deducted_premium)
            print("Total monthly premium : ", total_monthly_premium)
            total_monthly_premium_list_c.append(total_monthly_premium)
        
            ###---------------Insurance ends---------------------------------------

            


            ##---------------Amortized freeboard cost--------------------------
            Amortized_FC = []
            for i in range(len(totalBFE)): 
                principle_monthly_payment = (freeboardCost[i] * (r/n))/(1-((1+(r/n))**(-n*t)))
                loan_fees = principle_monthly_payment * 0.07
                Amortized_FC.append(int(principle_monthly_payment + loan_fees))

            Amortized_FC_list_c.append(Amortized_FC)
            #Amortized_FC_jsonnoBFE0 = Amortized_FC_json.remove(Amortized_FC_json[0])
            Amortized_FC_json = simplejson.dumps(Amortized_FC[1:0])   #**    

            print("Amortised cost :  ", Amortized_FC)

               ## for switching fc to amfc
            optimal_am_freeboardCost = max(Amortized_FC)
            
            for k in range(len(Amortized_FC)):
                if optimal_am_freeboardCost == Amortized_FC[k]:
                    optimal_freeboard_am_freeboardCost = totalBFE[k]


            optimal_am_freeboardCost_json = simplejson.dumps(optimal_am_freeboardCost)  
                ##

            # ##--------------Avoided annual loss and monthly avoided loss (Ehab's method)---------------------------------    ####check*********
            # annual_avoided_loss = []
            
            # for i in range(len(totalBFE)):                                ###check************ i+1
            #     annual_avoided_loss.append(AAL_absCurrency[4]-AAL_absCurrency[i])          
            # print("Avoided annual loss :  ", annual_avoided_loss)

            # annual_avoided_loss_json = simplejson.dumps(annual_avoided_loss)  

            # monthly_avoided_loss = []
            # for i in range(len(totalBFE)): 
            #     monthly_avoided_loss.append(int(annual_avoided_loss[i]/12))
            # print("Avoided monthly loss :  ", monthly_avoided_loss)
            # monthly_avoided_loss_list_c.append(monthly_avoided_loss)

            # monthly_avoided_loss_json = simplejson.dumps(monthly_avoided_loss)

            ##-----------------Annual and monthly premium saving------------------------------         ###check************
            annual_premium_saving = []
            
            for i in range(len(totalBFE)):                                   ###check************ i+1
                annual_premium_saving.append(total_annual_premium[0]-total_annual_premium[i])    
            print("Annual premium saving :  ", annual_premium_saving)
            annual_premium_saving_json = simplejson.dumps(annual_premium_saving)  

            monthly_premium_saving = []
            for i in range(len(totalBFE)):
                monthly_premium_saving.append(int(annual_premium_saving[i]/12))
            print("Monthly premium saving :  ", monthly_premium_saving)
            total_monthly_premium_saving_list_c.append(monthly_premium_saving)
            monthly_premium_saving_json = simplejson.dumps(monthly_premium_saving[1:])         #**


            ##-----------Total monthly saving---------------------------------------------
            total_monthly_saving = []
            
            for i in range(len(totalBFE)): 
                total_monthly_saving.append(int((annual_premium_saving[i]/12)+(annual_avoided_loss[i]/12)-Amortized_FC[i]))
            print("Total monthly saving :  ", total_monthly_saving)
            total_monthly_saving_list_c.append(total_monthly_saving)
            
            optimal_saving = max(total_monthly_saving)
            total_optimal_saving_list_c.append(max(total_monthly_saving))
            
            for k in range(len(total_monthly_saving)):
                if optimal_saving == total_monthly_saving[k]:
                    optimal_freeboard = totalBFE[k]
            total_optimal_freeboard_list_c.append(optimal_freeboard)

            total_monthly_saving_json = simplejson.dumps(total_monthly_saving[1:])   #**  
            optimal_saving_json = simplejson.dumps(optimal_saving)  

            ##-----------Total yearly saving---------------------------------------------
            total_yearly_saving = []
            for i in range(len(totalBFE)): 
                total_yearly_saving.append(int(total_monthly_saving[i] * 12))
            print("Total yearly saving :  ", total_yearly_saving)
            

            ##-----------Total loanbased freeboard cost---------------------------------------------
            total_loanbased_FC = []
            for i in range(len(totalBFE)): 
                total_loanbased_FC.append(round(Amortized_FC[i] * 12 * t,2))
            print("Total loanbased freeboard cost :", total_loanbased_FC)

            ##---------Time to recover freeboard cost through premium savings alone------------
            time_to_recover_FC_PS = []
            #time_to_recover_FC_PS.append(round(total_loanbased_FC[i]/annual_premium_saving[i],1))
            for i in range(len(totalBFE)):
                if annual_premium_saving[i] == 0:
                    time_to_recover_FC_PS.append(0)    ##
                else:    
                    time_to_recover_FC_PS.append(round(total_loanbased_FC[i]/annual_premium_saving[i],1))
            print("Time to recover FC PS :", time_to_recover_FC_PS)
                
            time_to_recover_FC_PS_json = simplejson.dumps(time_to_recover_FC_PS)     
            time_to_recover_FC_PS_list_c.append(time_to_recover_FC_PS)
            
            ##---------Time to recover freeboard cost through avoided annual loss alone------------
            time_to_recover_FC_AvAL = []
            #time_to_recover_FC_AvAL.append(round(total_loanbased_FC[i]/annual_avoided_loss[i],1))
            for i in range(len(totalBFE)):
                if annual_avoided_loss[i] == 0:
                    time_to_recover_FC_AvAL.append(0) ##
                else:    
                    time_to_recover_FC_AvAL.append(round(total_loanbased_FC[i]/annual_avoided_loss[i],1))
            print("Time to recover FC AvAL :", time_to_recover_FC_AvAL)

            
            ##---------Time to recover freeboard cost through total benefit------------
            time_to_recover_FC_TB = []
            #time_to_recover_FC_TB.append(round(total_loanbased_FC[i]/(annual_premium_saving[i] + annual_avoided_loss[i]),1))   
            #print("Time to recover freeboard cost through total benefit", time_to_recover_FC_TB)
            for i in range(len(totalBFE)):
                if (annual_premium_saving[i] + annual_avoided_loss[i]) == 0:
                    time_to_recover_FC_TB.append(0) ##
                else:    
                    time_to_recover_FC_TB.append(round(total_loanbased_FC[i]/(annual_premium_saving[i] + annual_avoided_loss[i]),1))    

            print("Time to recover freeboard cost through total benefit", time_to_recover_FC_TB)
            time_to_recover_FC_TB_list_c.append(time_to_recover_FC_TB)
            time_to_recover_FC_TB_json = simplejson.dumps(time_to_recover_FC_TB)  

        ##---------Time to recover freeboard cost through monthly savings------------
            time_to_recover_FC_MS = []
            for i in range(len(totalBFE)):
                if (total_monthly_saving[i] == 0):
                    time_to_recover_FC_MS.append(0) ##
                else:    
                    time_to_recover_FC_MS.append(round((total_loanbased_FC[i]/(total_monthly_saving[i])),1) ) 
            print("Time to recover freeboard cost through monthly savings", time_to_recover_FC_MS)

            time_to_recover_FC_MS_json = simplejson.dumps(time_to_recover_FC_MS)       

            ##----------------------------------------------------------------------------
        

            # ##---------------------total cost------------------------------
            # totalcost = []
            # for i in range(len(AAL_absCurrency)):
            #     totalcost.append(round((AAL_absCurrency[i]+total_annual_premium[i])*12+freeboardCost[i],3))    #discounted present value, estimated from:   1(1+R_D )^t = 12  for 7% real discount rate
            


            output_data.writerow({'Address': beforecomma,  'Lattitude': lat, 'Longitude': lon, 'Parish': parishvalue , 'Flood zone':zonevalue , 'Individual building optimal saving': optimal_saving , 'Individual building recommended freeboard': optimal_freeboard})

        ##########-----for summery analysis section ---------------##########
        ##----------------TOTAL----savings per month (flood insurance only)---------------------

            total_savings_permonth_insurance = []
            for i in range(len(totalBFE)):
                total_savings_permonth_insurance.append(monthly_premium_saving[i]-Amortized_FC[i])
            print("total_savings_permonth_insurance :",total_savings_permonth_insurance)
            total_savings_permonth_insurance_list_c.append(total_savings_permonth_insurance)

    ## lattitude and longitude ###
    print("\n")
    print("lattitude list : ", lattitude_c)
    print("longitude list : ", longitude_c)
    print("lattitude-longitude pair list : ", latlon_c)


    ## Total monthly premium saving ##
    print("\n")
    print("total_monthly_premium_saving_list_c : ", total_monthly_premium_saving_list_c)

  
    summation_total_monthly_premium_saving = []
    avg_total_monthly_premium_saving = []
    for z in range(len(monthly_premium_saving)):
        summation_total_monthly_premium_saving.append(0)
    #print("summationlist_total_monthly_premium_saving = " ,summation_total_monthly_premium_saving)

    for i in range(len(buildinglist)):   
        for z in range(len(monthly_premium_saving)):
            summation_total_monthly_premium_saving[z] = summation_total_monthly_premium_saving[z] + total_monthly_premium_saving_list_c[i][z]
    print("summationlist_total_monthly_premium_saving = " ,summation_total_monthly_premium_saving)
    summation_total_monthly_premium_saving_json = simplejson.dumps(summation_total_monthly_premium_saving[1:])   #**        

    for z in range(len(monthly_premium_saving)):
        avg_total_monthly_premium_saving.append(int(summation_total_monthly_premium_saving[z]/len(buildinglist)))
    print("avglist_total_monthly_premium_saving = " ,avg_total_monthly_premium_saving) 

    
    
    listofOptimalsIndividialBldg_monthly_premium_saving = []
    for each in range(len(total_optimal_freeboard_list_c)):
        listofOptimalsIndividialBldg_monthly_premium_saving.append(total_monthly_premium_saving_list_c[each][total_optimal_freeboard_list_c[each]])
        
    print("listofOptimalsIndividialBldg_monthly_premium_saving : ",listofOptimalsIndividialBldg_monthly_premium_saving)


    print("\n")
    
    
    ## Total monthly avoided loss ##
    print("\n")
    print("monthly_avoided_loss_list_c : ", monthly_avoided_loss_list_c)

  
    summation_monthly_avoided_loss = []
    avg_monthly_avoided_loss = []
    for z in range(len(monthly_avoided_loss)):
        summation_monthly_avoided_loss.append(0)
    #print("summationlist_monthly_avoided_loss = " ,summation_monthly_avoided_loss)

    for i in range(len(buildinglist)):   
        for z in range(len(monthly_avoided_loss)):
            summation_monthly_avoided_loss[z] = summation_monthly_avoided_loss[z] + monthly_avoided_loss_list_c[i][z]
    print("summationlist_monthly_avoided_loss = " ,summation_monthly_avoided_loss)
    summation_monthly_avoided_loss_json = simplejson.dumps(summation_monthly_avoided_loss[1:0])   #**        
    
    for z in range(len(monthly_avoided_loss)):
        avg_monthly_avoided_loss.append(int(summation_monthly_avoided_loss[z]/len(buildinglist)))
    print("avglist_monthly_avoided_loss = " ,avg_monthly_avoided_loss) 

    print("\n")

      
    ## Total Amortized_FC ##
    print("\n")
    print("Amortized_FC_list_c : ", Amortized_FC_list_c)

  
    summation_Amortized_FC = []
    avg_Amortized_FC = []
    for z in range(len(Amortized_FC)):
        summation_Amortized_FC.append(0)
    #print("summationlist_Amortized_FC = " ,summation_Amortized_FC)

    for i in range(len(buildinglist)):   
        for z in range(len(Amortized_FC)):
            summation_Amortized_FC[z] = summation_Amortized_FC[z] + (Amortized_FC_list_c[i][z])        ##negative added to show cost only
    print("summationlist_Amortized_FC = " ,summation_Amortized_FC)
    summation_Amortized_FC_json = simplejson.dumps(summation_Amortized_FC[1:])  #** 

    summation_Amortized_FC_neg = []
    for i in range(len(summation_Amortized_FC)):
           summation_Amortized_FC_neg.append(-1*summation_Amortized_FC[i])    
    print("summationlist_Amortized_FC neative = " ,summation_Amortized_FC_neg)
    summation_Amortized_FC_neg_json = simplejson.dumps(summation_Amortized_FC_neg[1:0])    #**        
    
    for z in range(len(Amortized_FC)):
        avg_Amortized_FC.append(int(summation_Amortized_FC[z]/len(buildinglist)))
    print("avglist_Amortized_FC = " ,avg_Amortized_FC) 

    print("\n")

    ## Total Freeboard Cost ##
    print("\n")
    print("freeboardCost_list_c : ", freeboardCost_list_c)

  
    summation_freeboardCost = []
    avg_freeboardCost = []
    for z in range(len(freeboardCost)):
        summation_freeboardCost.append(0)
    #print("summationlist_freeboardCost = " ,summation_freeboardCost)

    for i in range(len(buildinglist)):   
        for z in range(len(freeboardCost)):
            summation_freeboardCost[z] = summation_freeboardCost[z] + freeboardCost_list_c[i][z]
    print("summationlist_freeboardCost = " ,summation_freeboardCost)
    summation_freeboardCost_json = simplejson.dumps(summation_freeboardCost)        
    
    for z in range(len(freeboardCost)):
        avg_freeboardCost.append(int(summation_freeboardCost[z]/len(buildinglist)))
    print("avglist_freeboardCost = " ,avg_freeboardCost) 

    print("\n")

    ###
    ## community level for amortized freeboard cost

    ###
    
    ## Total Savings Permonth Insurance only ##
    print("\n")
    print("total_savings_permonth_insurance_list_c : ", total_savings_permonth_insurance_list_c)

  
    summation_total_savings_permonth_insurance = []
    avg_total_savings_permonth_insurance = []
    for z in range(len(total_savings_permonth_insurance)):
        summation_total_savings_permonth_insurance.append(0)
    #print("summationlist_total_savings_permonth_insurance = " ,summation_total_savings_permonth_insurance)

    for i in range(len(buildinglist)):   
        for z in range(len(total_savings_permonth_insurance)):
            summation_total_savings_permonth_insurance[z] = summation_total_savings_permonth_insurance[z] + total_savings_permonth_insurance_list_c[i][z]
    print("summationlist_total_savings_permonth_insurance = " ,summation_total_savings_permonth_insurance)
    summation_total_savings_permonth_insurance_json = simplejson.dumps(summation_total_savings_permonth_insurance)        
    
    for z in range(len(total_savings_permonth_insurance)):
        avg_total_savings_permonth_insurance.append(int(summation_total_savings_permonth_insurance[z]/len(buildinglist)))
    print("avglist_total_savings_permonth_insurance = " ,avg_total_savings_permonth_insurance) 

    print("\n")




   ####################********Community level analysis STARTS*********########################
    print("\n")
    ## Total monthly saving ##
    print("total_monthly_saving_list_c : ", total_monthly_saving_list_c)

  
    summation_total_monthly_saving = []
    avg_total_monthly_saving = []
    for z in range(len(total_monthly_saving)):
        summation_total_monthly_saving.append(0)
    #print("summationlist_total_monthly_saving = " ,summation_total_monthly_saving)

    for i in range(len(buildinglist)):   
        for z in range(len(total_monthly_saving)):
            summation_total_monthly_saving[z] = summation_total_monthly_saving[z] + total_monthly_saving_list_c[i][z]
    print("summationlist_total_monthly_saving = " ,summation_total_monthly_saving)
    summation_total_monthly_saving_json = simplejson.dumps(summation_total_monthly_saving[1:0]) #**        
    
    for z in range(len(total_monthly_saving)):
        avg_total_monthly_saving.append(int(summation_total_monthly_saving[z]/len(buildinglist)))
    print("avglist_total_monthly_saving = " ,avg_total_monthly_saving) 


    print("total_optimal_saving_list_c  : " , total_optimal_saving_list_c)
    print("total_optimal_freeboard_list_c : ", total_optimal_freeboard_list_c)

    optimal_saving = max(summation_total_monthly_saving)
    optimal_saving_json = simplejson.dumps(optimal_saving) 

    print("\n")
    
   ## Freeboard cost ##

    print("freeboardCost_list_c : ", freeboardCost_list_c)
    
    listofOptimalsIndividialBldg_freeboardcost = []
    for each in range(len(total_optimal_freeboard_list_c)):
        listofOptimalsIndividialBldg_freeboardcost.append(freeboardCost_list_c[each][total_optimal_freeboard_list_c[each]])
        
    print("listofOptimalsIndividialBldg_freeboardcost : ",listofOptimalsIndividialBldg_freeboardcost)
  
    summation_freeboardCost = []
    avg_freeboardCost = []
    for z in range(len(freeboardCost)):
        summation_freeboardCost.append(0)
    #print("summationlist_freeboardCost = " ,summation_freeboardCost)

    for i in range(len(buildinglist)):   
        for z in range(len(freeboardCost)):
            summation_freeboardCost[z] = summation_freeboardCost[z] + freeboardCost_list_c[i][z]
    print("summationlist_freeboardCost = " ,summation_freeboardCost)
    summation_freeboardCost_json = simplejson.dumps(summation_freeboardCost )

    
    for k in range(len(summation_total_monthly_saving)):
        if optimal_saving == summation_total_monthly_saving[k]:
            optimal_freeboard = totalBFE[k]
            aggregated_freeboard_cost = summation_freeboardCost[k]
    print("Aggregated_freeboard_cost = ", aggregated_freeboard_cost)        

    
    for z in range(len(freeboardCost)):
        avg_freeboardCost.append(int(summation_freeboardCost[z]/len(buildinglist)))
    print("avglist_freeboardCost = " ,avg_freeboardCost) 
    print("\n")

    
    ## Total annual premium ##
    print("total_annual_premium_list_c : ", total_annual_premium_list_c)
    print("total_monthly_premium_list_c : ", total_monthly_premium_list_c)

    summation_total_annual_premium = []
    avg_total_annual_premium = []
    for z in range(len(total_annual_premium)):
        summation_total_annual_premium.append(0)
    #print("summationlist_total_annual_premium = " ,summation_total_annual_premium)

    summation_total_monthly_premium = []
    avg_total_monthly_premium = []
    for z in range(len(total_monthly_premium)):
        summation_total_monthly_premium.append(0)
    #print("summationlist_total_monthly_premium = " ,summation_total_monthly_premium)

    for i in range(len(buildinglist)):   
        for z in range(len(total_annual_premium)):
            summation_total_annual_premium[z] = summation_total_annual_premium[z] + total_annual_premium_list_c[i][z]
    print("summationlist_total_annual_premium = " ,summation_total_annual_premium)        
    summation_total_annual_premium_json = simplejson.dumps(summation_total_annual_premium)

    for i in range(len(buildinglist)):   
        for z in range(len(total_monthly_premium)):
            summation_total_monthly_premium[z] = summation_total_monthly_premium[z] + total_monthly_premium_list_c[i][z]
    print("summationlist_total_monthly_premium = " ,summation_total_monthly_premium)        
    summation_total_monthly_premium_json = simplejson.dumps(summation_total_monthly_premium)

    for k in range(len(summation_total_monthly_saving)):
        if optimal_saving == summation_total_monthly_saving[k]:
            #optimal_freeboard = totalBFE[k]
            aggregated_total_annual_premium = summation_total_annual_premium[k]
    print("Aggregated_total_annual_premium = ", aggregated_total_annual_premium)  

    for k in range(len(summation_total_monthly_saving)):
        if optimal_saving == summation_total_monthly_saving[k]:
            #optimal_freeboard = totalBFE[k]
            aggregated_total_monthly_premium = summation_total_monthly_premium[k]
    print("Aggregated_total_monthly_premium = ", aggregated_total_monthly_premium)  


    for z in range(len(total_annual_premium)):
        avg_total_annual_premium.append(int(summation_total_annual_premium[z]/len(buildinglist)))
    print("avglist_total_annual_premium = " ,avg_total_annual_premium) 
    print("\n")

    for z in range(len(total_monthly_premium)):
        avg_total_monthly_premium.append(int(summation_total_monthly_premium[z]/len(buildinglist)))
    print("avglist_total_monthly_premium = " ,avg_total_monthly_premium) 
    print("\n")

    listofOptimalsIndividialBldg_annual_premium = []
    listofOptimalsIndividialBldg_monthly_premium = []
    for each in range(len(total_optimal_freeboard_list_c)):
        listofOptimalsIndividialBldg_annual_premium.append(total_annual_premium_list_c[each][total_optimal_freeboard_list_c[each]])
    print("listofOptimalsIndividialBldg_annual_premium : ",listofOptimalsIndividialBldg_annual_premium)
    
  
    listofOptimalsIndividialBldg_monthly_premium = []
    for each in range(len(total_optimal_freeboard_list_c)):
        listofOptimalsIndividialBldg_monthly_premium.append(total_monthly_premium_list_c[each][total_optimal_freeboard_list_c[each]])
        
    print("listofOptimalsIndividialBldg_monthly_premium : ",listofOptimalsIndividialBldg_monthly_premium)
   

    # ## Expected annual flood loss ##

    # print("AAL_absCurrency_list_c : ", AAL_absCurrency_list_c)

    # summation_AAL_absCurrency = []
    # avg_AAL_absCurrency = []
    # for z in range(len(AAL_absCurrency)):
    #     summation_AAL_absCurrency.append(0)
    # #print("summationlist_AAL_absCurrency = " ,summation_AAL_absCurrency)

    # for i in range(len(buildinglist)):   
    #     for z in range(len(AAL_absCurrency)):
    #         summation_AAL_absCurrency[z] = summation_AAL_absCurrency[z] + AAL_absCurrency_list_c[i][z]
    # print("summationlist_AAL_absCurrency = " ,summation_AAL_absCurrency)        
    # summation_AAL_absCurrency_json = simplejson.dumps(summation_AAL_absCurrency)

    # for k in range(len(summation_total_monthly_saving)):
    #     if optimal_saving == summation_total_monthly_saving[k]:
    #         #optimal_freeboard = totalBFE[k]
    #         aggregated_AAL_absCurrency = summation_AAL_absCurrency[k]
    # print("Aggregated AAL absCurrency = ", aggregated_AAL_absCurrency)  


    # for z in range(len(AAL_absCurrency)):
    #     avg_AAL_absCurrency.append(int(summation_AAL_absCurrency[z]/len(buildinglist)))
    # print("avglist_AAL_absCurrency = " ,avg_AAL_absCurrency) 
    # print("\n")

    # listofOptimalsIndividialBldg_AAL_absCurrency = []
    # for each in range(len(total_optimal_freeboard_list_c)):
    #     listofOptimalsIndividialBldg_AAL_absCurrency.append(AAL_absCurrency_list_c[each][total_optimal_freeboard_list_c[each]])
        
    # print("listofOptimalsIndividialBldg_AAL_absCurrency : ",listofOptimalsIndividialBldg_AAL_absCurrency)
    # print("\n")


    ##
    print("AAL_Total_list_c : ", AAL_Total_list_c)

    summation_AAL_Total = []
    avg_AAL_Total = []
    for z in range(len(AAL_Total_list)):
        summation_AAL_Total.append(0)
    #print("summationlist_AAL_Total = " ,summation_AAL_Total)

    for i in range(len(buildinglist)):   
        for z in range(len(AAL_Total_list)):
            summation_AAL_Total[z] = summation_AAL_Total[z] + AAL_Total_list_c[i][z]
    print("summation_AAL_Total = " ,summation_AAL_Total)        
    summation_AAL_Total_json = simplejson.dumps(summation_AAL_Total)

    for k in range(len(summation_total_monthly_saving)):
        if optimal_saving == summation_total_monthly_saving[k]:
            #optimal_freeboard = totalBFE[k]
            aggregated_AAL_Total = summation_AAL_Total[k]
    print("Aggregated AAL_Total = ", aggregated_AAL_Total)  


    for z in range(len(AAL_Total_list)):
        avg_AAL_Total.append(int(summation_AAL_Total[z]/len(buildinglist)))
    print("avglist_AAL_Total = " ,avg_AAL_Total) 
    print("\n")

    listofOptimalsIndividialBldg_AAL_Total = []
    for each in range(len(total_optimal_freeboard_list_c)):
        listofOptimalsIndividialBldg_AAL_Total.append(AAL_Total_list_c[each][total_optimal_freeboard_list_c[each]])
        
    print("listofOptimalsIndividialBldg_AAL_Total : ",listofOptimalsIndividialBldg_AAL_Total)
    print("\n")

  
## NEW AAL method- avoided monthly loss ##

    ## homeowner ##
    print("avoided_monthly_loss_homeowner : ", avoided_monthly_loss_homeowner) 
    print("avoided_monthly_loss_landlord : ", avoided_monthly_loss_landlord)   
    print("avoided_monthly_loss_tenant : ", avoided_monthly_loss_tenant)


    print("avoided_monthly_loss_homeowner_list_c : ", avoided_monthly_loss_homeowner_list_c)

    summation_avoided_monthly_loss_homeowner = []
    avg_avoided_monthly_loss_homeowner = []
    for z in range(len(avoided_monthly_loss_homeowner)):
        summation_avoided_monthly_loss_homeowner.append(0)
    #print("summationlist_avoided_monthly_loss_homeowner = " ,summation_avoided_monthly_loss_homeowner)

    for i in range(len(buildinglist)):   
        for z in range(len(avoided_monthly_loss_homeowner)):
            summation_avoided_monthly_loss_homeowner[z] = summation_avoided_monthly_loss_homeowner[z] + avoided_monthly_loss_homeowner_list_c[i][z]
    print("summationlist_avoided_monthly_loss_homeowner = " ,summation_avoided_monthly_loss_homeowner)        
    summation_avoided_monthly_loss_homeowner_json = simplejson.dumps(summation_avoided_monthly_loss_homeowner)

    for k in range(len(summation_total_monthly_saving)):
        if optimal_saving == summation_total_monthly_saving[k]:
            #optimal_freeboard = totalBFE[k]
            aggregated_avoided_monthly_loss_homeowner = summation_avoided_monthly_loss_homeowner[k]
    print("Aggregated avoided_monthly_loss_homeowner = ", aggregated_avoided_monthly_loss_homeowner)  


    for z in range(len(avoided_monthly_loss_homeowner)):
        avg_avoided_monthly_loss_homeowner.append(int(summation_avoided_monthly_loss_homeowner[z]/len(buildinglist)))
    print("avglist_avoided_monthly_loss_homeowner = " ,avg_avoided_monthly_loss_homeowner) 
    print("\n")

    listofOptimalsIndividialBldg_avoided_monthly_loss_homeowner = []
    for each in range(len(total_optimal_freeboard_list_c)):
        listofOptimalsIndividialBldg_avoided_monthly_loss_homeowner.append(avoided_monthly_loss_homeowner_list_c[each][total_optimal_freeboard_list_c[each]])
        
    print("listofOptimalsIndividialBldg_avoided_monthly_loss_homeowner : ",listofOptimalsIndividialBldg_avoided_monthly_loss_homeowner)
  

    ## landlord ##

    print("avoided_monthly_loss_landlord_list_c : ", avoided_monthly_loss_landlord_list_c)

    summation_avoided_monthly_loss_landlord = []
    avg_avoided_monthly_loss_landlord = []
    for z in range(len(avoided_monthly_loss_landlord)):
        summation_avoided_monthly_loss_landlord.append(0)
    #print("summationlist_avoided_monthly_loss_landlord = " ,summation_avoided_monthly_loss_landlord)

    for i in range(len(buildinglist)):   
        for z in range(len(avoided_monthly_loss_landlord)):
            summation_avoided_monthly_loss_landlord[z] = summation_avoided_monthly_loss_landlord[z] + avoided_monthly_loss_landlord_list_c[i][z]
    print("summationlist_avoided_monthly_loss_landlord = " ,summation_avoided_monthly_loss_landlord)        
    summation_avoided_monthly_loss_landlord_json = simplejson.dumps(summation_avoided_monthly_loss_landlord)

    for k in range(len(summation_total_monthly_saving)):
        if optimal_saving == summation_total_monthly_saving[k]:
            #optimal_freeboard = totalBFE[k]
            aggregated_avoided_monthly_loss_landlord = summation_avoided_monthly_loss_landlord[k]
    print("Aggregated avoided_monthly_loss_landlord = ", aggregated_avoided_monthly_loss_landlord)  


    for z in range(len(avoided_monthly_loss_landlord)):
        avg_avoided_monthly_loss_landlord.append(int(summation_avoided_monthly_loss_landlord[z]/len(buildinglist)))
    print("avglist_avoided_monthly_loss_landlord = " ,avg_avoided_monthly_loss_landlord) 
    print("\n")

    listofOptimalsIndividialBldg_avoided_monthly_loss_landlord = []
    for each in range(len(total_optimal_freeboard_list_c)):
        listofOptimalsIndividialBldg_avoided_monthly_loss_landlord.append(avoided_monthly_loss_landlord_list_c[each][total_optimal_freeboard_list_c[each]])
        
    print("listofOptimalsIndividialBldg_avoided_monthly_loss_landlord : ",listofOptimalsIndividialBldg_avoided_monthly_loss_landlord)
  

    ## tenant ##

    print("avoided_monthly_loss_tenant_list_c : ", avoided_monthly_loss_tenant_list_c)

    summation_avoided_monthly_loss_tenant = []
    avg_avoided_monthly_loss_tenant = []
    for z in range(len(avoided_monthly_loss_tenant)):
        summation_avoided_monthly_loss_tenant.append(0)
    #print("summationlist_avoided_monthly_loss_tenant = " ,summation_avoided_monthly_loss_tenant)

    for i in range(len(buildinglist)):   
        for z in range(len(avoided_monthly_loss_tenant)):
            summation_avoided_monthly_loss_tenant[z] = summation_avoided_monthly_loss_tenant[z] + avoided_monthly_loss_tenant_list_c[i][z]
    print("summationlist_avoided_monthly_loss_tenant = " ,summation_avoided_monthly_loss_tenant)        
    summation_avoided_monthly_loss_tenant_json = simplejson.dumps(summation_avoided_monthly_loss_tenant)

    for k in range(len(summation_total_monthly_saving)):
        if optimal_saving == summation_total_monthly_saving[k]:
            #optimal_freeboard = totalBFE[k]
            aggregated_avoided_monthly_loss_tenant = summation_avoided_monthly_loss_tenant[k]
    print("Aggregated avoided_monthly_loss_tenant = ", aggregated_avoided_monthly_loss_tenant)  


    for z in range(len(avoided_monthly_loss_tenant)):
        avg_avoided_monthly_loss_tenant.append(int(summation_avoided_monthly_loss_tenant[z]/len(buildinglist)))
    print("avglist_avoided_monthly_loss_tenant = " ,avg_avoided_monthly_loss_tenant) 
    print("\n")

    listofOptimalsIndividialBldg_avoided_monthly_loss_tenant = []
    for each in range(len(total_optimal_freeboard_list_c)):
        listofOptimalsIndividialBldg_avoided_monthly_loss_tenant.append(avoided_monthly_loss_tenant_list_c[each][total_optimal_freeboard_list_c[each]])
        
    print("listofOptimalsIndividialBldg_avoided_monthly_loss_tenant : ",listofOptimalsIndividialBldg_avoided_monthly_loss_tenant)
    
    
    
    if user_type == "Homeowner":
        listofOptimalsIndividialBldg_avoided_monthly_loss = listofOptimalsIndividialBldg_avoided_monthly_loss_homeowner
    elif user_type == "Tenant":
        listofOptimalsIndividialBldg_avoided_monthly_loss = listofOptimalsIndividialBldg_avoided_monthly_loss_tenant
    elif user_type == "Landlord":
        listofOptimalsIndividialBldg_avoided_monthly_loss = listofOptimalsIndividialBldg_avoided_monthly_loss_landlord
    # elif user_type == "Community official":
    #     listofOptimalsIndividialBldg_avoided_monthly_loss == listofOptimalsIndividialBldg_avoided_monthly_loss_CommunityOfficial
    else:
        print("None of the user type!")
        listofOptimalsIndividialBldg_avoided_monthly_loss = listofOptimalsIndividialBldg_avoided_monthly_loss_homeowner #"NONE"   #fix it later
        print("listofOptimalsIndividialBldg_avoided_monthly_loss = ", listofOptimalsIndividialBldg_avoided_monthly_loss)


## Time to recover the freeboard cost TB ##
    print("time_to_recover_FC_TB_list_c : ", time_to_recover_FC_TB_list_c)
 
    summation_time_to_recover_FC_TB = []
    avg_time_to_recover_FC_TB = []
    for z in range(len(time_to_recover_FC_TB)):
        summation_time_to_recover_FC_TB.append(0)
    #print("summationlist_time_to_recover_FC_TB = " ,summation_time_to_recover_FC_TB)

    for i in range(len(buildinglist)):   
        for z in range(len(time_to_recover_FC_TB)):
            summation_time_to_recover_FC_TB[z] = round(summation_time_to_recover_FC_TB[z] + time_to_recover_FC_TB_list_c[i][z],3)
    print("summationlist_time_to_recover_FC_TB = " ,summation_time_to_recover_FC_TB)
    summation_time_to_recover_FC_TB_json = simplejson.dumps(summation_time_to_recover_FC_TB)     

    for k in range(len(summation_total_monthly_saving)):
        if optimal_saving == summation_total_monthly_saving[k]:
            #optimal_freeboard = totalBFE[k]
            aggregated_time_to_recover_FC_TB = summation_time_to_recover_FC_TB[k]
    print("Aggregated time to recover FC TB = ", aggregated_time_to_recover_FC_TB)  
    
    for z in range(len(time_to_recover_FC_TB)):
        avg_time_to_recover_FC_TB.append(round(summation_time_to_recover_FC_TB[z]/len(buildinglist),3))
    print("avglist_time_to_recover_FC_TB = " ,avg_time_to_recover_FC_TB) 
    print("\n")
    
    listofOptimalsIndividialBldg_time_to_recover_FC_TB = []
    for each in range(len(total_optimal_freeboard_list_c)):
        listofOptimalsIndividialBldg_time_to_recover_FC_TB.append(time_to_recover_FC_TB_list_c[each][total_optimal_freeboard_list_c[each]])
        
    print("listofOptimalsIndividialBldg_time_to_recover_FC_TB : ",listofOptimalsIndividialBldg_time_to_recover_FC_TB)
  

    ## Time to recover the freeboard cost PS ##
    print("time_to_recover_FC_PS_list_c : ", time_to_recover_FC_PS_list_c)
 
    summation_time_to_recover_FC_PS = []
    avg_time_to_recover_FC_PS = []
    for z in range(len(time_to_recover_FC_PS)):
        summation_time_to_recover_FC_PS.append(0)
    #print("summationlist_time_to_recover_FC_PS = " ,summation_time_to_recover_FC_PS)

    for i in range(len(buildinglist)):   
        for z in range(len(time_to_recover_FC_PS)):
            summation_time_to_recover_FC_PS[z] = round(summation_time_to_recover_FC_PS[z] + time_to_recover_FC_PS_list_c[i][z],3)
    print("summationlist_time_to_recover_FC_PS = " ,summation_time_to_recover_FC_PS)
    summation_time_to_recover_FC_PS_json = simplejson.dumps(summation_time_to_recover_FC_PS)     

    for k in range(len(summation_total_monthly_saving)):
        if optimal_saving == summation_total_monthly_saving[k]:
            #optimal_freeboard = totalBFE[k]
            aggregated_time_to_recover_FC_PS = summation_time_to_recover_FC_PS[k]
    print("Aggregated time to recover FC PS = ", aggregated_time_to_recover_FC_PS)  
  
    
    for z in range(len(time_to_recover_FC_PS)):
        avg_time_to_recover_FC_PS.append(round(summation_time_to_recover_FC_PS[z]/len(buildinglist),3))
    print("avglist_time_to_recover_FC_PS = " ,avg_time_to_recover_FC_PS) 
    print("\n")

    ####################********Community level analysis ENDS*********########################

    #Json---------------------------------------
    time_to_recover_FC_TB_json = summation_time_to_recover_FC_TB_json
    time_to_recover_FC_PS_json = summation_time_to_recover_FC_PS_json
    Amortized_FC_json = summation_Amortized_FC_json
    Amortized_FC_neg_json = summation_Amortized_FC_neg_json
    freeboardCost_json = summation_freeboardCost_json
    total_annual_premium_json = summation_total_annual_premium_json
    total_monthly_premium_json = summation_total_monthly_premium_json
    total_monthly_saving_json = summation_total_monthly_saving_json
    #AAL_absCurrency_json = summation_AAL_absCurrency_json
    AAL_Total_json = summation_AAL_Total_json

    location_json_list = simplejson.dumps(location)    




    ## read the .csv file using Pandas
    #results_data = pd.read_csv(r'C:\inetpub\wwwroot\rootProject\output\results.csv')             ##**********server copy
    results_data = pd.read_csv('output/results.csv')                                              ##**********local copy

    results_data["Aggregated recommended freeboard"] = optimal_freeboard
    results_data["Aggregated total optimal monthly saving"] = optimal_saving
    results_data["Aggregated total freeboard cost"] = aggregated_freeboard_cost
    #results_data["Aggregated total amortised freeboard cost"] = aggregated_freeboard_cost   #fix it
    results_data["Aggregated total annual premium"] = aggregated_total_annual_premium
    results_data["Aggregated total monthly premium"] = aggregated_total_monthly_premium
    #results_data["Aggregated AAL absCurrency"] = aggregated_AAL_absCurrency
    results_data["Aggregated AAL Total"] = aggregated_AAL_Total
    results_data["Aggregated time to recover FC (total benefit)"] = aggregated_time_to_recover_FC_TB
    results_data["Aggregated time to recover FC PS"] = aggregated_time_to_recover_FC_PS

    #results_data.to_csv(r"C:\inetpub\wwwroot\rootProject\output\results.csv", index=False)            ##*********server copy
    results_data.to_csv("output/results.csv", index=False)                                            ##*********local copy
    print(results_data.head(3))

    ## creating GeoPandas GeoDataFrame using the Pandas dataframe
    results_gdf = gpd.GeoDataFrame(results_data, geometry = gpd.points_from_xy(results_data['Longitude'],results_data['Lattitude']))
    print("results gdf :")
    print( results_gdf)

    ## obtain ESRI WKT
    ESRI_WKT = 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]]'
 
    ## save the file as an ESRI Shaefile
    #results_gdf.to_file(filename = r'C:\inetpub\wwwroot\rootProject\results_shp', driver = 'ESRI Shapefile', crs='EPSG:4326')             ##*********server copy
    results_gdf.to_file(filename = 'results_shp', driver = 'ESRI Shapefile', crs='EPSG:4326')                                            ##*********local copy

   
    ## Individual report ###
    #listforindividual = zip(buildinglist, zonelist, total_optimal_freeboard_list_c, total_optimal_saving_list_c, listofOptimalsIndividialBldg_freeboardcost, listofOptimalsIndividialBldg_annual_premium, listofOptimalsIndividialBldg_AAL_absCurrency, listofOptimalsIndividialBldg_time_to_recover_FC_TB)
    listforindividual = zip(buildinglist, zonelist, total_optimal_freeboard_list_c, total_optimal_saving_list_c, listofOptimalsIndividialBldg_freeboardcost, listofOptimalsIndividialBldg_monthly_premium_saving, listofOptimalsIndividialBldg_avoided_monthly_loss, listofOptimalsIndividialBldg_time_to_recover_FC_TB)


    ###    for calculation with below BFEs       ######
    # data_dictionary = {"location": location_json_list, "BuildingCoverage": coverage_lvl_bldg, "ContentCoverage": coverage_lvl_cont, "BuildingDeductibe" : deductible_bldg ,"ContentDeductible" :deductible_cont , "time_to_recover_FC_PS_json":time_to_recover_FC_PS_json, "time_to_recover_FC_TB_json":time_to_recover_FC_TB_json, "time_to_recover_FC_PS1": time_to_recover_FC_PS[1], "time_to_recover_FC_PS2": time_to_recover_FC_PS[2],"time_to_recover_FC_PS3": time_to_recover_FC_PS[3],"time_to_recover_FC_PS4": time_to_recover_FC_PS[4], "time_to_recover_FC_TB1": time_to_recover_FC_TB[1], "time_to_recover_FC_TB2": time_to_recover_FC_TB[2], "time_to_recover_FC_TB3": time_to_recover_FC_TB[3], "time_to_recover_FC_TB4": time_to_recover_FC_TB[4], "summation_time_to_recover_FC_PSlow":min(summation_time_to_recover_FC_PS), "summation_time_to_recover_FC_PShigh": max(summation_time_to_recover_FC_PS),"summation_time_to_recover_FC_TBlow":min(summation_time_to_recover_FC_TB),"summation_time_to_recover_FC_TBhigh":max(summation_time_to_recover_FC_TB), "optimal_total_annual_premium_freeboard":optimal_total_annual_premium_freeboard, "optimal_total_annual_premium":optimal_total_annual_premium, "total_annual_premium_json":total_annual_premium_json,"total_annual_premium0": total_annual_premium[0],"total_annual_premium1": total_annual_premium[1],"total_annual_premium2": total_annual_premium[2],"total_annual_premium3": total_annual_premium[3],"total_annual_premium4": total_annual_premium[4], "summation_total_annual_premiumlow": min(summation_total_annual_premium), "summation_total_annual_premiumhigh":max(summation_total_annual_premium),"total_savings_permonth_insurance0" :total_savings_permonth_insurance[0],"total_savings_permonth_insurance1" :total_savings_permonth_insurance[1],"total_savings_permonth_insurance2" :total_savings_permonth_insurance[2],"total_savings_permonth_insurance3" :total_savings_permonth_insurance[3],"total_savings_permonth_insurance4" :total_savings_permonth_insurance[4],"optimal_freeboardCost": optimal_freeboardCost,"optimal_freeboard_freeboardCost":optimal_freeboard_freeboardCost,"optimal_freeboardCost_json":optimal_freeboardCost_json, "summation_freeboardCostlow":min(summation_freeboardCost), "summation_freeboardCosthigh":max(summation_freeboardCost), "optimal_AAL_absCurrency_freeboard":optimal_AAL_absCurrency_freeboard, "optimal_AAL_absCurrency": optimal_AAL_absCurrency, "AAL_absCurrency0":AAL_absCurrency[0],"AAL_absCurrency1":AAL_absCurrency[1],"AAL_absCurrency2":AAL_absCurrency[2],"AAL_absCurrency3":AAL_absCurrency[3],"AAL_absCurrency4":AAL_absCurrency[4],"AAL_absCurrency_json":AAL_absCurrency_json, "summation_AAL_absCurrencylow" :min(summation_AAL_absCurrency), "summation_AAL_absCurrencyhigh":max(summation_AAL_absCurrency), "monthly_premium_saving_json":monthly_premium_saving_json,"monthly_premium_saving0": monthly_premium_saving[0],"monthly_premium_saving1": monthly_premium_saving[1],"monthly_premium_saving2": monthly_premium_saving[2],"monthly_premium_saving3": monthly_premium_saving[3],"monthly_premium_saving4": monthly_premium_saving[4], "summation_total_monthly_premium_saving0":summation_total_monthly_premium_saving[0],"summation_total_monthly_premium_saving1":summation_total_monthly_premium_saving[1],"summation_total_monthly_premium_saving2":summation_total_monthly_premium_saving[2],"summation_total_monthly_premium_saving3":summation_total_monthly_premium_saving[3],"summation_total_monthly_premium_saving4":summation_total_monthly_premium_saving[4],"summation_total_monthly_premium_saving5":summation_total_monthly_premium_saving[5],"summation_total_monthly_premium_saving6":summation_total_monthly_premium_saving[6],"summation_total_monthly_premium_saving7":summation_total_monthly_premium_saving[7],"summation_total_monthly_premium_saving8":summation_total_monthly_premium_saving[8], "summation_monthly_avoided_loss0":summation_monthly_avoided_loss[0], "summation_monthly_avoided_loss1":summation_monthly_avoided_loss[1],"summation_monthly_avoided_loss2":summation_monthly_avoided_loss[2],"summation_monthly_avoided_loss3":summation_monthly_avoided_loss[3],"summation_monthly_avoided_loss4":summation_monthly_avoided_loss[4],"summation_monthly_avoided_loss5":summation_monthly_avoided_loss[5],"summation_monthly_avoided_loss6":summation_monthly_avoided_loss[6],"summation_monthly_avoided_loss7":summation_monthly_avoided_loss[7],"summation_monthly_avoided_loss8":summation_monthly_avoided_loss[8], "summation_freeboardCost0" :summation_freeboardCost[0],"summation_freeboardCost1" :summation_freeboardCost[1],"summation_freeboardCost2" :summation_freeboardCost[2],"summation_freeboardCost3" :summation_freeboardCost[3],"summation_freeboardCost4" :summation_freeboardCost[4],"summation_freeboardCost5" :summation_freeboardCost[5],"summation_freeboardCost6" :summation_freeboardCost[6],"summation_freeboardCost7" :summation_freeboardCost[7],"summation_freeboardCost8" :summation_freeboardCost[8], "Actual_construction_cost": Actual_construction_cost, "Amortized_FC_json" : Amortized_FC_json, "Amortized_FC0": Amortized_FC[0], "Amortized_FC1": Amortized_FC[1], "Amortized_FC2": Amortized_FC[2], "Amortized_FC3": Amortized_FC[3], "Amortized_FC4": Amortized_FC[4],"summation_Amortized_FC0": summation_Amortized_FC[0],"summation_Amortized_FC1": summation_Amortized_FC[1],"summation_Amortized_FC2": summation_Amortized_FC[2],"summation_Amortized_FC3": summation_Amortized_FC[3],"summation_Amortized_FC4": summation_Amortized_FC[4],"summation_Amortized_FC5": summation_Amortized_FC[5],"summation_Amortized_FC6": summation_Amortized_FC[6],"summation_Amortized_FC7": summation_Amortized_FC[7],"summation_Amortized_FC8": summation_Amortized_FC[8], "summation_total_savings_permonth_insurance0":summation_total_savings_permonth_insurance[0], "summation_total_savings_permonth_insurance1":summation_total_savings_permonth_insurance[1], "summation_total_savings_permonth_insurance2":summation_total_savings_permonth_insurance[2], "summation_total_savings_permonth_insurance3":summation_total_savings_permonth_insurance[3], "summation_total_savings_permonth_insurance4":summation_total_savings_permonth_insurance[4], "summation_total_savings_permonth_insurance5":summation_total_savings_permonth_insurance[5], "summation_total_savings_permonth_insurance6":summation_total_savings_permonth_insurance[6], "summation_total_savings_permonth_insurance7":summation_total_savings_permonth_insurance[7], "summation_total_savings_permonth_insurance8":summation_total_savings_permonth_insurance[8], "summation_total_monthly_saving0":summation_total_monthly_saving[0],  "summation_total_monthly_saving1":summation_total_monthly_saving[1], "summation_total_monthly_saving2":summation_total_monthly_saving[2], "summation_total_monthly_saving3":summation_total_monthly_saving[3], "summation_total_monthly_saving4":summation_total_monthly_saving[4], "summation_total_monthly_saving5":summation_total_monthly_saving[5], "summation_total_monthly_saving6":summation_total_monthly_saving[6], "summation_total_monthly_saving7":summation_total_monthly_saving[7], "summation_total_monthly_saving8":summation_total_monthly_saving[8], "floodzone": zonevalue, "optimal_saving_json":optimal_saving_json, "freeboardCost_json": freeboardCost_json, "monthly_avoided_loss_json": monthly_avoided_loss_json, "annual_avoided_loss_json": annual_avoided_loss_json, "total_annual_premium": total_annual_premium, "total_monthly_saving_json":total_monthly_saving_json, "summation_total_monthly_saving_low": min(summation_total_monthly_saving), "Optimalsavingsumm": optimal_saving, "time_to_recover_FC_MS": time_to_recover_FC_MS, "time_to_recover_FC_PS_json": time_to_recover_FC_PS_json, "SquareFootage":int(Square_footage), "No_Floors": No_Floors, "OptimalSaving" : optimal_saving, "OptimalFreeboard" : optimal_freeboard, "FreeboardCost0": freeboardCost[0], "FreeboardCost1": freeboardCost[1], "FreeboardCost2": freeboardCost[2], "FreeboardCost3": freeboardCost[3], "FreeboardCost4": freeboardCost[4], "total_monthly_saving0" : total_monthly_saving[0],"total_monthly_saving1" : total_monthly_saving[1],"total_monthly_saving2" : total_monthly_saving[2],"total_monthly_saving3" : total_monthly_saving[3],"total_monthly_savinglast" : total_monthly_saving[8], "AAL_absCurrency0": AAL_absCurrency[0],"AAL_absCurrency1": AAL_absCurrency[1],"AAL_absCurrency2": AAL_absCurrency[2],"AAL_absCurrency3": AAL_absCurrency[3],"AAL_absCurrency4": AAL_absCurrency[4], "total_annual_premium_BFE": total_annual_premium[0], "total_annual_premium_BFE1": total_annual_premium[1], "total_annual_premium_BFE2": total_annual_premium[2], "total_annual_premium_BFE3": total_annual_premium[3], "total_annual_premium_BFE4": total_annual_premium[4], "monthly_avoided_loss0": monthly_avoided_loss[0], "monthly_avoided_loss1": monthly_avoided_loss[1],"monthly_avoided_loss2": monthly_avoided_loss[2],"monthly_avoided_loss3": monthly_avoided_loss[3],"monthly_avoided_loss4": monthly_avoided_loss[4],"time_to_recover_FC_MS0" : time_to_recover_FC_MS[0], "time_to_recover_FC_MS1" : time_to_recover_FC_MS[1],"time_to_recover_FC_MS2" : time_to_recover_FC_MS[2],"time_to_recover_FC_MS3" : time_to_recover_FC_MS[3],"time_to_recover_FC_MS4" : time_to_recover_FC_MS[4], "netbenefit0" : netbenefit[0],"netbenefit1" : netbenefit[1],"netbenefit2" : netbenefit[2],"netbenefit3" : netbenefit[3], "netbenefit4" : netbenefit[4], 'script_insurance': script_insurance, 'div_insurance':div_insurance,  "annual_avoided_loss0": annual_avoided_loss[0], "annual_avoided_loss1": annual_avoided_loss[1],"annual_avoided_loss2":annual_avoided_loss[2],"annual_avoided_loss3": annual_avoided_loss[3],"annual_avoided_loss4": annual_avoided_loss[4] }
    
    print("avoided_monthly_loss_homeowner : ", avoided_monthly_loss_homeowner) 
    print("avoided_monthly_loss_landlord : ", avoided_monthly_loss_landlord)   
    print("avoided_monthly_loss_tenant : ", avoided_monthly_loss_tenant)

    #####   for calculation without below BFEs        ######
    data_dictionary = {"location": location_json_list,"user_type":user_type, "building_type": building_type, "assessment_type":assessment_type, "buildinglocation_type":buildinglocation_type, "CRS": CRS, "CRSpercent":CRSpercent, "listindividual": listforindividual, "buildinglocation": buildinglist, \
        "latlon_pair_list" :latlon_c , "latlon_pair_list_oneaddress" :latlon_c[0]  ,"lattitude_list" : lattitude_c[0], "longitude_list" : longitude_c[0],\
        "BuildingCoverage": coverage_lvl_bldg, "ContentCoverage": coverage_lvl_cont, "BuildingDeductibe" : deductible_bldg ,"ContentDeductible" :deductible_cont , \
        "time_to_recover_FC_TB1": time_to_recover_FC_TB[1], "time_to_recover_FC_TB2": time_to_recover_FC_TB[2], "time_to_recover_FC_TB3": time_to_recover_FC_TB[3], "time_to_recover_FC_TB4": time_to_recover_FC_TB[4], \
        "summation_time_to_recover_FC_PSlow":min(summation_time_to_recover_FC_PS), "summation_time_to_recover_FC_PShigh": max(summation_time_to_recover_FC_PS),\
        "summation_time_to_recover_FC_TBlow":min(summation_time_to_recover_FC_TB),"summation_time_to_recover_FC_TBhigh":max(summation_time_to_recover_FC_TB),\
        "optimal_total_monthly_premium_freeboard":optimal_total_monthly_premium_freeboard, "optimal_total_monthly_premium":optimal_total_monthly_premium,"total_monthly_premium_json":total_monthly_premium_json, "total_annual_premium_json":total_annual_premium_json,\
        "total_monthly_premium0": total_monthly_premium[0],\
        "total_monthly_premium1": total_monthly_premium[1],"total_monthly_premium2": total_monthly_premium[2],"total_monthly_premium3": total_monthly_premium[3],"total_monthly_premium4": total_monthly_premium[4], "summation_total_monthly_premiumlow": min(summation_total_monthly_premium),"summation_total_monthly_premiumhigh":max(summation_total_monthly_premium),\
        "summation_total_annual_premiumlow": min(summation_total_annual_premium),"summation_total_annual_premiumhigh":max(summation_total_annual_premium),\
        "total_savings_permonth_insurance0" :total_savings_permonth_insurance[0], \
        "total_savings_permonth_insurance1" :total_savings_permonth_insurance[1],"total_savings_permonth_insurance2" :total_savings_permonth_insurance[2], "total_savings_permonth_insurance3" :total_savings_permonth_insurance[3],"total_savings_permonth_insurance4" :total_savings_permonth_insurance[4],\
        "optimal_freeboardCost": optimal_freeboardCost,"optimal_freeboard_freeboardCost":optimal_freeboard_freeboardCost,"optimal_freeboardCost_json":optimal_freeboardCost_json, "summation_freeboardCostlow":min(summation_freeboardCost), "summation_freeboardCosthigh":max(summation_freeboardCost),\
        "summation_am_freeboardCostlow":min(summation_Amortized_FC[1:]), "summation_am_freeboardCosthigh":max(summation_Amortized_FC[1:]), \
        "monthly_premium_saving_json":monthly_premium_saving_json,"monthly_premium_saving0": monthly_premium_saving[0],"monthly_premium_saving1": monthly_premium_saving[1],"monthly_premium_saving2": monthly_premium_saving[2],"monthly_premium_saving3": monthly_premium_saving[3],"monthly_premium_saving4": monthly_premium_saving[4], \
        "summation_total_monthly_premium_saving0":summation_total_monthly_premium_saving[0],\
        "summation_total_monthly_premium_saving1":summation_total_monthly_premium_saving[1],"summation_total_monthly_premium_saving2":summation_total_monthly_premium_saving[2], "summation_total_monthly_premium_saving3":summation_total_monthly_premium_saving[3],"summation_total_monthly_premium_saving4":summation_total_monthly_premium_saving[4], "summation_total_monthly_premium_savingHigh": max(summation_total_monthly_premium_saving[1:]), "summation_total_monthly_premium_savingLow": min(summation_total_monthly_premium_saving[1:]),\
        "summation_monthly_avoided_loss0":summation_monthly_avoided_loss[0], \
        "summation_monthly_avoided_loss1":summation_monthly_avoided_loss[1],"summation_monthly_avoided_loss2":summation_monthly_avoided_loss[2],"summation_monthly_avoided_loss3":summation_monthly_avoided_loss[3],"summation_monthly_avoided_loss4":summation_monthly_avoided_loss[4],\
        "summation_freeboardCost0" :summation_freeboardCost[0],\
        "summation_freeboardCost1" :summation_freeboardCost[1],"summation_freeboardCost2" :summation_freeboardCost[2],"summation_freeboardCost3" :summation_freeboardCost[3],"summation_freeboardCost4" :summation_freeboardCost[4],\
        "Actual_construction_cost": Actual_construction_cost,\
        "Amortized_FC_json" : Amortized_FC_json, "Amortized_FC_neg_json":Amortized_FC_neg_json, "Amortized_FC0":Amortized_FC[0], "Amortized_FC1": Amortized_FC[1], "Amortized_FC2": Amortized_FC[2], "Amortized_FC3": Amortized_FC[3], "Amortized_FC4": Amortized_FC[4],\
        "summation_Amortized_FC0":  summation_Amortized_FC[0],\
        "summation_Amortized_FC1":  summation_Amortized_FC[1],"summation_Amortized_FC2":  summation_Amortized_FC[2],"summation_Amortized_FC3":  summation_Amortized_FC[3],"summation_Amortized_FC4":  summation_Amortized_FC[4], \
        "summation_total_savings_permonth_insurance0":summation_total_savings_permonth_insurance[0],\
        "summation_total_savings_permonth_insurance1":summation_total_savings_permonth_insurance[1], "summation_total_savings_permonth_insurance2":summation_total_savings_permonth_insurance[2], "summation_total_savings_permonth_insurance3":summation_total_savings_permonth_insurance[3],"summation_total_savings_permonth_insurance4":summation_total_savings_permonth_insurance[4],\
        "summation_total_monthly_saving0":summation_total_monthly_saving[0],\
        "summation_total_monthly_saving1":summation_total_monthly_saving[1], "summation_total_monthly_saving2":summation_total_monthly_saving[2],"summation_total_monthly_saving3":summation_total_monthly_saving[3], "summation_total_monthly_saving4":summation_total_monthly_saving[4],\
        "floodzone": zonevalue, "optimal_saving_json":optimal_saving_json, "freeboardCost_json": freeboardCost_json,"monthly_avoided_loss_json": monthly_avoided_loss_json, "annual_avoided_loss_json": annual_avoided_loss_json,\
        "total_monthly_premium": total_monthly_premium,"total_annual_premium": total_annual_premium, "total_monthly_saving_json":total_monthly_saving_json, "summation_total_monthly_saving_low": min(summation_total_monthly_saving[1:]),\
        "Optimalsavingsumm": optimal_saving, "time_to_recover_FC_MS": time_to_recover_FC_MS, "time_to_recover_FC_PS_json": time_to_recover_FC_PS_json, \
        "SquareFootage":int(Square_footage), "No_Floors": No_Floors, "OptimalSaving" : optimal_saving, "OptimalFreeboard" : optimal_freeboard,\
        "FreeboardCost0": freeboardCost[0],\
         "FreeboardCost1": freeboardCost[1], "FreeboardCost2": freeboardCost[2], "FreeboardCost3": freeboardCost[3], "FreeboardCost4": freeboardCost[4],\
        "total_monthly_saving0" : total_monthly_saving[0],\
        "total_monthly_saving1" : total_monthly_saving[1],"total_monthly_saving2" : total_monthly_saving[2],"total_monthly_saving3" : total_monthly_saving[3],"total_monthly_savinglast" : total_monthly_saving[4], \
        "total_monthly_premium_BFE": total_monthly_premium[0],\
         "total_monthly_premium_BFE1": total_monthly_premium[1], "total_monthly_premium_BFE2": total_monthly_premium[2],"total_monthly_premium_BFE3": total_monthly_premium[3], "total_monthly_premium_BFE4": total_monthly_premium[4],\
        "monthly_avoided_loss0": monthly_avoided_loss[0],\
        "monthly_avoided_loss1": monthly_avoided_loss[1],"monthly_avoided_loss2": monthly_avoided_loss[2],"monthly_avoided_loss3": monthly_avoided_loss[3],"monthly_avoided_loss4": monthly_avoided_loss[4], "summation_monthly_avoided_lossHigh": max(summation_monthly_avoided_loss[1:]), "summation_monthly_avoided_lossLow": min(summation_monthly_avoided_loss[1:]),\
        "time_to_recover_FC_MS0" : time_to_recover_FC_MS[0],\
         "time_to_recover_FC_MS1" : time_to_recover_FC_MS[1],"time_to_recover_FC_MS2" : time_to_recover_FC_MS[2],"time_to_recover_FC_MS3" : time_to_recover_FC_MS[3],"time_to_recover_FC_MS4" : time_to_recover_FC_MS[4],\
        "annual_avoided_loss0": annual_avoided_loss[0], \
        "annual_avoided_loss1": annual_avoided_loss[1],"annual_avoided_loss2":annual_avoided_loss[2],"annual_avoided_loss3": annual_avoided_loss[3],"annual_avoided_loss4": annual_avoided_loss[4],\
        "optimal_AAL_Total_list_freeboard":optimal_AAL_Total_list_freeboard, "optimal_AAL_Total_list": optimal_AAL_Total_list, 
        "AAL_Total_list0":AAL_Total_list[0],\
        "AAL_Total_list1":AAL_Total_list[1],"AAL_Total_list2":AAL_Total_list[2],"AAL_Total_list3":AAL_Total_list[3],"AAL_Total_list4":AAL_Total_list[4],\
        "AAL_Total_json":AAL_Total_json, "summation_AAL_Totallow" :min(summation_AAL_Total), "summation_AAL_Totalhigh":max(summation_AAL_Total),\
                "time_to_recover_FC_PS_json":time_to_recover_FC_PS_json, "time_to_recover_FC_TB_json":time_to_recover_FC_TB_json, "time_to_recover_FC_PS1": time_to_recover_FC_PS[1], "time_to_recover_FC_PS2": time_to_recover_FC_PS[2],"time_to_recover_FC_PS3": time_to_recover_FC_PS[3],"time_to_recover_FC_PS4": time_to_recover_FC_PS[4] }       
    # "optimal_AAL_absCurrency_freeboard":optimal_AAL_absCurrency_freeboard, "optimal_AAL_absCurrency": optimal_AAL_absCurrency, "AAL_absCurrency0":AAL_absCurrency[0],"AAL_absCurrency1":AAL_absCurrency[1],"AAL_absCurrency2":AAL_absCurrency[2],"AAL_absCurrency3":AAL_absCurrency[3],"AAL_absCurrency4":AAL_absCurrency[4],\
    # "AAL_absCurrency_json":AAL_absCurrency_json, "summation_AAL_absCurrencylow" :min(summation_AAL_absCurrency), "summation_AAL_absCurrencyhigh":max(summation_AAL_absCurrency),"AAL_absCurrency0": AAL_absCurrency[0],"AAL_absCurrency1": AAL_absCurrency[1],"AAL_absCurrency2": AAL_absCurrency[2],"AAL_absCurrency3": AAL_absCurrency[3],"AAL_absCurrency4": AAL_absCurrency[4],\
    #  "netbenefit0" : netbenefit[0],"netbenefit1" : netbenefit[1],"netbenefit2" : netbenefit[2],"netbenefit3" : netbenefit[3], "netbenefit4" : netbenefit[4], 
 

    search.datadict = data_dictionary

    return render(request, 'nodisc.html', data_dictionary)


def report(request):
    data = search.datadict
    report.data = data


    return render(request, 'report.html', data)


def exportpdf(request):

     ### pdf making ######
    template = get_template('report.html')
    data = report.data
    html = template.render(data)
    report.pdf = render_to_pdf('report.html', data)
    print("what is going on?  ", type(report.pdf))

    # print("what is going on inside this file?  ", type(report.pdf))
    if report.pdf:
        response = HttpResponse(report.pdf, content_type='application/pdf')
        response['Content-disposition']='attachment;filename=FloodsafehomeAnalysis'+'.pdf'
        return response
    #pass

   

def exportfile(request):
    response= HttpResponse(content_type='text/csv')
    response['Content-disposition']='attachment;filename=FloodSafeHomeResults'+'.csv'

    # opening the CSV file 
    #with open(r'C:\inetpub\wwwroot\rootProject\output\results.csv', mode ='r')as file:     ##**********server copy
    with open('output/results.csv', mode ='r')as file:                                      ##**********local copy
        # reading the CSV file 
        csvFile = csv.reader(file) 
        # creating a csv writer object 
        csvwriter = csv.writer(response) 
        # displaying the contents of the CSV file 
        for lines in csvFile: 
            print(lines) 
            csvwriter.writerow(lines)
            
 
    return response

def exportshp(request):
    response= HttpResponse(content_type='application/zip')
    response['Content-disposition']='attachment;filename=FloodsafehomeResults_shp'+'.zip'

    # path to folder which needs to be zipped
    directory = r'rootProject\results_shp'  # './results_shp'  ##**********server copy
    #directory = './results_shp'                                 ##**********local copy
    # initializing empty file paths list
    file_paths = []

    # crawling through directory and subdirectories
    for root, directories, files in os.walk(directory):
        for filename in files:
            # join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)

    # printing the list of all files to be zipped
    print('Following files will be zipped in this program:')
    for file_name in file_paths:
        print(file_name)

    # writing files to a zipfile
    with ZipFile(response,'w') as zip:
        # writing each file one by one
        for file in file_paths:
            zip.write(file)
    print('All files zipped successfully!')
    
    return response    



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

