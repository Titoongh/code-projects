# -*- coding: utf-8 -*-
import numpy as np
from random import randint, random, randrange, choice
import matplotlib
import matplotlib.pyplot as plt

def individual(length,max):
    #return name

def population(count, length,  max):
    #retun name_list

def evolve(pop, decision, retain=0.2, random_select=0.1, mutate=0.1):
    graded_score = [ (score(decision,x), x) for x in pop]
    score_pop = sum([g[0] for g in graded_score])
    graded = [ x[1] for x in sorted(graded_score,reverse=True)]
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
            pos_to_mutate = randint(0, len(individual)-1)
            individual[pos_to_mutate] = mutation

    parents_length = len(parents)
    desired_length = len(pop) - parents_length
    children = []
    while len(children) < desired_length:
        male = randint(0, parents_length-1)
        female = randint(0, parents_length-1)
        male = parents[male]
        female = parents[female]
        #keep first and last part
        children.append(child)
    parents.extend(children)
    return parents, score_pop, graded_score


