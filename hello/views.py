from django.shortcuts import render
from django.http import HttpResponse
import requests
import os

from .models import Greeting

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')

    #レーティンググラフ
    #return render(request, "ratinggraph.html")

    #ティーポット
    #r = requests.get('http://httpbin.org/status/418')
    #print(r.text)
    #return HttpResponse('<pre>' + r.text + '</pre>')

    #
    return render(request,"form.html")

def vote(request):
    tmp = request.POST["username"]

    return HttpResponse('<pre>' + tmp + '</pre>')


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
