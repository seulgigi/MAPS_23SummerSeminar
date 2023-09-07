import module
import pickle
import numpy as np
import random
import copy


with open("problem1.pickle", mode='rb') as fr:
    test_instance = pickle.load(fr)
class chrosome:
    def __init__(self, prob : test_instance):
        self.prob = prob
        self.chrosome = []
        self.schedule_list = [[] for _ in range(self.prob.numMch)]
        self.total_time = 0
        for j in np.random.permutation(self.prob.job_list):
            self.chrosome.append([j, random.choice(self.prob.machine_list)])

    def sheduling(self):
        self.schedule_list = [[] for _ in range(self.prob.numMch)]
        for l in self.prob.machine_list:
            for k in range(self.prob.numJob):
                if self.chrosome[k][1] == l:
                    self.schedule_list[l.ID].append(self.chrosome[k][0])
        return self.schedule_list
    def add_totaltime(self):
        for i in self.prob.machine_list:
            start_time = 0
            befo = -1
            for j in self.schedule_list[i.ID]:
                if befo != -1:
                    start_time += self.prob.setup[i.ID][befo][j.ID]
                befo = j.ID
                start_time = start_time + self.prob.ptime[0][j.ID]
            self.total_time += start_time
        return self.total_time

    def mutation(self):  # population : generate_initial_population
        random_job = random.sample(range(0, self.prob.numJob), 2)
        # 작업 위치 변경
        ########## 작업을 변경 ##########
        ex1 = self.chrosome[random_job[0]][0]
        ex2 = self.chrosome[random_job[1]][0]
        self.chrosome[random_job[0]][0] = ex2
        self.chrosome[random_job[1]][0] = ex1
        self.chrosome = self.chrosome
        return self.chrosome

def crossover_operator(population):
    random_chrosmoe_num = random.sample(range(1, len(population)), 2)
    random_ch1 = population[random_chrosmoe_num[0]]
    random_ch2 = population[random_chrosmoe_num[1]]
    random_cut = random.sample(range(0, random_ch1.prob.numJob), 1)
    ex1 = copy.deepcopy(random_ch1)
    ex2 = copy.deepcopy(random_ch2)
    chrosome = ex1.chrosome[random_cut[0]:]
    for i in range(len(ex2.chrosome)):
        if not any(ex2.chrosome[i][0] in sublist for sublist in chrosome): #TODO 같은 job인데 ==에서는 다르다는고 나옴(해결)
            chrosome.append(ex2.chrosome[i])
    ex1.chrosome = chrosome
    return ex1


if __name__ == '__main__':
    with open("problem1.pickle", mode='rb') as fr:
        test_instance = pickle.load(fr)
    population = []
    for i in range(3): # 반복되는 수만큼 유전자 생성
        box = chrosome(test_instance)
        box.schedule_list = box.sheduling()
        box.total_time = box.add_totaltime()
        population.append(box)
        #population.append(generate_initial_population(test_instance))
    population = sorted(population, key=lambda x: x.total_time)


    for i in range(3):  # 반복되는 수만큼 돌연변이 생성
        random_chrosome = copy.deepcopy(population[random.sample(range(1, len(population)), 1)[0]])
        random_chrosome.chrosome = random_chrosome.mutation()
        random_chrosome.schedule_list = random_chrosome.sheduling()
        random_chrosome.total_time = random_chrosome.add_totaltime()
        population.append(random_chrosome)

    population= sorted(population, key=lambda x: x.total_time)[:4]

    for i in range(3):  # 반복되는 수만큼 유전자 조합하여 생성
        crossed_chrosome = crossover_operator(population)
        crossed_chrosome.schedule_list = crossed_chrosome.sheduling()
        crossed_chrosome.total_time = crossed_chrosome.add_totaltime()
        population.append(crossed_chrosome)
    population= sorted(population, key=lambda x: x.total_time)[:4]

