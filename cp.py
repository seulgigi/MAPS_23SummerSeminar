from module import *
from docplex.cp.model import *
import docplex.cp.utils_visu as visu
import matplotlib.pyplot as plt
from pylab import rcParams

def cp_scheduling(prob:Instance):
    nbrOfJobs = prob.numJob
    jobs = [*range(0, nbrOfJobs)]
    nbrOfMachines = prob.numMch
    machines = [*range(0, nbrOfMachines)]
    processingTimes = prob.ptime
    setup_matrix = prob.setup

    mdl = CpoModel(name='cp_model')

    processing_itv_vars = [
        [mdl.interval_var(optional=True, size=processingTimes[m][j], name="interval_job{}_machine{}".format(j, m)) for m
         in machines] for j in jobs]
    for m in machines:
        for j in jobs:
            print(processing_itv_vars[j][m])

    objective = mdl.max([mdl.end_of(processing_itv_vars[j][m]) for j in jobs for m in machines])
    mdl.add(mdl.minimize(objective))

    for j in jobs:
        mdl.add(mdl.sum([mdl.presence_of(processing_itv_vars[j][m]) for m in machines]) == 1)

    sequence_vars = [mdl.sequence_var([processing_itv_vars[j][m] for j in jobs], types=[j for j in jobs],
                                      name="sequences_machine{}".format(m)) for m in machines]
    for m in machines:
        mdl.add(mdl.no_overlap(sequence_vars[m], setup_matrix[m]))

    msol = mdl.solve(log_output=True)
    print("Solution: ")
    msol.print_solution()

    # 그래프 부분
    rcParams['figure.figsize'] = 25, 5
    seq = [*range(0, nbrOfMachines)]
    job_id = dict()
    for m in machines:
        for j in jobs:
            job_id[processing_itv_vars[j][m].get_name()] = j
        seq[m] = msol.get_var_solution(sequence_vars[m])
        visu.sequence(name=sequence_vars[m].get_name())
        vs = seq[m].get_value()
        for v in vs:
            nm = v.get_name()
            visu.interval(v, 'lightgreen', 'J' + str(job_id[nm]))
        for j in range(len(vs) - 1):
            end = vs[j].get_end()
            j1 = job_id[vs[j].get_name()]
            j2 = job_id[vs[j + 1].get_name()]
            visu.transition(end, end + setup_matrix[m][j1][j2])
    visu.show()


def cp_scheduling_ortools(prob:Instance):
    pass