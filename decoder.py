#! /usr/bin/python
import argparse
from audioop import reverse
from email import policy
parser = argparse.ArgumentParser()

class Decoder():
    def __init__(self,value_policy,states):
        O, T = read_states(states)
        decode(value_policy, O, T)

def read_states(path):
    with open(path, 'r') as f:
        lines = f.readlines()

    O = 15
    T = 10
    return O, T

def action_map(ac):
    action = {0: 0, 1: 1, 2: 2, 3: 4, 4: 6}
    return action[ac]

def decode(value_policy, O, T):
    with open(value_policy, 'r') as f:
        lines = f.readlines()
        split_lines = [line.strip().split() for line in lines]
        for o in reversed(range(O+1)):
            for t in reversed(range(T+1)):
                if not (o == 0 or t == 0):
                    print(str(o).zfill(2) + str(t).zfill(2) + " " + str(action_map(int(split_lines[o*(T+1) + t][1]))) + " " + split_lines[o*(T+1) + t][0])


if __name__ == "__main__":
    parser.add_argument("--value-policy",type=str,required=True,help="Path to file containing optimal value function and policy")
    parser.add_argument("--states",type=str,required=True,help="Path to cricket states file")
    
    args = parser.parse_args()
    decoder = Decoder(args.value_policy,args.states)