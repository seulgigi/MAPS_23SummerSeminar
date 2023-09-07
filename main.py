from module import *
from milp import *
from cp import *
import heuristic
import random
import time
import multiprocessing
import pickle
import pandas as pd
from schedule import Schedule, Bar
import matplotlib.pyplot as plt

def test1():
    fo = -1
    load_time = []
    object = []
    sol_status = []
    total = {}
    c = 0
    for i in range(32):
        start_time = time.time()
        filename = "problem{}.pickle".format(i + 1)
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
    with open('cp_scheduling_ortools_answer{}.pickle'.format(c), mode='wb') as fw:
        pickle.dump(savething, fw)
    return total
def test2():
    fo = -1
    load_time = []
    object = []
    sol_status = []
    total = {}
    c = 0
    for i in range(32):
        start_time = time.time()
        filename = "problem{}.pickle".format(i + 1)
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
    with open('cp_scheduling_answer{}.pickle'.format(c), mode='wb') as fw:
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
    for i in range(32):
        fo = -1 # 상태를 확인하기위한 변수
        start_time = time.time()
        filename = "problem{}.pickle".format(i + 1)
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
    with open('milp_scheduling_ortools_answer{}.pickle'.format(c), mode='wb') as fw:
        pickle.dump(savething, fw)
    return total
def test4():
    load_time = []
    object = []
    sol_status = []
    total = {}
    c = 0
    for i in range(32):
        start_time = time.time()
        filename = "problem{}.pickle".format(i + 1)
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
    with open('milp_scheduling_answer{}.pickle'.format(c), mode='wb') as fw:
        pickle.dump(savething, fw)
    return total


class Machine:
    type = 'Unrelated PMSP with SDST'

    def __init__(self, _id: int):
        self.ID = _id  # instance variable unique to each instance
        self.available = 0  # 작업이 가능한 시점
        self.assigned = []  # machine에 할당된 job list

    def __repr__(self):
        return 'Machine ' + str(self.ID)


class Instance:
    type = 'Unrelated PMSP with SDST'

    def __init__(self, jobs: list, mchs: list, ptime, setups):
        self.numJob = len(jobs)
        self.numMch = len(mchs)
        self.job_list = jobs
        self.machine_list = mchs
        self.ptime = ptime  # 프로세스 타임
        self.setup = setups  # 셋업 타임

    def getPTime(self, job: Job, machine: Machine):
        return self.ptime[machine.ID][job.ID]  # add time return code

    def getSetup(self, job_i: Job, job_j: Job, machine: Machine):
        return self.setup[machine.ID][job_i.ID][job_j.ID]



def generate_prob(numJob, numMch) -> Instance:
    job_list = []
    machine_list = []
    jobs = [*range(0, numJob)]
    machines = [*range(0, numMch)]

    job_list += [Job(i) for i in jobs]
    machine_list += [Machine(i) for i in machines]
    ptimes = [[random.randint(10, 40) for j in jobs] for m in machines]
    setup_matrix = [*range(0, numMch)]
    for m in machines:
        for j in jobs:
            job_list[j].due = random.randint(10, 40)
            for j in jobs:
                setup_matrix[m] = [[random.randint(6, 15) for j in jobs] for j in jobs]

    return Instance(job_list, machine_list, ptimes, setup_matrix)


def scheduling(prob:Instance, alg:str) -> Schedule:
    schedule_list = [[] for _ in range(prob.numMch)]

    if alg == 'EDD':  # 납기일이 빠른 순서대로 스케줄링
        sorted_job = sorted(prob.job_list, key=lambda j: j.due)
        # # 작업 종료 시간(납기일)을 기준으로 오름차순 정렬

        for j in sorted_job:
            selected_machine = min(prob.machine_list, key=lambda m: m.available)
            # machine의 이전 작업이 끝나는 시간, 즉 end가 빠른 machine을 선택

            schedule_list[selected_machine.ID].append(match_job_bar(prob, selected_machine, j))

    elif alg == 'SPT':
        schedule_list = solve_SPT(schedule_list, prob)


    print('Scheduling is done.')
    return Schedule('SPT', prob, schedule_list)

