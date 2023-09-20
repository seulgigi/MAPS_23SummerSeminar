import random
import pickle
import gurobipy as grb
import numpy as np
from module import Instance


def gurobi_milp(prob:Instance, opt_model=None):

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

    opt_model = grb.Model(name="MIP Model")

    #결정변수
    C_i = {i: opt_model.addVar(vtype=grb.GRB.CONTINUOUS,lb=0,name="C_{0}".format(i)) for i in SJ}
    C_ik = {(i, k): opt_model.addVar(vtype=grb.GRB.CONTINUOUS,lb=0,name="C_{0}_{1}".format(i, k)) for i in SJ for k in SM}
    S_ik = {(i, k): opt_model.addVar(vtype=grb.GRB.CONTINUOUS, lb=0, name="S_{0}_{1}".format(i, k)) for i in SJ for k in SM}
    y_ik = {(i, k): opt_model.addVar(vtype=grb.GRB.BINARY, name="y_{0}_{1}".format(i, k))for i in SJ for k in SM}
    z_ijk = {(i,j,k): opt_model.addVar(vtype=grb.GRB.BINARY, name="z_{0}_{1}_{2}".format(i,j,k)) for i in SJ for j in SJ for k in SM if i<j}

    #제약조건
    constraint_1 = {(i, k): opt_model.addConstr(lhs=(C_ik[i, k] + S_ik[i,k]),sense=grb.GRB.LESS_EQUAL,rhs=M * y_ik[i, k],
            name="constraint1_{0}_{1}".format(i, k)) for i in SJ for k in SM}
    constraint_2 = {(i, k): opt_model.addConstr(lhs=(C_ik[i, k] ),sense=grb.GRB.GREATER_EQUAL, rhs=S_ik[i, k] + p[k][i] - M * (1 - y_ik[i, k]),
            name="constraint2_{0}_{1}".format(i, k)) for i in SJ for k in SM}
    constraint_3 = {(i, j, k): opt_model.addConstr(lhs=(S_ik[i, k] ), sense=grb.GRB.GREATER_EQUAL, rhs=C_ik[j, k] + s[k][j][i]*y_ik[j, k] - M2*z_ijk[i, j, k],
                                                name="constraint3_{0}_{1}_{2}".format(i, j, k)) for k in SM for i in SJ for j in SJ if i < j}
    constraint_4 = {(i, j, k): opt_model.addConstr(lhs=(S_ik[j, k]), sense=grb.GRB.GREATER_EQUAL,
                                    rhs=C_ik[i, k] + s[k][i][j]*y_ik[i,k] - M2*(1 - z_ijk[i,j,k]), name="constraint4_{0}_{1}_{2}".format(i, j, k)) for k in SM for i in SJ for j in SJ if i < j}
    constraint_5 = {i :opt_model.addConstr(lhs=grb.quicksum(y_ik[i, k] for k in SM),sense=grb.GRB.EQUAL,rhs=1,name="constraint5_{0}".format(i)) for i in SJ}
    constraint_6 = {i: opt_model.addConstr(lhs=grb.quicksum(C_ik[i, k] for k in SM),sense=grb.GRB.LESS_EQUAL, rhs=C_i[i], name="constraint6_{0}".format(i)) for i in SJ}

    #목적함수
    objective = grb.quicksum(C_i[i] for i in SJ)

    opt_model.ModelSense = grb.GRB.MINIMIZE
    opt_model.setObjective(objective)
    opt_model.setParam('TimeLimit', 3600)
    opt_model.optimize()

    return opt_model



