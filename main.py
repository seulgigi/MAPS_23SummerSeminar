from pulp import pulp, LpStatusOptimal, LpStatus
from module import *
from milp import *
from cp import *
import heuristic
import random
import time
import multiprocessing
import pickle
import pandas as pd

from pp import pulp_scheduling


def test1():
    load_time = []
    object = []
    sol_status = []
    total = {}
    c = 0
    for i in range(30):
        start_time = time.time()
        filename = "problem_M{}.pickle".format(i + 1)
        with open(filename, mode='rb') as fr:
            test_instance = pickle.load(fr)
            values = cp_scheduling_ortools(test_instance)
        end_time = time.time()
        loading_time = end_time - start_time
        if values != None:
            load_time.append(loading_time)
            object.append(values[0].ObjectiveValue())
            c+=1
            sol_status.append(values[1])
    total[time] = load_time
    total[value] = object
    total[count] = c
    total["answer"] = sol_status
    savething = {"object_value": total[value], "time": total[time], "status": total["answer"]}
    with open('cp_scheduling_ortools_answer_M{}.pickle'.format(c), mode='wb') as fw:
        pickle.dump(savething, fw)
    return total
def test2():
    load_time = []
    object = []
    sol_status = []
    total = {}
    c = 0
    for i in range(30):
        start_time = time.time()
        filename = "problem_M{}.pickle".format(i + 1)
        with open(filename, mode='rb') as fr:
            test_instance = pickle.load(fr)
            values = cp_scheduling(test_instance)
        end_time = time.time()
        loading_time = end_time - start_time
        if values != None:
            load_time.append(loading_time)
            object.append(values.get_objective_values()[0])
            c+=1
            sol_status.append(values.get_solve_status())
    total[time] = load_time
    total[value] = object
    total[count] = c
    total["answer"] = sol_status
    savething = {"object_value": total[value], "time": total[time], "status": total["answer"]}
    with open('cp_scheduling_answer_M{}.pickle'.format(c), mode='wb') as fw:
        pickle.dump(savething, fw)
    return total
def test3():
    # pywraplp.Solver.OPTIMAL => 0
    # pywraplp.Solver.FEASIBLE => 1
    load_time=[]
    object = []
    sol_status = []
    total = {}
    c=0
    for i in range(30):
        start_time = time.time()
        filename = "problem_M{}.pickle".format(i + 1)
        with open(filename, mode='rb') as fr:
            test_instance = pickle.load(fr)
            values = milp_scheduling_ortools(test_instance)
        end_time = time.time()
        loading_time = end_time - start_time
        if values != None:
            load_time.append(loading_time)
            object.append(values.Objective().Value())
            sol_status.append(values.Solve())
        c +=1
    total[time] = load_time
    total[value] = object
    total["num"] = c
    total["answer"] = sol_status
    savething = {"num_prob": total["num"], "object_value": total[value], "time": total[time],"status":total["answer"]}
    with open('milp_scheduling_ortools_answer_M{}.pickle'.format(c), mode='wb') as fw:
        pickle.dump(savething, fw)
    return total
def test4():
    load_time = []
    object = []
    sol_status = []
    total = {}
    c = 0
    for i in range(30):
        start_time = time.time()
        filename = "problem_M{}.pickle".format(i + 1)
        with open(filename, mode='rb') as fr:
            test_instance = pickle.load(fr)
            values = milp_scheduling(test_instance)
        end_time = time.time()
        loading_time = end_time - start_time
        if values != None :
            load_time.append(loading_time)
            object.append(values.objective_value)
            sol_status.append(values.solve_status.name)
        c+=1
    total[time] = load_time
    total[value] = object
    total["num"] = c
    total["answer"] = sol_status
    savething = {"num_prob": total["num"], "object_value": total[value], "time": total[time], "status": total["answer"]}
    with open('milp_scheduling_answer_M{}.pickle'.format(c), mode='wb') as fw:
        pickle.dump(savething, fw)
    return total

def test5():
    load_time = []
    object = []
    sol_status = []
    total = {}
    c = 0
    for i in range(30):
        start_time = time.time()
        filename = "problem_M{}.pickle".format(i + 1)
        with open(filename, mode='rb') as fr:
            test_instance = pickle.load(fr)
            values = gurobi_milp(test_instance)
        end_time = time.time()
        loading_time = end_time - start_time
        if values != None:
            load_time.append(loading_time)
            object.append(values.ObjVal)
            sol_status.append(values.status)
        c += 1
    total[time] = load_time
    total[value] = object
    total["num"] = c
    total["answer"] = sol_status
    savething = {"num_prob": total["num"], "object_value": total[value], "time": total[time],
                 "status": total["answer"]}
    with open('gurobi_milp_answer_M{}.pickle'.format(c), mode='wb') as fw:
        pickle.dump(savething, fw)
    return total


def test6():
    # 1 = optimap , -1 = Infeasible , 0 = feasible, -2 = unbounded , -3 = 문제정의 x
    load_time = []
    object = []
    sol_status = []
    total = {}
    c = 0
    for i in range(3):
        start_time = time.time()
        filename = "problem{}.pickle".format(i + 1)
        with open(filename, mode='rb') as fr:
            test_instance = pickle.load(fr)
            values = pulp_scheduling(test_instance)
        end_time = time.time()
        loading_time = end_time - start_time
        if values != None:
            load_time.append(loading_time)
            object.append(pulp.value(values.objective))
            sol_status.append(values.status)
        c += 1
    total[time] = load_time
    total[value] = object
    total["num"] = c
    total["answer"] = sol_status
    savething = {"num_prob": total["num"], "object_value": total[value], "time": total[time], "status": total["answer"]}
    with open('pulp_scheduling_answer{}.pickle'.format(c), mode='wb') as fw:
        pickle.dump(savething, fw)
    return total


if __name__ == '__main__':
    cp_or = test1()
    cp = test2()
    milp_or = test3()
    milp = test4()
    goruby = test5()
    pulp = test6()


    #test_instance = generate_prob(numJob=3, numMch=2)
    #schedule = heuristic.scheduling(test_instance, 'SPT')
    #schedule.print_schedule()
    #draw_gantt_chart(schedule, test_instance)

    # schedule = milp_scheduling(test_instance)
    # schedule.print_schedule()
    #draw_gantt_chart(schedule, test_instance)

    # schedule = cp_scheduling(test_instance)
    # schedule = milp_scheduling_ortools(test_instance)
    # schedule = cp_scheduling_ortools(test_instance)
