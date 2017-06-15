# -*- coding: utf-8 -*-
import numpy as np
from random import randint, random, randrange, choice
import matplotlib
import matplotlib.pyplot as plt
from find_my_name import find_next, find_last
import pandas as pd
from difflib import SequenceMatcher
import editdist
import unicodedata
import fuzzy
import sys
sys.path.append('python-Levenshtein/Levenshtein')
from StringMatcher import StringMatcher
vowels = ['a','e','i','o','u','y',u'â',u'à',u'é',u'è',u'ë',u'ê',u'ï',u'î',u'ö',u'ô',u'ù',u'ü',u'û']



def create_relations(alpha_dic):
    rel_mat = pd.DataFrame()
    # rel_mat.index = alpha_dic.keys()
    # rel_mat.columns = alpha_dic.keys()
    for key in alpha_dic.keys():
        if len(key) < 2 and key not in ['0','1']:
            for k in alpha_dic.keys():
                if len(k) < 2 and k not in ['0','1']:
                    if key == k:
                        rel_mat.loc[key,k]= 1
                        continue
                    if key in vowels and k in vowels :
                        rel_mat.loc[key,k] = 0.5
                        continue
                    if key not in vowels and k not in vowels :
                        rel_mat.loc[key,k] = 0.5
                        continue
                    else :
                        rel_mat.loc[key,k] = 0

    return rel_mat


def correl_name(name1,name2,rel_mat):
    n1 = name1
    n2 = name2
    if len(name2) > len(name1) :
        n2 = name1
        n1 = name2
    score = 0
    diff = len(n1) - len(n2)
    for i in range(len(n1)):
        if i <= len(n2):
            n1_c = n1[len(n1)-1-i:-1]
            n2_c = n2[:i]
        else :
            dec = i - len(n2)
            n1_c = n1[len(n1)-1-i:-1-dec]
            n2_c = n2
        for j in range(len(n1_c)):
            score += rel_mat.ix[n1_c[j],n2_c[j]]
    return score

def seq_matcher(name1,name2):
    name1 = unicode(unicodedata.normalize('NFKD', name1).encode('ascii', 'ignore'),'utf-8')
    name2 = unicode(name2,'utf-8')
    name2 = unicode(unicodedata.normalize('NFKD', name2).encode('ascii', 'ignore'),'utf-8')

    soundex = fuzzy.Soundex(4)
    name1 = soundex(name1)
    name2 = soundex(name2)

    # dmeta = fuzzy.DMetaphone()
    # name1 = dmeta(name1)[0]
    # name2 = dmeta(name2)[0]

    # name1 = fuzzy.nysiis(name1)
    # name2 = fuzzy.nysiis(name2)

    m = SequenceMatcher(None, name1, name2)
    # Calculate an edit distance"abcef"
    # print 'm',m.ratio()
    e = editdist.distance(name1, name2)
    # print 'e',e
    sm = StringMatcher(seq1=name1,seq2=name2)
    # return e
    # print sm.distance()
    return sm.distance()


def score(name1,user_profil,rel_mat):
    mean_score = 0
    # print 'name 1',name1
    for name2 in user_profil['name']:
        # print 'name 2', name2
        score = seq_matcher(name1,name2)
        # score = correl_name(name1,name2,rel_mat)
        # if len(name1) >= len(name2) :
        #     score /= correl_name(name1,name1,rel_mat)
        # else :
        #     score /= correl_name(name2,name2,rel_mat)
        mean_score += score
    mean_score /= len(user_profil['name'])
    return mean_score


def evolve(pop,alpha_dic,alpha_mat,rel_mat,user_profil,retain=0.2, random_select=0.1, mutate=0.1):
    graded_score = [ (score(x,user_profil,rel_mat), x) for x in pop]
    print graded_score
    score_pop = sum([g[0] for g in graded_score])/float(len(graded_score))
    # graded = [ x[1] for x in sorted(graded_score,reverse=True)]
    graded = [ x[1] for x in sorted(graded_score,reverse=False)]
    print graded
    retain_length = int(len(graded)*retain)
    parents = graded[:retain_length]
    # randomly add other individuals to
    # promote genetic diversity
    for individual in graded[retain_length:]:
        if random_select > random():
            parents.append(individual)

    # mutate some individuals
    for individual in parents:
        if mutate > random():
            #change one vowel or one cons
            new = None
            # print individual
            while new == None :
                pos_to_mutate = randint(0, len(individual)-1)
                # print 'pos', pos_to_mutate
                # print individual[pos_to_mutate]
                if pos_to_mutate >= 2 :
                    # print '2',individual[pos_to_mutate-2:pos_to_mutate]
                    idx = alpha_dic[individual[pos_to_mutate-2:pos_to_mutate]]
                elif pos_to_mutate == 1 :
                    idx = alpha_dic['1'+individual[0]]
                else:
                    idx = 27

                if pos_to_mutate != len(individual) -1:
                    new = find_next(alpha_mat,alpha_dic,idx)
                else :
                    new = find_last(alpha_mat,alpha_dic,idx)

                # print 'new',new
                if new == None or new == individual[pos_to_mutate]:
                    # exit()
                    continue
                try:
                    last = individual[pos_to_mutate-1]
                except :
                    last = '0'
                try:
                    after = individual[pos_to_mutate+1]
                except :
                    after = '1'
                try :
                    if alpha_mat[alpha_dic[last+new]][alpha_dic[after]] == 0:
                        # print 'lol'
                        new = None
                except :
                    new = None

            new_ind = ''
            for i in range(len(individual)):
                if i == pos_to_mutate  :
                    new_ind += new
                else :
                    new_ind += individual[i]

    parents_length = len(parents)
    desired_length = len(pop) - parents_length
    children = []
    while len(children) < desired_length:
        male = randint(0, parents_length-1)
        female = randint(0, parents_length-1)
        male = parents[male]
        female = parents[female]
        len_f = len(female)/2
        len_m = len(male)-len_f-1
        #keep first and last part
        child = male[:len_m]+female[len_f:]
        children.append(child)
    parents.extend(children)

    print score_pop
    return parents, score_pop


