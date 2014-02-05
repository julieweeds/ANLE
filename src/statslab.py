__author__ = 'juliewe'

import math
import numpy as np
import matplotlib.pyplot as plt

def getSampleLists():
    #dummy function to return two lists of results
    listA=[79,72,80,76,72]
    listB=[74,76,71,75,70]
    return(listA,listB)

def sampling(xarray,yarray):

    xmean=np.mean(xarray)
    xstdev=np.std(xarray)
    xerror = xstdev/math.pow(len(xarray),0.5)
    ymean=np.mean(yarray)
    ystdev=np.std(yarray)
    yerror = ystdev/math.pow(len(yarray),0.5)


    return((xmean,xerror),(ymean,yerror))

def diffmeans(xarray,yarray):

    xmean=np.mean(xarray)
    xstdev=np.std(xarray)
    xn=len(xarray)

    xerror = xstdev/math.pow(xn,0.5)
    ymean=np.mean(yarray)
    ystdev=np.std(yarray)
    yn=len(yarray)
    yerror = ystdev/math.pow(yn,0.5)


    print "Mean, st. dev and error for x are "+ str(xmean)+", "+str(xstdev)+", "+str(xerror)
    print "Mean, st. dev and error for y are "+str(ymean)+", "+str(ystdev)+', '+str(yerror)

    observeddiff = xmean-ymean
    differror = xerror+yerror
    print "Difference of means is "+str(observeddiff)+" and estimated error is "+str(differror)
    zvalue = observeddiff/differror
    print "Z value is "+str(zvalue)
    if zvalue<cv:
        print "NOT SIGNIFICANT"
    else:
        print "SIGNIFICANT"

def meandiffs(xarray,yarray):

    difflist=[]
    for (x,y) in zip(xarray,yarray):
        difflist.append(x-y)
    diffarray=np.array(difflist)
    diffmean=np.mean(diffarray)
    dn=len(difflist)
    diffsd=np.std(diffarray)
    differror=diffsd/math.pow(dn,0.5)

    print "Mean, sd and error for diffs are "+str(diffmean)+", "+str(diffsd)+", "+str(differror)

    zvalue = diffmean/differror
    print "Z value is "+str(zvalue)
    if zvalue<cv:
        print "NOT SIGNIFICANT"
    else:
        print "SIGNIFICANT"

def fit(x,line):
    y=x*line[0]+line[1]
    return y


def myscatter(xs,ys,thisxlabel='',thisylabel='',thistitle='',c=''):
    xl=np.min(xs)-1
    yl=np.min(ys)-1
    yu=np.max(ys)+1
    xu=np.max(xs)+1

    xfit=np.array([xl,xu])

    myline = np.polyfit(xarray,yarray,1)
    print myline

    plt.plot(xs,ys,'o',xfit,fit(xfit,myline),'-r')
    plt.xlim(xl,xu)
    plt.ylim(yl,yu)
    plt.xlabel(thisxlabel)
    plt.ylabel(thisylabel)
    plt.title(thistitle)
    plt.text(xu-3.5,yu-1,'pearson = '+str(c))
    plt.show()



if __name__=="__main__":

    cv=1.645
    (xlist,ylist)=getSampleLists()

    xarray=np.array(xlist)
    yarray=np.array(ylist)

    diffmeans(xarray,yarray)
    meandiffs(xarray,yarray)

    r=np.corrcoef(xarray,yarray)[0,1]

    myscatter(xarray,yarray,c=r)