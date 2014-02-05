__author__ = 'juliewe'
###
#wnsim.py is a possible "solution" for lab 2
#there are many other possible solutions - many of which may be neater and/or more efficient
###

from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic as wn_ic
import sys
import numpy as np
#from extra import mypearson
import matplotlib.pyplot as plt

def sssim(s1,s2,metric,ic):

    #function to call the correct wordnet similarity metric on two wordnet synsets (given an ic file)

    if metric =='path':
        return s1.path_similarity(s2)
    elif metric == 'res':
        return s1.res_similarity(s2,ic)
    elif metric == 'lin':
        return s1.lin_similarity(s2,ic)
    else:
        print "Error: unknown metric"
        exit()

def wnsim(word1,word2,ps = wn.NOUN, metric='path',ic=wn_ic.ic('ic-brown.dat')):

    #function to calculate wn similarity of two words
    #maximises similarity over all senses of the given part of speech (by default noun)

    ss1=wn.synsets(word1,pos=ps)
    ss2=wn.synsets(word2,pos=ps)

    maxsim = 0
    for s1 in ss1:
        for s2 in ss2:
            thissim = sssim(s1,s2,metric,ic)
            if thissim>maxsim:
                maxsim=thissim

    #print maxsim
    return maxsim

def test(wordlist):

    #prints out all of the definitions of all of the words in wordlist
    for word in wordlist:

        ss = wn.synsets(word,pos=wn.NOUN)
        for s in ss:
            print s.definition

def loadfile(fn):
    #reads in the mcdata file and stores human score in a dictionary (key = word pair, value = score)
    scoredict={}
    with open(fn,'r') as instream:

        for line in instream:
            parts=line.rstrip().split(',')
            #print parts
            pair=(parts[0],parts[1])
            scoredict[pair]=float(parts[2])

    return scoredict

def wnpairs(pairlist,metric='path'):
    #creates a score dictionary for word pairs in wordlist for the given similarity measure
    scoredict={}
    for (a,b) in pairlist:

        sim = wnsim(a,b,metric=metric)
        scoredict[(a,b)]=sim
    return scoredict

def myscatter(xs,ys,thisxlabel='',thisylabel='',thistitle='',c=''):
    plt.scatter(xs,ys)
    plt.xlim(0,5)
    if thisylabel=='res':
        plt.ylim=(0,14)
    else:
        plt.ylim=(0,1)
    plt.xlabel(thisxlabel)
    plt.ylabel(thisylabel)
    plt.title(thistitle)
    plt.text(0.2,1,'pearson = '+str(c))
    plt.show()



if __name__=="__main__":

    testwords=['car','chicken']
    #testwords=['car','automobile']
    metrics=['path','res','lin']
    test(testwords)
    for met in metrics:
        sim = wnsim(testwords[0],testwords[1],metric=met)
        print testwords[0],testwords[1],met, str(sim)

    filename=sys.argv[1]
    mcscores=loadfile(filename)
    print mcscores
    for met in metrics:
        wnscores=wnpairs(mcscores.keys(),met)
        print wnscores
        xs=[]
        ys=[]
        for key in mcscores.keys():
            xs.append(mcscores.get(key,0))
            ys.append(wnscores.get(key,0))
        xarray=np.array(xs)
        yarray=np.array(ys)
        #print mypearson(xs,ys)
        corr=np.corrcoef(xarray,yarray)[0,1]

        myscatter(xs,ys,c=corr,thistitle='Correlation between WN and Human Judgements',thisxlabel='Human Judgements',thisylabel=met)
        print "Correlation between human judgements and "+met+" is "+str(corr)
