from django.shortcuts import render
from django.http import HttpResponse
import requests
import os
import json
from bs4 import BeautifulSoup
from .models import Greeting
from .skr import getdatas,maximizeRate,makeoutputDic,manycontest


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
    return vote(request)

def vote(request):
    manycontest()
    error = " "
    try:
        name = request.POST["username"]
    except:
        name = "hdnkt"
    #該当ユーザーの履歴をjsonでゲット
    #r = requests.get('https://atcoder.jp/users/'+tmp+'/history/json').json()

    #スクレイビング
    #site=requests.get("https://atcoder.jp/users/"+tmp)
    #data = BeautifulSoup(site.text,"html.parser")

    try:
        tmp,ratedHis = getdatas(name)
        ans,ind=maximizeRate(tmp,ratedHis)
        final = makeoutputDic(ans,ind,tmp)
    except:
        name="hdnkt"
        tmp,ratedHis = getdatas(name)
        ans,ind=maximizeRate(tmp,ratedHis)
        final = makeoutputDic(ans,ind,tmp)
        error = "入力された名前のユーザーは存在しません。"

    return render(request,"ratinggraph.html",{"final":final,"name":name,"error":error})


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
