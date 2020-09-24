from django.shortcuts import render, HttpResponse
from rootApp.models import Contact, FreeboardConstructionCost
from datetime import datetime
from django.contrib import messages
from django.db.models import Q

# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def freeboardproject(request):
    return render(request, 'research.html')    

def decisionmakingmap(request):
    return render(request, 'decisionmakingmap.html')      

def survey(request):
    return render(request, 'survey.html')  

def dosurvey(request):
    return render(request, 'dosurvey.html')      

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

    location = request.GET.get('location', 'sdjflkaksjflk')
    locationList=location.split(',')
    locationList = list(map(str.strip, locationList))
    addressvalue = FreeboardConstructionCost.objects.filter(
         Q(address__icontains=locationList[0]) ,  Q(street__icontains=locationList[1])).all()
    data_dict = {"my_data" : addressvalue , "vegetable" : ['alu', 'potol']}
    return render(request, 'search_results.html', data_dict)