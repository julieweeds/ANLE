__author__ = 'juliewe'
import math
import matplotlib

def myplot

def minusmean(list):
    total=0.0
    count=0.0
    for number in list:
        total+=number
        count+=1.0

    mean=total/count
    newlist=[]
    for number in list:
        newlist.append(number-mean)
    return newlist

def mypearson(list1,list2):
    list1=minusmean(list1)
    list2=minusmean(list2)
    #print list1,list2
    XY = 0
    XX=0
    YY=0
    for i,x in enumerate(list1):
        XX +=x*x
        YY += list2[i]*list2[i]
        XY += x*list2[i]

    #print XX,XY,YY

    r = XY / math.pow(XX*YY,0.5)
    return r