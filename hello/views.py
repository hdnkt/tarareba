from django.shortcuts import render
from django.http import HttpResponse
import requests
import os
import json
from bs4 import BeautifulSoup

from .models import Greeting


# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')

    #レーティンググラフ
    return render(request, "ratinggraph.html")

    #ティーポット
    #r = requests.get('http://httpbin.org/status/418')
    #print(r.text)
    #return HttpResponse('<pre>' + r.text + '</pre>')

    #
    #return render(request,"form.html")

def vote(request):
    tmp = request.POST["username"]
    #該当ユーザーの履歴をjsonでゲット
    #r = requests.get('https://atcoder.jp/users/'+tmp+'/history/json').json()

    #すくれいびんぐ
    site=requests.get("https://atcoder.jp/users/"+tmp)
    data = BeautifulSoup(site.text,"html.parser")

    ret = data.find_all("script")

    return HttpResponse('<pre>'+str(ret[12])[27:-10]+'</pre>')


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
