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
len_pop = 1000
len_name = 5
pop = []
for i in range(len_pop):
    len_name = np.random.randint(4,9)
    pop.append(create_name(alpha_mat,alpha_dic,len_name= len_name))
for j in range(nb_gen):
    #modifier fonction de name mixing pour creer quelque chose de plausible
    #gerer erreur dic
    print j
    #penser a supprimer les noms egaux
    #possible de faire une mutation si le prénom mixé existe déjà
    #bien relire le code
    pop, score_pop = evolve(pop,alpha_dic,alpha_mat,rel_mat,profile)

for name in parents[:20]:
    print name


