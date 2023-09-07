import pickle

with open('cp_scheduling_answer2.pickle', mode='rb') as fr:
    user_loaded1 = pickle.load(fr)

with open('cp_scheduling_ortools_answer2.pickle', mode='rb') as fs:
    user_loaded2 = pickle.load(fs)

with open('milp_scheduling_ortools_answer3.pickle', mode='rb') as ff:
    user_loaded3 = pickle.load(ff)

with open('milp_scheduling_answer3.pickle', mode='rb') as ff:
    user_loaded4 = pickle.load(ff)
print("1123213")