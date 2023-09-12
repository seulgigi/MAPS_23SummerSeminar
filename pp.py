import numpy as np
from pulp import LpProblem, LpMinimize, LpBinary, LpInteger, LpConstraint

from module import *
import pulp as pl


def pulp_scheduling(prob:Instance):
    SJ = range(0, prob.numJob)
    SM = range(0, prob.numMch)
    s = prob.setup
    p = prob.ptime
    M = 0
    max_s = np.array(s).max()
    for i in SJ:
        M = M + max([row[i] for row in p])
        M = M + max_s
    M2 = M + max_s
    model = LpProblem("pulp_model", LpMinimize)

    # 결정변수
    C_i = {i: pl.LpVariable(name=f'C_{i}', lowBound=0, cat=pl.LpContinuous) for i in SJ}
    C_ik = {(i, k): pl.LpVariable(name=('C_' + str(i) + '_' + str(k)), lowBound=0, cat=pl.LpContinuous) for i in SJ for k in SM}
    S_ik = {(i, k): pl.LpVariable(name=('S_' + str(i) + '_' + str(k)), lowBound=0, cat=pl.LpContinuous) for i in SJ for k in SM}
    y_ik = {(i, k): pl.LpVariable(name=('Y_' + str(i) + '_' + str(k)), lowBound=0, cat=pl.LpBinary) for i in SJ for k in SM}
    z_ijk = {(i, j, k): pl.LpVariable(name=('Z_' + str(i) + '_' + str(j) + '_' + str(k)), lowBound=0, cat=pl.LpBinary) for i in SJ for j in SJ for k
             in SM if i < j}

    for i in SJ:
        for k in SM:
            model += C_ik[i, k] + S_ik[i, k] <= M * y_ik[i, k], f"constraint_1_{i}_{k}"
            model += C_ik[i, k] >= S_ik[i, k] + p[k][i] - M * (1 - y_ik[i, k]), f"constraint_2_{i}_{k}"

    for i in SJ:
        for j in SJ:
            for k in SM:
                if i < j:
                    model += S_ik[i, k] >= C_ik[j, k] + s[k][j][i] * y_ik[j, k] - M2 * z_ijk[
                        i, j, k], f"constraint_3_{i}_{j}_{k}"
                    model += S_ik[j, k] >= C_ik[i, k] + s[k][i][j] * y_ik[i, k] - M2 * (
                                1 - z_ijk[i, j, k]), f"constraint_4_{i}_{j}_{k}"

    for i in SJ:
        model += pl.lpSum(y_ik[i, k] for k in SM) == 1, f"constraint_5_{i}"

    for i in SJ:
        model += pl.lpSum(C_ik[i, k] for k in SM) <= C_i[i], f"constraint_6_{i}"

    model += pl.lpSum(C_i[i] for i in SJ)
    solver = pl.getSolver('PULP_CBC_CMD', timeLimit=10)

    result = model.solve(solver)

    return result