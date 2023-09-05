import module
import pickle
import numpy as np
import random
import copy

with open("problem1.pickle", mode='rb') as fr:
    test_instance = pickle.load(fr)
def generate_initial_population(prob:test_instance):
    chrosome =[]
    schedule_list = [[] for _ in range(prob.numMch)]
    total_time = 0
    ########## 작업순서를 무작위로 정렬하고 기계에 부여 ##########
    for j in np.random.permutation(prob.job_list):
        chrosome.append([j,random.choice(prob.machine_list)])

    ########## 스케줄링 하는 부분 ##########
    for l in prob.machine_list :
        for k in range(prob.numJob):
            if chrosome[k][1] == l:
                schedule_list[l.ID].append(chrosome[k][0])

    ########## 총시간계산 하는 부분 ##########
    for i in prob.machine_list:
        start_time = 0
        befo =-1
        for j in schedule_list[i.ID]:
            befo = j.ID
            start_time = start_time + prob.ptime[0][j.ID]
            if befo != -1 :
                start_time += prob.setup[i.ID][befo][j.ID]
        total_time += start_time
    chrosome.insert(0, total_time)
    return chrosome
def mutation(population : generate_initial_population, prob:test_instance):
    total_time = 0
    chrosome = []
    # 랜덤으로 바꿀값 선택하는 부분
    ########## 작업번호및 유전자 랜덤 선택 하는 부분 ##########
    random_chrosmoe = random.sample(range(1, len(population)), 1)
    random_job = random.sample(range(1, prob.numJob+1), 2)
    test = copy.deepcopy(population[random_chrosmoe[0]])
    # 작업 위치 변경
    ########## 작업을 변경 ##########
    ex1 = test[random_job[0]][0] #TODO 디버그는 되는데 실행은 안됨?
    ex2 = test[random_job[1]][0]
    test[random_job[0]][0] = ex2
    test[random_job[1]][0] = ex1

    ########## 스케줄링 하는 부분 ##########
    schedule_list = [[] for _ in range(prob.numMch)] # 다시 스케줄링
    for l in prob.machine_list : #스케줄리스트에 추가하는 코드
        for k in range(prob.numJob):
            if test[k+1][1].ID == l.ID:
                schedule_list[l.ID].append(test[k+1][0])


    ########## 총시간계산 하는 부분 ##########
    for i in prob.machine_list: # 시간 계산
        start_time = 0
        befo =-1
        for j in schedule_list[i.ID]:
            befo = j.ID
            start_time = start_time + prob.ptime[0][j.ID]
            if befo != -1 :
                start_time += prob.setup[i.ID][befo][j.ID]
        total_time += start_time
    test[0] = total_time
    chrosome.append(test)
    return chrosome
    print("THE END")

def crossover_operator(population: generate_initial_population, prob: test_instance):
    chrosome=[]
    total_time = 0
    ########## 유전자 2개및 나눌부분 랜덤 선택 하는 부분 ##########
    random_chrosmoe = random.sample(range(1, len(population)), 2)
    random_cut = random.sample(range(1, prob.numJob + 1), 1)
    ex1 = copy.deepcopy(population[random_chrosmoe[0]][1:])
    ex2 = copy.deepcopy(population[random_chrosmoe[1]][1:])
    chrosome = ex1[random_cut[0]:]
    for i in range(len(ex2)):
        if not any(ex2[i][0] in sublist for sublist in chrosome): #TODO 같은 job인데 ==에서는 다르다는고 나옴(해결)
            chrosome.append(ex2[i])

    ########## 스케줄링 하는 부분 ##########
    schedule_list = [[] for _ in range(prob.numMch)]  # 다시 스케줄링
    for l in prob.machine_list:  # 스케줄리스트에 추가하는 코드
        for k in range(prob.numJob):
            if chrosome[k][1].ID == l.ID:
                schedule_list[l.ID].append(chrosome[k][0])

    ########## 총시간계산 하는 부분 ##########
    for i in prob.machine_list:  # 시간 계산
        start_time = 0
        befo = -1
        for j in schedule_list[i.ID]:
            befo = j.ID
            start_time = start_time + prob.ptime[0][j.ID]
            if befo != -1:
                start_time += prob.setup[i.ID][befo][j.ID]
        total_time += start_time
    chrosome.insert(0, total_time)
    return chrosome

if __name__ == '__main__':
    population = []
    for i in range(3): # 반복되는 수만큼 유전자 생성
        population.append(generate_initial_population(test_instance))
    population = sorted(population, key=lambda x: x[0])
    mutation(population,test_instance) # 확인용 나중에 지워야함
    crossover_operator(population, test_instance) # 코드 확인용 나중에 지워야함

    for i in range(3): # 반복되는 수만큼 돌연변이 생성
        chrosome = mutation(population, test_instance)
        population.append(chrosome)
    population= sorted(population, key=lambda x: x[0])[:20]

    for i in range(3):  # 반복되는 수만큼 유전자 조합하여 생성
        crossover_operator(population, test_instance)
    population= sorted(population, key=lambda x: x[0])[:20]

