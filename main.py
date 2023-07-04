import random
from schedule import Schedule, Bar

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
    schedule_list = [[] for _ in range(prob.numMch)]

    if alg == 'EDD':  # 납기일이 빠른 순서대로 스케줄링
        sorted_job = sorted(prob.job_list, key=lambda j: j.due)
        # # 작업 종료 시간(납기일)을 기준으로 오름차순 정렬

        for j in sorted_job:
            selected_machine = min(prob.machine_list, key=lambda m: m.available)
            # machine의 이전 작업이 끝나는 시간, 즉 end가 빠른 machine을 선택

            schedule_list[selected_machine.ID].append(match_job_bar(prob, selected_machine, j))

    print('Scheduling is done.')
    return Schedule('EDD', prob, schedule_list)

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
    machine.available = job.end
    # 기계의 다음 작업 시작 시간
    machine.assigned.append(job)
    # 기계에 할당된 작업 추가

    return Bar(job, job_setup)

if __name__ == '__main__':
    test_instance = generate_prob(numJob=10, numMch=5)
    schedule = scheduling(test_instance, 'EDD')
    schedule.print_schedule()

import matplotlib.pyplot as plt


def draw_gantt_chart(schedule: Schedule, prob: Instance):
    plt.figure(figsize=(25, 5))

    # 각각의 스케줄 가져오기
    for machine_id, sch in enumerate(schedule.schedule):
        t=0
        # 기계 선정
        machine = prob.machine_list[machine_id]
        # 이전 끝난 시간
        prev_end = 0
        # 기계에서 작업가져오기
        for i, bar in enumerate(sch):
            job = bar.job
            # setup time 계산
            setup_time = prob.getSetup(machine.assigned[t-1], job, machine) if machine.assigned else 0
            t+=1
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

draw_gantt_chart(schedule, test_instance)