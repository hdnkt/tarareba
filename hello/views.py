from django.shortcuts import render
from django.http import HttpResponse
import requests
import os
import json
from bs4 import BeautifulSoup
from .models import Greeting
from .skr import getdatas,maximizeRate,makeoutputDic,manycontest,getdatasa


# Create your views here.
def index(request):
    return vote(request)

def result(request,username):
    r = ""
    name = username
    sex = "male"
    return last(request,name,sex,r)

def resultr(request,username):
    r = "r"
    name = username
    sex = "female"
    return last(request,name,sex,r)

def vote(request):
    name = "hdnkt"
    sex = "male"
    try:
        name = request.POST["username"]
        sex = request.POST["sex"]
    except:
        name = "hdnkt"
        sex = "male"
    return last(request,name,sex,"")

def last(request,name,sex,r):
    error = " "

    try:
        if sex =="female":
            r = "r"
            dic=manycontest()
            tmp,ratedHis = getdatas(name,dic)
            real = tmp[len(tmp)-1]["NewRating"]
            ans,ind=maximizeRate(tmp,ratedHis)
            final = makeoutputDic(ans,ind,tmp)
        else:
            tmp,ratedHis = getdatasa(name)
            real = tmp[len(tmp)-1]["NewRating"]
            ans,ind=maximizeRate(tmp,ratedHis)
            final = makeoutputDic(ans,ind,tmp)
    except:
        name="hdnkt"
        tmp,ratedHis = getdatasa(name)
        real = tmp[len(tmp)-1]["NewRating"]
        ans,ind=maximizeRate(tmp,ratedHis)
        final = makeoutputDic(ans,ind,tmp)
        error = "入力された名前のユーザーは存在しません。"
    
    highest = final[len(final)-1]["NewRating"]
    dist = "+"+str(highest-real) if highest-real >= 0 else str(highest-real)

    return render(request,"ratinggraph.html",{"final":final,"name":name,"error":error,"r":r,"highest":highest,"real":real,"dist":dist})


def db(request):
    greeting = Greeting()
    greeting.save()
    greetings = Greeting.objects.all()
    return render(request, "db.html", {"greetings": greetings})
