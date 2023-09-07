import random
import matplotlib.pyplot as plt

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

    def __eq__(self, other):
        if isinstance(other, Job):
            if (other.ID== self.ID) and (other.due== self.due):
                return True
        return False
#TODO 어떻게 코드를 쓰는 것인지는 모르겠습니다.

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

class Schedule:
    def __init__(self, _alg: str, instance, schedule_list: list):
        self.algorithm = _alg
        self.instance = instance
        self.schedule = schedule_list

    def print_schedule(self):
        for m in self.schedule:
            print(m)


class Bar:
    def __init__(self, job, setup: int):
        self.seq = job.ID
        self.job = job
        self.machine = job.assignedMch
        self.start = job.start
        self.end = job.end
        self.setup = setup

    def __repr__(self):

        return 'Bar ' + str(self.seq)

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

def generate_prob(numJob, numMch) -> Instance:
    H = 1000  # 임의로 설정 하였지만 나중에 받아오는 형식
    pmax = H/(numJob/numMch)
    job_list = []
    machine_list = []
    jobs = [*range(0, numJob)]
    machines = [*range(0, numMch)]

    job_list += [Job(i) for i in jobs]
    machine_list += [Machine(i) for i in machines]
    ptimes = [[random.randint(round(pmax*0.6), round(pmax)) for j in jobs] for m in machines]
    setup_matrix = [*range(0, numMch)]
    for m in machines:
        for j in jobs:
            job_list[j].due = random.randint(10, 40)
            for j in jobs:
                setup_matrix[m] = [[random.randint(round(0.05*ptimes[m][j]*2), round(0.1*ptimes[m][j]*2)) for j in jobs] for j in jobs]
    # random.uniform(0.5,1.5)
    return Instance(job_list, machine_list, ptimes, setup_matrix)


