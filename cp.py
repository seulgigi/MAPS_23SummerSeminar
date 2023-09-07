from module import *
from docplex.cp.model import *
import docplex.cp.utils_visu as visu
import matplotlib.pyplot as plt
from pylab import rcParams
from ortools.sat.python import cp_model
import numpy as np

def cp_scheduling(prob:Instance):
    nbrOfJobs = prob.numJob
    jobs = [*range(0, nbrOfJobs)]
    nbrOfMachines = prob.numMch
    machines = [*range(0, nbrOfMachines)]
    processingTimes = prob.ptime
    setup_matrix = prob.setup

    mdl = CpoModel(name='cp_model')

    processing_itv_vars = [[mdl.interval_var(optional=True, size=processingTimes[m][j], name="interval_job{}_machine{}".format(j, m)) for m in machines] for j in jobs]
    for m in machines:
        for j in jobs:
            print(processing_itv_vars[j][m])

    objective = mdl.sum([mdl.end_of(processing_itv_vars[j][m]) for j in jobs for m in machines])
    mdl.add(mdl.minimize(objective))

    for j in jobs:
        mdl.add(mdl.sum([mdl.presence_of(processing_itv_vars[j][m]) for m in machines]) == 1)

    sequence_vars = [mdl.sequence_var([processing_itv_vars[j][m] for j in jobs], types=[j for j in jobs],
                                      name="sequences_machine{}".format(m)) for m in machines]
    for m in machines:
        mdl.add(mdl.no_overlap(sequence_vars[m], setup_matrix[m]))
    msol = mdl.solve(TimeLimit=3600) #log_output=True
    print("Solution: ")
    msol.print_solution()
    return msol


    """# 그래프 부분
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
    visu.show()"""


def cp_scheduling_ortools(prob:Instance):
    jobs = [*range(0, prob.numJob)]
    machines = [*range(0, prob.numMch)]
    setup_matrix = prob.setup
    processingTimes = prob.ptime
    H = 100000000000000
    """ SJ = range(0, prob.numJob)
        max_s = np.array(setup_matrix).max()
        for i in SJ:
            M = M + max([row[i] for row in processingTimes])
            M = M + max_s
        H = M + max_s"""
    model = cp_model.CpModel()
    presence_vars = [[model.NewBoolVar(name="presence_machine{}_job{}".format(m, j)) for j in jobs] for m in machines]
    start_vars = [[model.NewIntVar(0, H, name="start_machine{}_job{}".format(m, j)) for j in jobs] for m in machines]
    end_vars = [[model.NewIntVar(0, H, name="end_machine{}_job{}".format(m, j)) for j in jobs] for m in machines]
    processing_itv_vars = [
        [model.NewOptionalIntervalVar(start=start_vars[m][j], end=end_vars[m][j], size=processingTimes[m][j],
                                      is_present=presence_vars[m][j], name="interval_machine{}_job{}".format(m, j))
         for j in jobs] for m in machines]
    for m in machines:
        model.AddNoOverlap(processing_itv_vars[m])

    presence_lit = [[[model.NewBoolVar('%i and %i in %i' % (j1, j2, m)) for j2 in jobs] for j1 in jobs] for m in
                    machines]
    precedence = [[[model.NewBoolVar('%i -> %i in %i' % (j1, j2, m)) for j2 in jobs] for j1 in jobs] for m in machines]
    for m in machines:
        for j1 in jobs:
            for j2 in jobs:
                if j1 != j2:
                    lit12 = precedence[m][j1][j2]
                    lit21 = precedence[m][j2][j1]
                    model.Add(start_vars[m][j2] >= end_vars[m][j1] + setup_matrix[m][j1][j2]).OnlyEnforceIf(lit12,
                                                                                                            presence_vars[m][j1],presence_vars[m][j2])
                    model.Add(start_vars[m][j1] >= end_vars[m][j2] + setup_matrix[m][j2][j1]).OnlyEnforceIf(lit21,presence_vars[m][j1],presence_vars[m][j2])
                    model.AddBoolOr(lit12, lit21, presence_vars[m][j1].Not(), presence_vars[m][j2].Not())
    for j in jobs:
        alt_intvs = []
        for m in machines:
            alt_intvs.append(presence_vars[m][j])
        model.Add(cp_model.LinearExpr.Sum(alt_intvs) == 1)

    objective = cp_model.LinearExpr.Sum([end_vars[m][j] for j in jobs for m in machines])
    model.Minimize(objective)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 3600
    # solver.parameters.enumerate_all_solutions = True
    solver.parameters.log_search_progress = True
    status = solver.Solve(model)
    if status in [cp_model.OPTIMAL] :
        return [solver , "OPTIMAL"]
    elif status in [cp_model.FEASIBLE] :
        return [solver, "FEASIBLE"]
    else:
        return [solver, "no"]


