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

def getdatas(name):
    site=requests.get("https://atcoder.jp/users/"+name)
    data = BeautifulSoup(site.text,"html.parser")
    #print(data)
    ret = data.find_all("script")

    his = requests.get('https://atcoder.jp/users/'+name+'/history/json').json()
    tmp = json.loads(str(ret[12])[27:-10])

    return tmp,onlyRated(his)

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


def maximizeRate(ratedHis):#単調増加するように選択
    now = [ratedHis[0]["Performance"]]
    ans = 800*math.log2(2**(now[0]/800))-1200
    ans = [round(helpBeginner(ans))]
    ind = [0]
    for i in range(1,len(ratedHis)):
        pre = ans[len(ans)-1]
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
        print(ind[i])
        ret.append(tmp[ind[i]])
        ret[i]["OldRating"]=ret[i-1]["NewRating"]
        ret[i]["NewRating"]=ans[i]
    return ret


#tmp,ratedHis = getdatas("rokahikou")
#ans,ind=maximizeRate(ratedHis)
#final = makeoutputDic(ans,ind,tmp)