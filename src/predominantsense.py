__author__ = 'juliewe'

from nltk.corpus import wordnet as wn
from nltk.corpus import lin_thesaurus as lin
#import wnsim
import operator

noun_lin = 'simN.lsp'
k = 10
mywords = ['bow','hull']


def wnsensesim(synset1, synset2, metric):
    #return wn similarity of two synsets according to metric

    if metric == 'path_similarity':
        return wn.path_similarity(synset1, synset2)
    else:#add more similarity measures e.g., jcn
        print "Unsupported wn similarity measure requested"


def wnss(word, synset, metric='path_similarity', pos=wn.NOUN):
    #return the wn similarity of word to synset - maximised over the senses of word, determined by metric

    senses = wn.synsets(word, pos)
    if len(senses)==0:
        print "Warning: no WN synsets for "+word
    max = 0
    for sense in senses:
        sim = wnsensesim(sense, synset, metric)
        if sim > max: max = sim
    return max


def prevalent_sense(word,pos=wn.NOUN):
    #determine the prevalence
    distthes = lin.scored_synonyms(word, fileid=noun_lin)
    sortedthes = sorted(distthes, key=operator.itemgetter(1), reverse=True)[0:k]
    #print sortedthes

    scores = {}  #dict for the scores for each sense which will be contributed to by each neighbour

    for wnsynset in wn.synsets(word,pos):
        #initialise scores for each synset as 0
        scores[wnsynset.name] = 0

    for (neigh, dss) in sortedthes:
        if len(wn.synsets(neigh))>0: #check neighbour is in WN otherwise all sims will be 0

            sum = 0  #this will be the sum of wnss scores for this distributional neighbour (summed over all senses)
            neighscores = {}  #this stores the wnss scores for each sense for this neighbour
                            #it could be a list with index corresponding to WN synset number
                            #will need to divide by sum and times by dss before adding to the sum over all distributional neighbours for each sense
            for wnsynset in wn.synsets(word,pos):
                wnss_score = wnss(neigh, wnsynset,pos=pos)#look up wnss score for this neighbour and this sense
                sum += wnss_score  #add it to the sum over all senses for the neighbour
                neighscores[wnsynset.name] = wnss_score  #store it in dictionary so that each value can later be divided by sum
            #print neighscores,sum,dss
            for wnsynset in wn.synsets(word,pos):#second loop is needed to divide by sum (which is not known until completion of first loop)
                                                #sum will be different for each neighbour so it is not a constant which can be ignored
                scores[wnsynset.name] += dss * neighscores[wnsynset.name] / sum  #weight the score for each sense (according to this neighbour)
                                                                    # by its dss score and inversely by the sum of wnss scores for this neighbour
                                                                    # and add to the total for this sense
        else:
            print "Warning: ignoring distributional neighbour "+neigh+" : not in WordNet as noun"  #this is likely to happen when distributional neighbours are proper nouns see 'hull' example
                                                #probably should modifiy code so that it is the top k neighbours excluding words not in WN


    scoreslist = [scoretuple for scoretuple in scores.items()]
    sortedscores = sorted(scoreslist, key=operator.itemgetter(1), reverse=True)
    #print sortedscores
    return sortedscores[0]


if __name__ == '__main__':

    #mywords is list of words for which to find prevalent sense
    #could be returned by a function or read from a file (e.g., all of the nouns in a given sentence)

    for word in mywords:
    #for synset in wn.synsets(word):
    #   print synset,synset.name

        (sense, score) = prevalent_sense(word)
        print word, sense, wn.synset(sense).definition, score


