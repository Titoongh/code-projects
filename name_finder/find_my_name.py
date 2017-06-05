# -*- coding: utf-8 -*-
import json
import pandas as pd
import numpy as np
import random
LEN_NAME = 5

def find_next(alpha_mat,alpha_dic,idx):
    candidates = []
    # print 'seq : ', alpha_dic.keys()[alpha_dic.values().index(idx)]
    for i,l in enumerate(alpha_mat[idx]):
        if l != 0 :
            # print 'prob next', l, alpha_dic.keys()[alpha_dic.values().index(i)]
            candidates.append([alpha_dic.keys()[alpha_dic.values().index(i)]]*np.round(l*100))
    candidates = list(np.concatenate(candidates))
    candidates = [c for c in candidates if c !='0']
    # print candidates
    np.random.shuffle(candidates)
    try :
        r = random.randrange(0,len(candidates))
    except :
        return None

    return candidates[r]

def find_last(alpha_mat,alpha_dic,idx):
    candidates = []
    seq =  alpha_dic.keys()[alpha_dic.values().index(idx)]
    # print seq
    for alph in alpha_dic.keys():
        if  alph != '0' :
            try :
                idx = alpha_dic[seq[1] + alph]
            except :
                continue
            # print alph
            if  alpha_mat[alpha_dic[seq]][alpha_dic[alph]]> 0.0 and alpha_mat[idx][26] > 0 :
                # print 'go'
                candidates.append([alpha_dic.keys()[alpha_dic.values().index(idx)]]*np.round(alpha_mat[idx][26]*100))

    # print candidates

    try :
        candidates = list(np.concatenate(candidates))

        # print candidates
        candidates = [c for c in candidates if c !='0']
        np.random.shuffle(candidates)
        r = random.randrange(0,len(candidates))
    except :
        return None

    return candidates[r]


def create_name(alpha_mat, alpha_dic,len_name = LEN_NAME):
    my_new_name = ''
    for n in range(len_name):
        # print n
        if n >= 2 :
            # print my_new_name[n-2:n]
            idx = alpha_dic[my_new_name[n-2:n]]
        elif n == 1 :
            # print my_new_name[-1]
            idx = alpha_dic['1'+my_new_name[-1]]
        else:
            idx = 27

        if n != len_name -1:
            new = find_next(alpha_mat,alpha_dic,idx)
        else :
            # print my_new_name
            new = find_last(alpha_mat,alpha_dic,idx)
        if new == None :
            break
        my_new_name += new[-1]
        # if my_new_name[-1] == '0':
    # print 'YOUR NEW NAME IS : ',my_new_name
    return my_new_name

if __name__ == '__main__':

    with open('alphabet_dic.txt','r') as file:
        alpha_dic = json.load(file)

    alpha_mat = pd.DataFrame().from_csv('alphabet_matrice.csv')
    alpha_mat = np.array(alpha_mat)
    print alpha_dic

    df = pd.DataFrame(columns=['name'])
    for t in range(100):
        name = create_name(alpha_mat,alpha_dic)
        df.loc[t,'name'] = name

    df.to_csv('user_profile.csv')

