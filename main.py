import random
from schedule import *

class Job:
    type = 'Unrelated PMSP with SDST'  # class variable shared by all instances

    def __init__(self, _id: int):
        self.ID = _id  # instance variable unique to each instance
        self.complete = False
        self.start = -1
        self.end = -1
        self.assignedMch = -1

    def __repr__(self):
        return 'Job ' + str(self.ID)


class Machine:
    type = 'Unrelated PMSP with SDST'

    def __init__(self, _id: int):
        self.ID = _id  # instance variable unique to each instance
        self.available = 0
        self.assigned = []

    def __repr__(self):
        return 'Machine ' + str(self.ID)


class Instance:
    type = 'Unrelated PMSP with SDST'

    def __init__(self, jobs: list, mchs: list, ptime, setups):
        self.numJob = len(jobs)
        self.numMch = len(mchs)
        self.job_list = jobs
        self.machine_list = mchs
        self.ptime = ptime
        self.setup = setups

    def getPTime(self, job: Job, machine: Machine):
        pass

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
            for j in jobs:
                setup_matrix[m] = [[random.randint(6, 15) for j in jobs] for j in jobs]

    return Instance(job_list, machine_list, ptimes, setup_matrix)


def scheduling(prob:Instance, alg:str) -> Schedule:
    if alg == 'EDD':
        pass
    print('Scheduling is done.')


if __name__ == '__main__':
    test_instance = generate_prob(numJob=10, numMch=5)
    schedule = scheduling(test_instance)
