# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import json


vowels = ['a','e','i','o','u','y',u'â',u'à',u'é',u'è',u'ë',u'ê',u'ï',u'î',u'ö',u'ô',u'ù',u'ü',u'û']

with open('alphabet_dic.txt','r') as file:
    alpha_dic = json.load(file)

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
            # print n1_c[j]
            # print n2_c[j]
            # print rel_mat.ix[n1_c[j],n2_c[j]]
            score += rel_mat.ix[n1_c[j],n2_c[j]]
    return score


name1 = 'amelie'
# name2 = 'martin'
name2 = 'proutlepate'
# name2 = 'melanie'

rel_mat = create_relations(alpha_dic)
score = correl_name(name1,name2,rel_mat)
if len(name1) >= len(name2) :
    score /= correl_name(name1,name1,rel_mat)
else :
    score /= correl_name(name2,name2,rel_mat)
print score

