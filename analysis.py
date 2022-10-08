#! /usr/bin/python
import argparse, subprocess, os
parser = argparse.ArgumentParser()
import numpy as np
import matplotlib.pyplot as plt

def get_encoded_policy(path='data/cricket/rand-pol.txt',rand_pol_path='rand-pol'):
    O = 15
    T = 30 

    rand_pol = {}
    with open(path, 'r') as f:
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

    with open(rand_pol_path, 'w') as f:
        for ac in encoded_pol:
            f.write(str(ac) + "\n")

def state_map(o, t, O=15, T=30):
    return o * (T + 1) + t

def action_map(ac):
    action = {0: 0, 1: 1, 2: 2, 4: 3, 6: 4}
    return action[ac]

def task1(p1_parameter, mdp_path, planner_path, states_path, rand_pol_path):
    rand_win_prob = []
    optimal_win_prob = []

    q_ls = np.linspace(0, 1, 21)
    for q in q_ls:
        cmd_encoder = "python","encoder.py","--parameters", p1_parameter, "--q", str(q), "--states", states_path
        f = open(mdp_path,'w')
        subprocess.call(cmd_encoder,stdout=f)
        f.close()

        cmd_planner = "python","planner.py","--mdp",mdp_path
        f = open(planner_path,'w')
        subprocess.call(cmd_planner,stdout=f)
        f.close()

        with open(planner_path, 'r') as f:
            lines = f.readlines()
            optimal_win_prob.append(float(lines[-1].strip().split()[0]))

        # Get win probability for random policy
        cmd_planner = "python","planner.py","--mdp",mdp_path,"--policy",rand_pol_path
        f = open(planner_path,'w')
        subprocess.call(cmd_planner,stdout=f)
        f.close()

        with open(planner_path, 'r') as f:
            lines = f.readlines()
            rand_win_prob.append(float(lines[-1].strip().split()[0]))

        print("Weakness = {:.3f}: optimal win prob = {:.6f}, rand-pol win prob = {:.6f}".format(q, optimal_win_prob[-1], rand_win_prob[-1]))

    plt.title("Win Probability vs B's Weakness")
    plt.plot(q_ls, optimal_win_prob, label="Optimal Policy")
    plt.plot(q_ls, rand_win_prob, label="Random Policy")
    plt.xlabel("q")
    plt.ylabel("Win Probability")
    plt.grid(linestyle = '--', linewidth = 0.5)
    plt.legend()
    plt.show()

def task2(p1_parameter, mdp_path, planner_path, states_path, rand_pol_path):
    cmd_encoder = "python","encoder.py","--parameters", p1_parameter, "--q", "0.25", "--states", states_path
    f = open(mdp_path,'w')
    subprocess.call(cmd_encoder,stdout=f)
    f.close()

    rand_win_prob = []
    optimal_win_prob = []

    T = 20
    runs = np.arange(1, T+1)

    # Get win probability for optimal policy
    cmd_planner = "python","planner.py","--mdp",mdp_path
    f = open(planner_path,'w')
    subprocess.call(cmd_planner,stdout=f)
    f.close()

    with open(planner_path, 'r') as f:
        lines = f.readlines()
        for t in runs:
            optimal_win_prob.append(float(lines[state_map(10, t)].strip().split()[0]))

    # Get win probability for random policy
    cmd_planner = "python","planner.py","--mdp",mdp_path,"--policy",rand_pol_path
    f = open(planner_path,'w')
    subprocess.call(cmd_planner,stdout=f)
    f.close()

    with open(planner_path, 'r') as f:
        lines = f.readlines()
        for t in runs:
            rand_win_prob.append(float(lines[state_map(10, t)].strip().split()[0]))
    
    plt.title("Win Probability vs Runs to Score (Balls = 10)")
    plt.plot(runs, optimal_win_prob, label="Optimal Policy")
    plt.plot(runs, rand_win_prob, label="Random Policy")
    plt.xticks(runs)
    plt.xlabel("Runs")
    plt.ylabel("Win Probability")
    plt.grid(linestyle = '--', linewidth = 0.5)
    plt.legend()
    plt.show()

def task3(p1_parameter, mdp_path, planner_path, states_path, rand_pol_path):
    cmd_encoder = "python","encoder.py","--parameters", p1_parameter, "--q", "0.25", "--states", states_path
    f = open(mdp_path,'w')
    subprocess.call(cmd_encoder,stdout=f)
    f.close()

    rand_win_prob = []
    optimal_win_prob = []

    O = 15
    balls = np.arange(1, O+1)

    # Get win probability for optimal policy
    cmd_planner = "python","planner.py","--mdp",mdp_path
    f = open(planner_path,'w')
    subprocess.call(cmd_planner,stdout=f)
    f.close()

    with open(planner_path, 'r') as f:
        lines = f.readlines()
        for o in balls:
            optimal_win_prob.append(float(lines[state_map(o, 10, 15, 30)].strip().split()[0]))

    # Get win probability for random policy
    cmd_planner = "python","planner.py","--mdp",mdp_path,"--policy",rand_pol_path
    f = open(planner_path,'w')
    subprocess.call(cmd_planner,stdout=f)
    f.close()

    with open(planner_path, 'r') as f:
        lines = f.readlines()
        for o in balls:
            rand_win_prob.append(float(lines[state_map(o, 10, 15, 30)].strip().split()[0]))

    plt.title("Win Probability vs Balls Left (Runs = 10)")
    plt.plot(balls, optimal_win_prob, label="Optimal Policy")
    plt.plot(balls, rand_win_prob, label="Random Policy")
    plt.xticks(balls)
    plt.xlabel("Balls Left")
    plt.ylabel("Win Probability")
    plt.grid(linestyle = '--', linewidth = 0.5)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    parser.add_argument("--task",type=int,choices=[1,2,3],default=1)
    args = parser.parse_args()

    p1_parameter = "data/cricket/sample-p1.txt"
    rand_pol_path = 'rand-pol'
    mdp_path = 'mdp'
    planner_path = 'planner'
    states_path = 'states'

    get_encoded_policy(rand_pol_path=rand_pol_path)

    cmd_cricket_states =  "python", "cricket_states.py", "--balls", "15", "--runs", "30"
    f = open(states_path,'w')
    subprocess.call(cmd_cricket_states,stdout=f)
    f.close()

    if (args.task == 1):
        # Win probability vs B's weakness
        task1(p1_parameter, mdp_path, planner_path, states_path, rand_pol_path)
    elif (args.task == 2):
        # Number of balls = 10, q = 0.25 and varying runs to score from 1 to 20. Plotting the win probability
        task2(p1_parameter, mdp_path, planner_path, states_path, rand_pol_path)
    elif (args.task == 3):
        # Number of runs = 10, q = 0.25 and balls remaining from 1 to 15. Plotting the win probability
        task3(p1_parameter, mdp_path, planner_path, states_path, rand_pol_path)

    # Clean up
    os.remove(rand_pol_path)
    os.remove(mdp_path)
    os.remove(planner_path)
    os.remove(states_path)