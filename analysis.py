#! /usr/bin/python
import argparse
import subprocess, os
parser = argparse.ArgumentParser()
import numpy as np
import matplotlib.pyplot as plt

def task1(states, p1_parameter):
    rand_win_prob = []
    optimal_win_prob = []

    q_ls = np.linspace(0, 1, 101)
    for q in q_ls:
        cmd_encoder = "python","encoder.py","--parameters", p1_parameter, "--q", str(q), "--states",states
        f = open('mdp','w')
        subprocess.call(cmd_encoder,stdout=f)
        f.close()

        cmd_planner = "python","planner.py","--mdp","mdp"
        f = open('planner','w')
        subprocess.call(cmd_planner,stdout=f)
        f.close()

        # Get optimal win probability for 30 balls, 15 runs
        with open('planner', 'r') as f:
            lines = f.readlines()
            optimal_win_prob.append(float(lines[-1].strip().split()[0]))

        print(f"Weakness = {q}: Optimal Win Probability = {optimal_win_prob[-1]}")

        os.remove('mdp')
        os.remove('planner')

    plt.title("Win Probability vs B's Weakness")
    plt.plot(q_ls, optimal_win_prob)
    plt.xlabel("q")
    plt.ylabel("Win Probability")
    plt.show()

def task2():
    pass

def task3():
    pass

if __name__ == "__main__":
    parser.add_argument("--task",type=int,choices=[1,2,3],default=1)
    
    args = parser.parse_args()
    if (args.task == 1):
        # Win probability vs B's weakness
        task1("data/cricket/cricket_state_list.txt", "data/cricket/sample-p1.txt")
    elif (args.task == 2):
        # Number of balls = 10, q = 0.25 and varying runs to score from 1 to 20. Plotting the win probability
        pass
    elif (args.task == 3):
        # Number of runs = 10, q = 0.25 and balls remaining from 1 to 15. Plotting the win probability
        pass