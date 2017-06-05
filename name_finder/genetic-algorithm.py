# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import json
from GA_func import create_relations, evolve
from find_my_name import create_name

profile = pd.DataFrame().from_csv('user_profile.csv')

with open('alphabet_dic.txt','r') as file:
    alpha_dic = json.load(file)

alpha_mat = pd.DataFrame().from_csv('alphabet_matrice.csv')
alpha_mat = np.array(alpha_mat)

rel_mat = create_relations(alpha_dic)

nb_gen = 30
len_pop = 50
len_name = 5
pop = []
for i in range(len_pop):
    pop.append(create_name(alpha_mat,alpha_dic,len_name= len_name))
for j in range(nb_gen):
    parents, score_pop = evolve(pop,alpha_dic,alpha_mat,rel_mat,profile)

for name in parents[:20]:
    print name


