import random
from module import *
import pickle
num=0
for i in range(40):
    num += 1
    a = i+1
    problem = generate_prob(4+a , 4)
    with open('problem{}.pickle'.format(num), mode='wb') as fw:
        pickle.dump(problem, fw)
    num += 1

