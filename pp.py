from pulp import LpProblem, LpMinimize, LpBinary, LpInteger, LpConstraint

from module import *
from docplex.cp.model import *
import pulp as pl


def pulp_scheduling(prob:Instance):
    nbrOfJobs = prob.numJob
    jobs = [*range(0, nbrOfJobs)]
    nbrOfMachines = prob.numMch
    machines = [*range(0, nbrOfMachines)]
    processingTimes = prob.ptime
    setup_matrix = prob.setup

    mdl = LpProblem("pulp_model", LpMinimize)

    processing_itv_vars = [[pl.LpVariable(f"interval_job{j}_machine{m}", cat=pl.LpContinuous, lowBound=0) for m in machines] for j in jobs]
    for m in machines:
        for j in jobs:
            print(processing_itv_vars[j][m])

    objective = pl.lpSum([pl.lpSum(processing_itv_vars[j][m] for m in machines) for j in jobs])
    mdl += objective, "Objective"

    for j in jobs:
        mdl += pl.lpSum(processing_itv_vars[j][m] for m in machines) == 1, "Job_{}".format(j)

    sequence_vars = [pl.LpVariable("sequences_machine{}".format(m), lowBound=0, cat=pl.LpInteger) for m in machines]

    for m in machines:
        mdl += pl.lpSum(processing_itv_vars[j][m] * j for j in jobs) >= sequence_vars[m], "No_Overlap_{}".format(m)

    mdl.solve()
    if pl.LpStatus[mdl.status] == 'Optimal':
        print("Solution:")
        for j in jobs:
            for m in machines:
                if pl.value(processing_itv_vars[j][m]) == 1:
                    print("Job {} is scheduled on Machine {}".format(j, m))
    else:
        print("No optimal solution found.")

    return mdl



def pp_scheduling_ortools(prob:Instance):
    jobs = [*range(0, prob.numJob)]
    machines = [*range(0, prob.numMch)]
    setup_matrix = prob.setup
    processingTimes = prob.ptime
    H = 100000000000000

    model = pl.LpProblem("pulp_model", pl.LpMinimize)
    presence_vars = pl.LpVariable.dicts("presence", [(m, j) for m in machines for j in jobs], cat=pl.LpBinary)
    start_vars = pl.LpVariable.dicts("start", [(m, j) for m in machines for j in jobs], lowBound=0, upBound=H, cat=pl.LpInteger)
    end_vars = pl.LpVariable.dicts("end", [(m, j) for m in machines for j in jobs], lowBound=0, upBound=H, cat=pl.LpInteger)

    for m in machines:
        for j1 in jobs:
            for j2 in jobs:
                if j1 != j2:
                    model += start_vars[(m, j2)] >= end_vars[(m, j1)] + setup_matrix[m][j1][j2] - H * (1 - presence_vars[(m, j1)]) - H * (1 - presence_vars[(m, j2)])

    for j in jobs:
        model += pl.lpSum(presence_vars[(m, j)] for m in machines) == 1

    objective = pl.lpSum(end_vars[(m, j)] for m in machines for j in jobs)
    model += objective

    model.solve()

    if pl.LpStatus[model.status] == "Optimal":
        return [pl, "OPTIMAL"]
    elif pl.LpStatus[model.status] == "Feasible":
        return [pl, "FEASIBLE"]
    else:
        return [pl, "no"]