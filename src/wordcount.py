__author__ = 'juliewe'

import sys

def foobar():
    foobar="Three blind mice"
    foobar2=list(foobar)
    count=0
    for thing in foobar2:
        count+=1
    print count
    print len(foobar2)
    print len(foobar)

def wc(filename):
    with open(filename,'r') as instream:

        linecount=0
        wordcount=0
        charcount=0
        for line in instream:
            linecount+=1
            charcount+=len(line)
            words=line.rstrip().split(' ')
            wordcount+=len(words)

        print linecount, wordcount, charcount


if __name__=='__main__':

    if len(sys.argv)<2:
        foobar()
    else:
        filename=sys.argv[1]
        print filename
        wc(filename)