def solve_SPT(schedule_list: list, prob: Instance) -> list:
    sorted_job = []
    first_job_list = []
    count = 0

    for m in prob.machine_list:
        sorted_job.append(sorted(prob.job_list, key=lambda j: prob.getPTime(j, m)))
        first_job_list.append(sorted_job[m.ID][0])

    print(first_job_list)

    while len(set(first_job_list)) <= prob.numMch - 1:
        count += 1
        duplicate_job = list(set([x for x in first_job_list if first_job_list.count(x) > 1]))
        for j in duplicate_job:
            duplicate_machine = [m for i, m in enumerate(prob.machine_list) if i in [j for j, job in enumerate(first_job_list) if job in duplicate_job]]
            min_machine = min(duplicate_machine, key=lambda m: prob.getPTime(j, m))
            for m in duplicate_machine:
                if m != min_machine:
                    first_job_list[m.ID] = sorted_job[m.ID][count]
            print(first_job_list)

    for m, j in zip(prob.machine_list, first_job_list):
        schedule_list[m.ID].append(match_job_bar(prob, m, j))

    while True:
        selected_machine = min(prob.machine_list, key=lambda m: m.available)
        for j in sorted_job[selected_machine.ID]:
            if j.complete == False:
                schedule_list[selected_machine.ID].append(match_job_bar(prob, selected_machine, j))
                break

        if all(j.complete for j in prob.job_list):
            break
    return schedule_list

def match_job_bar(prob: Instance, machine: Machine, job: Job) -> Bar:
    job_setup = 0
    if len(machine.assigned) == 0:
        job.start = machine.available
    else:
        job_setup = prob.getSetup(machine.assigned[-1], job, machine)
        job.start = machine.available + job_setup
        # selected_machine에 이전 작업에서 현재 작업으로의 setuptime을 더함

    job.end = job.start + prob.getPTime(job, machine)
    # 작업 종료 시간 설정

    job.assignedMch = machine.ID
    # job 지정된 machine의 번호 저장

    job.complete = True

    machine.available = job.end
    # 기계의 다음 작업 시작 시간

    machine.assigned.append(job)
    # 기계에 할당된 작업 추가

    return Bar(job, job_setup)

def draw_gantt_chart(schedule: Schedule, prob: Instance):
    plt.figure(figsize=(25, 5))

    # 각각의 스케줄 가져오기
    for machine_id, bars in enumerate(schedule.schedule):
        # 기계 선정
        machine = prob.machine_list[machine_id]
        # 이전 끝난 시간
        prev_end = 0
        # 기계에서 작업가져오기
        for i, bar in enumerate(bars):
            job = bar.job
            # setup time 계산
            setup_time = prob.getSetup(machine.assigned[-1], job, machine) if machine.assigned else 0
            # 차트 그리기
            if prev_end == 0:
                plt.barh(machine_id, bar.end - bar.start, left=prev_end, height=1,label=f'Job {job.ID}', alpha=0.4)
            else:
                plt.barh(machine_id, bar.end - bar.start, left=prev_end+setup_time, height=1, label=f'Job {job.ID}', alpha=0.4)
                plt.barh(machine_id, setup_time, left=prev_end, height=0.5, color='gray', alpha=0.2)
            # 다시 시작할 시간 설정
            prev_end = bar.end
    # 그래프 그리기
    plt.xlabel('Time')
    plt.ylabel('Machine')
    plt.yticks(range(prob.numMch), [f'Machine {i}' for i in range(prob.numMch)])
    plt.title('Gantt Chart')
    plt.legend(loc='upper right')

    # Show the chart
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    cp_or = test1()
    cp = test2()
    milp_or = test3()
    milp = test4()



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
    test_instance = generate_prob(numJob=10, numMch=5)
    schedule = scheduling(test_instance, 'SPT')
    schedule.print_schedule()
    draw_gantt_chart(schedule, test_instance)
