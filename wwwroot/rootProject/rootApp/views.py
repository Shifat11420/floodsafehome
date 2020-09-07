from django.shortcuts import render, HttpResponse
from rootApp.models import Contact
from datetime import datetime
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def freeboardproject(request):
    return render(request, 'research.html')    

def decisionmakingmap(request):
    return render(request, 'index.html')      

def survey(request):
    return render(request, 'survey.html')  

def helpcenter(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        desc = request.POST.get('desc')
        contact = Contact(name=name, email=email, desc=desc, date=datetime.today()) 
        contact.save()
        messages.success(request, 'Your message has been sent!')

    return render(request, 'contact.html')    

