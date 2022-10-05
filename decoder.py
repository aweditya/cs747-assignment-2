#! /usr/bin/python
import argparse
parser = argparse.ArgumentParser()

class Decoder():
    def __init__(self,value_policy,states):
        states, O, T = read_states(states)
        decode(states, value_policy, O, T)

def read_states(path):
    states = []
    O = 0
    T = 0
    with open(path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()

            o = int(line[0:2])
            t = int(line[2:4])
            states.append([o, t])

            O = max(o, O)
            T = max(t, T)

    return states, O, T

def state_map(o, t, O, T):
    return o * (T + 1) + t

def action_map(ac):
    action = {0: 0, 1: 1, 2: 2, 3: 4, 4: 6}
    return action[ac]

def decode(states, value_policy, O, T):
    with open(value_policy, 'r') as f:
        lines = f.readlines()
        split_lines = [line.strip().split() for line in lines]
        for state in states:
            o = state[0]
            t = state[1]
            id = state_map(o, t, O, T)
            print(str(o).zfill(2) + str(t).zfill(2) + " " + str(action_map(int(split_lines[id][1]))) + " " + split_lines[id][0])

if __name__ == "__main__":
    parser.add_argument("--value-policy",type=str,required=True,help="Path to file containing optimal value function and policy")
    parser.add_argument("--states",type=str,required=True,help="Path to cricket states file")
    
    args = parser.parse_args()
    decoder = Decoder(args.value_policy,args.states)