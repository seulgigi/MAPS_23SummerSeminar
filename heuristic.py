from module import *

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