import random

from module import *

import pickle

num=0

for i in range(30):
    num += 1
    problem = generate_prob(12 , 4)
    with open('problem_L{}.pickle'.format(num), mode='wb') as fw:
        pickle.dump(problem, fw)


