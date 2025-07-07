'''from .bus import *
from .train import *
from .flight import *
from .booking import *
from .passenger import *
from .user import *
 
'''
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')
