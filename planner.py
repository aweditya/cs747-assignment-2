#! /usr/bin/python
import argparse
parser = argparse.ArgumentParser()
import numpy as np

class Planner():
    def __init__(self,mdp,algorithm,policy):
        S, A, T, R, gamma = read_mdp(mdp)

def read_mdp(path):
    T = R = dict()
    with open(path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            split_line = line.strip().split()
            if split_line[0] == "numStates":
                S = int(split_line[1])
            elif split_line[0] == "numActions":
                A = int(split_line[1])
                T = R = np.zeros((S, A, S))
            elif split_line[0] == "end":
                end_states = map(int, split_line[1])
            elif split_line[0] == "transition":
                s1 = int(split_line[1])
                a = int(split_line[2])
                s2 = int(split_line[3])
                r = float(split_line[4])
                p = float(split_line[5])
                R[s1, a, s2] = r
                T[s1, a, s2] = p
            elif split_line[0] == "mdptype":
                mdptype = split_line[1]
            elif split_line[0] == "discount":
                gamma = float(split_line[1])

    if mdptype == "episodic":
        for ed in end_states:
            R[ed, :, ed] = 0
            T[ed, :, ed] = 1

    return S, A, T, R, gamma

if __name__ == "__main__":
    parser.add_argument("--mdp",type=str,required=True,help="Path to input MDP file")
    parser.add_argument("--algorithm",type=str,choices=["vi", "hpi", "lp", "dual_lp"],default="vi")
    parser.add_argument("--policy",type=str,help="Policy file for which V^pi is to be evaluated (optional)")
    
    args = parser.parse_args()
    # print(args)
    
    planner = Planner(args.mdp,args.algorithm,args.policy)