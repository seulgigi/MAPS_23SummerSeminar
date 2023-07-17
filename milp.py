from module import *
from docplex.mp.model import Model
from ortools.linear_solver import pywraplp

def milp_scheduling(prob:Instance):
    SJ = range(0, prob.numJob)
    SM = range(0, prob.numMch)
    H = 10000000
    M = 10000000
    s = prob.setup
    p = prob.ptime
    u = {(i, k): 1 for i in SJ for k in SM}

    model = Model(name='PMSP')

    # 결정변수
    C_k = {k: model.continuous_var(lb=0, name='C_' + str(k)) for k in SM}
    x_i = {i: model.continuous_var(lb=0, name='x_' + str(i)) for i in SJ}
    y_ik = {(i, k): model.binary_var(name='y_' + str(i) + '_' + str(k)) for i in SJ for k in SM}
    z_ijk = {(i, j, k): model.binary_var(name='z_' + str(i) + '_' + str(j) + '_' + str(k)) for i in SJ for j in SJ for k in SM}

    constraint_2 = {(i, j): model.add_constraint(
        ct=model.sum(model.sum(p[k][i]*y_ik[i, k]+s[k][h][i] * z_ijk[h, i, k] for h in SJ) for k in SM) + x_i[i] <= x_i[j] + M*(1-model.sum(z_ijk[i, j, k] for k in SM)),
        ctname="constraint_2_{0}_{1}".format(i, j)) for i in SJ for j in SJ if i != j}

    constraint_3 = {(i, k): model.add_constraint(
        ct=model.sum(s[k][h][i] * z_ijk[h, i, k] for h in SJ) + p[k][i] * y_ik[i, k] + x_i[i] <= C_k[k] + M*(1-y_ik[i, k]),
        ctname="constraint_3_{0}_{1}".format(i, k)) for i in SJ for k in SM}

    constraint_4 = {(i): model.add_constraint(
        ct=model.sum(u[i, k] * y_ik[i, k] for k in SM) == 1,
        ctname="constraint_4_{0}".format(i)) for i in SJ}

    constraint_5 = {(i): model.add_constraint(
        ct=model.sum(y_ik[i, k] for k in SM) == 1,
        ctname="constraint_5_{0}".format(i)) for i in SJ}

    constraint_6 = {(k): model.add_constraint(
        ct=model.sum(z_ijk[i, i, k] for i in SJ) <= 1,
        ctname="constraint_6_{0}".format(k)) for k in SM}

    constraint_7 = {(i, k): model.add_constraint(
        ct=model.sum(z_ijk[j, i, k] for j in SJ) == y_ik[i, k],
        ctname="constraint_7_{0}_{1}".format(i, k)) for i in SJ for k in SM}

    constraint_8 = {(i, k): model.add_constraint(
        ct=model.sum(z_ijk[i, j, k] for j in SJ if i != j) <= y_ik[i, k],
        ctname="constraint_8_{0}_{1}".format(i, k)) for i in SJ for k in SM}

    # Redundant
    constraint_9 = {(i): model.add_constraint(
        ct=x_i[i] >= 0,
        ctname="constraint_9_{0}".format(i)) for i in SJ}

    # Redundant
    constraint_10 = {(k): model.add_constraint(
        ct=C_k[k] <= H,
        ctname="constraint_10_{0}".format(k)) for k in SM}

    # 목적함수 (1)
    model.minimize(model.sum(C_k[k] for k in SM))

    model.set_time_limit(500)
    result = model.solve(log_output=True)

    print('Scheduling is done.')


def milp_scheduling_ortools(prob:Instance):
    solver = pywraplp.Solver.CreateSolver('SCIP')

    due_dates = prob.job_list[:].due
    proc_times = prob.ptime
    intervals = []
    start_variables = []
    end_variables = []
    early_variables = []
    tardy_variables = []
    total_tardiness = []

    num_jobs = prob.numJob

    infinity = solver.infinity()
    X = []
    C = []
    T = []
    for i in range(num_jobs):
        x_temp = []
        ### 여기까지 해결
        for j in range(num_jobs):
            x_temp.append(solver.IntVar(0.0, 1.0, 'X_' + str(i + 1) + '_' + str(j + 1)))
        X.append(x_temp)
        C.append(solver.NumVar(0, infinity, 'C_' + str(i + 1)))
        T.append(solver.NumVar(0, infinity, 'T_' + str(i + 1)))

    # Add Constraints Here
    for i in range(num_jobs):
        for j in range(num_jobs):
            if i is not j:
                solver.Add(X[i][j] + X[j][i] == 1)

    for i in range(num_jobs):
        solver.Add(C[i] >= proc_times[i])

    for i in range(num_jobs):
        for j in range(num_jobs):
            if i is not j:
                solver.Add(C[i] - C[j] + X[i][j] * 10000 >= proc_times[i])

    for i in range(num_jobs):
        solver.Add(T[i] >= C[i] - due_dates[i])

    solver.Minimize(sum(T))
    solver.EnableOutput()
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('Solution:')
        print('Objective value =', solver.Objective().Value())