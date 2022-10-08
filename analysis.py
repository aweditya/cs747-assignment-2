#! /usr/bin/python
import argparse
from base64 import encode
import subprocess, os
parser = argparse.ArgumentParser()
import numpy as np
import matplotlib.pyplot as plt

def state_map(o, t, O, T):
    return o * (T + 1) + t

def action_map(ac):
    action = {0: 0, 1: 1, 2: 2, 4: 3, 6: 4}
    return action[ac]

def task1(p1_parameter):
    O = 15
    T = 30 

    rand_pol = {}
    with open('data/cricket/rand-pol.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            split_line = line.strip().split()
            s = split_line[0]
            o = int(s[0:2])
            t = int(s[2:])
            ac = int(split_line[1])

            if not o in rand_pol.keys():
                rand_pol[o] = {}
            
            rand_pol[o][t] = ac

    encoded_pol = []
    for o in range(0, O+1):
        for t in range(0, T+1):
            if not (o == 0 or t == 0):
                encoded_pol.append(action_map(rand_pol[o][t]))
            else:
                encoded_pol.append(0)

    with open('rand-pol', 'w') as f:
        for ac in encoded_pol:
            f.write(str(ac) + "\n")

    rand_win_prob = []
    optimal_win_prob = []

    cmd_cricket_states =  "python", "cricket_states.py", "--balls", str(O), "--runs", str(T)
    f = open('states','w')
    subprocess.call(cmd_cricket_states,stdout=f)
    f.close()

    q_ls = np.linspace(0, 1, 21)
    for q in q_ls:
        cmd_encoder = "python","encoder.py","--parameters", p1_parameter, "--q", str(q), "--states", "states"
        f = open('mdp','w')
        subprocess.call(cmd_encoder,stdout=f)
        f.close()

        cmd_planner = "python","planner.py","--mdp","mdp"
        f = open('planner','w')
        subprocess.call(cmd_planner,stdout=f)
        f.close()

        with open('planner', 'r') as f:
            lines = f.readlines()
            optimal_win_prob.append(float(lines[-1].strip().split()[0]))

        # Get win probability for random policy
        cmd_planner = "python","planner.py","--mdp","mdp","--policy","rand-pol"
        f = open('planner','w')
        subprocess.call(cmd_planner,stdout=f)
        f.close()

        with open('planner', 'r') as f:
            lines = f.readlines()
            rand_win_prob.append(float(lines[-1].strip().split()[0]))

        print(f"Weakness = {q}: optimal win prob = {optimal_win_prob[-1]}, rand-pol win prob = {rand_win_prob[-1]}")

        os.remove('mdp')
        os.remove('planner')

    plt.title("Win Probability vs B's Weakness")
    plt.plot(q_ls, optimal_win_prob, label="Optimal Policy")
    plt.plot(q_ls, rand_win_prob, label="Random Policy")
    plt.xlabel("q")
    plt.ylabel("Win Probability")
    plt.legend()
    plt.show()

    os.remove('states')
    os.remove('rand-pol')

def task2():
    pass

def task3():
    pass

if __name__ == "__main__":
    parser.add_argument("--task",type=int,choices=[1,2,3],default=1)
    
    args = parser.parse_args()
    if (args.task == 1):
        # Win probability vs B's weakness
        task1("data/cricket/sample-p1.txt")
    elif (args.task == 2):
        # Number of balls = 10, q = 0.25 and varying runs to score from 1 to 20. Plotting the win probability
        pass
    elif (args.task == 3):
        # Number of runs = 10, q = 0.25 and balls remaining from 1 to 15. Plotting the win probability
        pass