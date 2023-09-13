import pickle

with open('problem/cp_scheduling_answer_S31.pickle', mode='rb') as fr:
    cp_scheduling = pickle.load(fr)
with open('problem/cp_scheduling_ortools_answer_S31.pickle', mode='rb') as fs:
    cp_scheduling_ortools = pickle.load(fs)
with open('problem/milp_scheduling_answer_S31.pickle', mode='rb') as fx:
    milp_scheduling = pickle.load(fx)
with open('problem/milp_scheduling_ortools_answer_S31.pickle', mode='rb') as fd:
    milp_scheduling_ortools = pickle.load(fd)
gg = []

print("cp_scheduling : " , sum(cp_scheduling['object_value'])/len(cp_scheduling['object_value']),sum(cp_scheduling['time'])/len(cp_scheduling['time']))
print("cp_scheduling_ortools : " , sum(cp_scheduling_ortools['object_value'])/len(cp_scheduling_ortools['object_value']),sum(cp_scheduling_ortools['time'])/len(cp_scheduling_ortools['time']))
print("milp_scheduling : " , sum(milp_scheduling['object_value'])/len(milp_scheduling['object_value']),sum(milp_scheduling['time'])/len(milp_scheduling['time']))
print("milp_scheduling_ortools : " , sum(milp_scheduling_ortools['object_value'])/len(milp_scheduling_ortools['object_value']),sum(milp_scheduling_ortools['time'])/len(milp_scheduling_ortools['time']))
