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
    error = ""
    name = username
    sex = "male"
    try:
        if sex =="female":
            dic=manycontest()
            tmp,ratedHis = getdatas(name,dic)
            ans,ind=maximizeRate(tmp,ratedHis)
            final = makeoutputDic(ans,ind,tmp)
        else:
            tmp,ratedHis = getdatasa(name)
            ans,ind=maximizeRate(tmp,ratedHis)
            final = makeoutputDic(ans,ind,tmp)
    except:
        name="hdnkt"
        tmp,ratedHis = getdatasa(name)
        ans,ind=maximizeRate(tmp,ratedHis)
        final = makeoutputDic(ans,ind,tmp)
        error = "入力された名前のユーザーは存在しません。"

    return render(request,"ratinggraph.html",{"final":final,"name":name,"error":error})

def vote(request):
    error = " "
    try:
        name = request.POST["username"]
        sex = request.POST["sex"]
    except:
        name = "hdnkt"
        sex = "male"
    #該当ユーザーの履歴をjsonでゲット
    #r = requests.get('https://atcoder.jp/users/'+tmp+'/history/json').json()

    #スクレイビング
    #site=requests.get("https://atcoder.jp/users/"+tmp)
    #data = BeautifulSoup(site.text,"html.parser")

    try:
        if sex =="female":
            dic=manycontest()
            tmp,ratedHis = getdatas(name,dic)
            ans,ind=maximizeRate(tmp,ratedHis)
            final = makeoutputDic(ans,ind,tmp)
        else:
            tmp,ratedHis = getdatasa(name)
            ans,ind=maximizeRate(tmp,ratedHis)
            final = makeoutputDic(ans,ind,tmp)
    except:
        name="hdnkt"
        tmp,ratedHis = getdatasa(name)
        ans,ind=maximizeRate(tmp,ratedHis)
        final = makeoutputDic(ans,ind,tmp)
        error = "入力された名前のユーザーは存在しません。"

    return render(request,"ratinggraph.html",{"final":final,"name":name,"error":error})


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
