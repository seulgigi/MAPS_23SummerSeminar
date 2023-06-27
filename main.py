import random
from schedule import *

class Job:
    type = 'Unrelated PMSP with SDST'  # class variable shared by all instances

    def __init__(self, _id: int):
        self.ID = _id  # instance variable unique to each instance
        self.complete = False
        self.start = -1  # 작업의 시작 시간
        self.end = -1  # 작업이 끝나는 시간
        self.assignedMch = -1
        self.due = -1

    def __repr__(self):
        return 'Job ' + str(self.ID)


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
    if alg == 'EDD':  # 납기일이 빠른 순서대로 스케줄링
        sorted_job = sorted(prob.job_list, key=lambda j: j.due)
        # # 작업 종료 시간(납기일)을 기준으로 오름차순 정렬

        for j in sorted_job:
            selected_machine = min(prob.machine_list, key=lambda m: m.available)
            # machine의 이전 작업이 끝나는 시간, 즉 end가 빠른 machine을 선택

            if len(selected_machine.assigned) == 0:
                j.start = selected_machine.available
            else:
                j.start = selected_machine.available + prob.getSetup(selected_machine.assigned[-1], j, selected_machine)
                # selected_machine에 이전 작업에서 현재 작업으로의 setuptime을 더함

            j.end = j.start + prob.getPTime(j, selected_machine)
            # 작업 종료 시간 설정

            j.assignedMch = selected_machine.ID
            # job 지정된 machine의 번호 저장

            selected_machine.available = j.end
            # 기계의 다음 작업 시작 시간

            selected_machine.assigned.append(j)
            # 기계에 할당된 작업 추가

        for m in prob.machine_list:
            print(m.assigned)


    print('Scheduling is done.')


if __name__ == '__main__':
    test_instance = generate_prob(numJob=10, numMch=5)
    schedule = scheduling(test_instance, 'EDD')
