from unicodedata import name


#! /usr/bin/python
import argparse
parser = argparse.ArgumentParser()

class Planner():
    def __init__(self,mdp,algorithm,policy):
        pass

if __name__ == "__main__":
    parser.add_argument("--mdp",type=str,required=True,help="Path to input MDP file")
    parser.add_argument("--algorithm",type=str,choices=["vi", "hpi", "lp", "dual_lp"],default="vi")
    parser.add_argument("--policy",type=str,help="Policy file for which V^pi is to be evaluated (optional)")
    
    args = parser.parse_args()
    print(args)
    
    planner = Planner(args.mdp,args.algorithm,args.policy)