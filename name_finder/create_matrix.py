# -*- coding: utf-8 -*-
import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt

alpha_dic = {'a':0,
            'b':1,
            'c':2,
            'd':3,
            'e':4,
            'f':5,
            'g':6,
            'h':7,
            'i':8,
            'j':9,
            'k':10,
            'l':11,
            'm':12,
            'n':13,
            'o':14,
            'p':15,
            'q':16,
            'r':17,
            's':18,
            't':19,
            'u':20,
            'v':21,
            'w':22,
            'x':23,
            'y':24,
            'z':25,
            '0':26,
            '1':27
            }
trad_ascii = {'\xef':u'ï',
                '\xee':u'î',
                '\xe9':u'é',
                '\xc8':u'è',
                '\xe8':u'è',
                '\xf4':u'ô',
                '\xe7':u'ç',
                '\xe2':u'â',
                '\xc9':u'é',
                '\xeb':u'ë'
                }

def upgrade_mat(alpha_dic,alpha_mat,l):

    alpha_dic[l] = len(alpha_dic)

    alpha_mat = np.vstack((alpha_mat,np.zeros((1,len(alpha_dic)-1))))
    alpha_mat = np.hstack((alpha_mat,np.zeros((len(alpha_dic),1))))
    return alpha_dic,alpha_mat

if __name__ == '__main__':

    data = pd.DataFrame().from_csv('name_list.csv')
    alpha_mat = np.zeros((len(alpha_dic),len(alpha_dic)))

    for j in range(len(data)):
        name = data.ix[j,'name']
        for i,l in enumerate(name):#iterate over letters in word
            l = l.lower()
            if l in trad_ascii.keys():#use unicode
                l = trad_ascii[l]

            #If new letter, upgrade matrice and dic
            if l not in alpha_dic.keys():
                alpha_dic, alpha_mat = upgrade_mat(alpha_dic,alpha_mat,l)
            idx_l = alpha_dic[l]

            if i == 0 : #27 is the index of '1' which mean first letter
                alpha_mat[27][idx_l]+= 1

            #use unicode for next l
            try :
                next_l = name[i+1].lower()
                if next_l in trad_ascii.keys():
                    next_l = trad_ascii[next_l]
            except :
                next_l = '0'

            #upgrade matrice and dic if new letter
            if next_l not in alpha_dic.keys():
                alpha_dic, alpha_mat = upgrade_mat(alpha_dic,alpha_mat,next_l)
            idx_next = alpha_dic[next_l]

            #fill matrice
            alpha_mat[idx_l][idx_next] += 1

            if i == 0:
                last_l = '1'
            else:
                last_l = name[i-1].lower()
            if last_l in trad_ascii.keys():
                last_l = trad_ascii[last_l]
            seq = last_l + l
            if seq not in alpha_dic.keys():
                alpha_dic, alpha_mat = upgrade_mat(alpha_dic,alpha_mat,seq)
            idx_second = alpha_dic[seq]
            alpha_mat[idx_second][idx_next] += 1

    for i,row in enumerate(alpha_mat):
        if i != 26 :
            alpha_mat[i] /= alpha_mat[i].sum()
        else:
            alpha_mat[i] = alpha_mat[i]
            continue

    fig, ax= plt.subplots()
    xy = []
    for i in range(len(alpha_dic)):
        xy.append(alpha_dic.keys()[alpha_dic.values().index(i)])

    ax.set_xticklabels(xy)
    ax.set_xticks(np.arange(len(xy)))
    ax.set_yticks(np.arange(len(xy)))
    ax.set_yticklabels(xy)
    im = ax.imshow(alpha_mat, cmap = 'jet',interpolation = 'nearest', origin='lower')
    clim=im.properties()['clim']
    fig.colorbar(im, shrink=0.5)
    plt.show()

    print alpha_mat
    print alpha_dic
    alpha_mat = pd.DataFrame(alpha_mat)
    alpha_mat.to_csv('alphabet_matrice.csv')
    with open("alphabet_dic.txt", 'w') as file:
        json.dump(alpha_dic, file)
























