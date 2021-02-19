from bs4 import BeautifulSoup
import requests
import json
import math

def helpBeginner(r):
    if r <=400:
        return 400/(math.e**((400-r)/400))
    else:
        return r
    
def rejectReset(n):
    return 1200*(math.sqrt(1-0.81**n)/(1-0.9**n)-1)/(math.sqrt(19)-1)

def getdatas(name,dic):
    site=requests.get("https://atcoder.jp/users/"+name+"?graph=rating")
    data = BeautifulSoup(site.text,"html.parser")
    #print(data)
    ret = data.find_all("script")
    his = requests.get('https://atcoder.jp/users/'+name+'/history/json').json()
    tmp = json.loads(str(ret[12])[27:-10])

    for i in range(len(tmp)):
        tmp[i]["StandingsU"]=tmp[i]["StandingsUrl"]
        tmp[i]["StandingsUrl"]="https://atcoder.jp"+tmp[i]["StandingsUrl"]

        try:
            reg=dic[tmp[i]["StandingsU"].split(sep="/")[2]].split()
            if len(reg)==1:
                tmp[i]["low"]=0
                tmp[i]["high"]=10000
            else:
                if reg[0]=="-":
                    tmp[i]["low"]=0
                    tmp[i]["high"]=int(reg[1])
                else:
                    tmp[i]["low"]=int(reg[0])
                    tmp[i]["high"]=10000
        except:
            tmp[i]["low"]=0
            tmp[i]["high"]=10000

    return tmp,onlyRated(his)

def getdatasa(name):
    site=requests.get("https://atcoder.jp/users/"+name+"?graph=rating")
    data = BeautifulSoup(site.text,"html.parser")
    #print(data)
    ret = data.find_all("script")
    his = requests.get('https://atcoder.jp/users/'+name+'/history/json').json()
    tmp = json.loads(str(ret[12])[27:-10])

    for i in range(len(tmp)):
        tmp[i]["StandingsU"]=tmp[i]["StandingsUrl"]
        tmp[i]["StandingsUrl"]="https://atcoder.jp"+tmp[i]["StandingsUrl"]
        tmp[i]["low"]=0
        tmp[i]["high"]=10000

    return tmp,onlyRated(his)

def Rated(contestName):
    sit = requests.get("https://atcoder.jp/contests/"+contestName)
    data = BeautifulSoup(sit.text,"html.parser")
    ret = data.find_all("p")
    ret=ret[2].text
    ret=ret.split("\n")
    ret = ret[2].split()
    low = 0
    high = 10000
    if len(ret)==3:
        low=0
        high=10000
    else:
        if ret[2]=="-":
            low=0
            high=int(ret[3])
        else:
            low=int(ret[2])
            high = 10000
    return low,high

def manycontest():
    dic = {}
    for p in range(1,10):
        sit = requests.get("https://atcoder.jp/contests/archive?page="+str(p))
        data = BeautifulSoup(sit.text,"html.parser")
        ret = data.find_all("tr")
        ans=ret
        for i in range(len(ans)):
            sp = str(ans[i]).split(sep="/")
            if len(sp)>10 and ans[i].text.split(sep="\n")[7]!="-":
                dic[sp[10].split(sep="\"")[0]]=ans[i].text.split(sep="\n")[7]
    return dic

def onlyRated(his):
    ratedHis = []
    pefdic = {}
    for i in range(len(his)):
        if i >= len(his):
            break
        #print(his[i])
        if his[i]["IsRated"]==True:
            ratedHis.append(his[i])
    return ratedHis


def maximizeRate(tmp,ratedHis):#単調増加するように選択
    now = [ratedHis[0]["Performance"]]
    ans = 800*math.log2(2**(now[0]/800))-1200
    ans = [round(helpBeginner(ans))]
    ind = [0]
    for i in range(1,len(ratedHis)):
        pre = ans[len(ans)-1]
        if pre < tmp[i]["low"] or tmp[i]["high"] < pre:
            continue
        this = 0.9*(2**(ratedHis[i]["Performance"]/800))
        for j in range(len(now)):
            this+=(2**(now[len(now)-j-1]/800))*(0.9**(j+2))

        this = this/((0.9*(0.9**(len(now)+1))-0.9)/(0.9-1))
        this = 800*math.log2(this)
        this = this-rejectReset(len(now)+1)
        this = helpBeginner(this)
        if pre <= this:
            ans.append(round(this))
            now.append(ratedHis[i]["Performance"])
            ind.append(i)
    return ans,ind

def calculateRate(ratedHis,ind):#使うindexを渡す
    now = [ratedHis[ind[0]]["Performance"]]
    ans = 800*math.log2(2**(now[0]/800))-1200
    ans = [round(helpBeginner(ans))]
    for k in range(1,len(ind)):
        i = ind[k]
        pre = ans[len(ans)-1]
        this = 0.9*(2**(ratedHis[i]["Performance"]/800))
        for j in range(len(now)):
            this+=(2**(now[len(now)-j-1]/800))*(0.9**(j+2))

        this = this/((0.9*(0.9**(len(now)+1))-0.9)/(0.9-1))
        this = 800*math.log2(this)
        this = this-rejectReset(len(now)+1)
        this = helpBeginner(this)
        ans.append(round(this))
        now.append(ratedHis[i]["Performance"])
    return ans,ind

def makeoutputDic(ans,ind,tmp):
    ret = []
    ret.append(tmp[ind[0]])
    ret[0]["OldRating"]=0
    ret[0]["NewRating"]=ans[0]
    for i in range(1,len(ans)):
        #print(ind[i])
        ret.append(tmp[ind[i]])
        ret[i]["OldRating"]=ret[i-1]["NewRating"]
        ret[i]["NewRating"]=ans[i]
    return ret



name="yamunaku"
dic = manycontest()
tmp,ratedHis = getdatas(name,dic)
ans,ind=maximizeRate(tmp,ratedHis)
final = makeoutputDic(ans,ind,tmp)

a = [[6,11]]
b = []
b.append(a[0])
b[0][1]=8
print(a)
#[{6: 8}]