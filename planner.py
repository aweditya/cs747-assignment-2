#! /usr/bin/python
import argparse
parser = argparse.ArgumentParser()
import numpy as np
from pulp import *

class Planner():
    def __init__(self,mdp,algorithm,policy):
        S, A, T, R, gamma = read_mdp(mdp)

        if algorithm == "vi":
            if policy == None:
                V_star, pi_star = vi(S, A, T, R, gamma)
                print_result(V_star, pi_star)
            else:
                policy = read_policy(policy)
                V_pi = policy_eval(S, A, T, R, gamma, policy)
                print_result(V_pi, policy)
        elif algorithm == "hpi":
            if policy == None:
                V_star, pi_star = hpi(S, A, T, R, gamma)
                print_result(V_star, pi_star)
            else:
                policy = read_policy(policy)
                V_pi = policy_eval(S, A, T, R, gamma, policy)
                print_result(V_pi, policy)
        elif algorithm == "lp":
            if policy == None:
                V_star, pi_star = lp(S, A, T, R, gamma)
                print_result(V_star, pi_star)
            else:
                policy = read_policy(policy)
                V_pi = policy_eval(S, A, T, R, gamma, policy)
                print_result(V_pi, policy)
        elif algorithm == "dual_lp":
            if policy == None:
                V_star, pi_star = dual_lp(S, A, T, R, gamma)
                print_result(V_star, pi_star)
            else:
                policy = read_policy(policy)
                V_pi = policy_eval(S, A, T, R, gamma, policy)
                print_result(V_pi, policy)

def read_mdp(path):
    with open(path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            split_line = line.strip().split()
            if split_line[0] == "numStates":
                S = int(split_line[1])
            elif split_line[0] == "numActions":
                A = int(split_line[1])
                R = np.zeros((S, A))
                T = np.zeros((S, A, S))
            elif split_line[0] == "end":
                end_states = list(map(int, split_line[1:]))
            elif split_line[0] == "transition":
                s1 = int(split_line[1])
                a = int(split_line[2])
                s2 = int(split_line[3])
                r = float(split_line[4])
                p = float(split_line[5])
                R[s1, a] += p*r
                T[s1, a, s2] += p
            elif split_line[0] == "mdptype":
                mdptype = split_line[1]
            elif split_line[0] == "discount":
                gamma = float(split_line[1])
    
    return S, A, T, R, gamma

def read_policy(path):
    policy = []
    with open(path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            policy.append(int(line.strip()))

    return policy

def vi(S, A, T, R, gamma):
    V_star = np.zeros(S)
    while(True):
        V_star_next = np.max(R + np.sum(gamma * T * V_star.reshape(1, 1, S), axis=2), axis=1)
        if np.allclose(V_star, V_star_next, rtol=1e-11, atol=1e-8):
            pi_star = np.argmax(R + np.sum(gamma * T * V_star.reshape(1, 1, S), axis=2), axis=1)
            return V_star_next, pi_star
        else:
            V_star = V_star_next

def hpi(S, A, T, R, gamma):
    pi = np.random.randint(0, A, size=S)
    while(True):
        v_pi = policy_eval(S, A, T, R, gamma, pi)
        pi_improved = np.argmax(R + gamma * np.sum(T * v_pi.reshape(1, 1, S), axis=2), axis=1)
        if (pi == pi_improved).all():
            return v_pi, pi
        else:
            pi = pi_improved

def lp(S, A, T, R, gamma):
    V_star = np.zeros(S)

    # Create the LP problem
    prob = LpProblem("Primal", LpMinimize)

    lpVariables = []
    for i in range(S):
        variable = LpVariable(f"V_{i}")
        lpVariables.append(variable)

    # Objective
    prob += lpSum(lpVariables)

    # Constraints
    for s1 in range(S):
        for a in range(A):
            constraint = R[s1, a]
            for s2 in range(S):
                constraint += gamma * T[s1, a, s2] * lpVariables[s2]

            prob += lpVariables[s1] >= constraint

    prob.solve(PULP_CBC_CMD(msg=0))

    for s in range(S):
        V_star[s] = lpVariables[s].varValue

    pi_star = np.argmax(R + np.sum(gamma * T * V_star.reshape(1, 1, S), axis=2), axis=1)
    return V_star, pi_star

def dual_lp(S, A, T, R, gamma):
    pi_star = np.zeros(S)
    prob = LpProblem("Dual", LpMaximize)

    lpVariables = []
    for i in range(S):
        x_i = []
        for k in range(A):
            variable = LpVariable(f"x_{i}^{k}")
            x_i.append(variable)

        lpVariables.append(x_i)

    # Objective
    prob += sum(map(sum, lpVariables * R))
    #print(prob)

    # Constraints
    for j in range(S):
        rhs = 1
        lhs = 0
        for k in range(A):
            for i in range(S):
                rhs += gamma * T[i, k, j] * lpVariables[i][k]

            lhs += lpVariables[j][k] 

        prob += lhs == rhs

    prob.solve(PULP_CBC_CMD(msg=0))

    variableValues = np.array([[lpVariables[i][k].varValue for k in range(A)] for i in range(S)])
    pi_star = np.argmax(variableValues, axis=1)

    return policy_eval(S, A, T, R, gamma, pi_star), pi_star

def policy_eval(S, A, T, R, gamma, policy):
    V_pi = np.linalg.pinv(np.eye(S) - gamma * T[np.arange(S), policy, :]) @ R[np.arange(S), policy]
    return V_pi

def print_result(V, pi):
    for value, action in zip(V, pi):
        print(value, action)

if __name__ == "__main__":
    parser.add_argument("--mdp",type=str,required=True,help="Path to input MDP file")
    parser.add_argument("--algorithm",type=str,choices=["vi", "hpi", "lp", "dual_lp"],default="vi")
    parser.add_argument("--policy",type=str,help="Policy file for which V^pi is to be evaluated (optional)")
    
    args = parser.parse_args()
    
    planner = Planner(args.mdp,args.algorithm,args.policy)
