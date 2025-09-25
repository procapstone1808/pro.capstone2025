from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    context = {}
    return render(request, 'index.html', context)

def login_view(request):
    context = {}
    return render(request, 'login.html', context)
#def aplicacion (request):
    #return HttpResponse("")