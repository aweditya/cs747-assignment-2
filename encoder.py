#! /usr/bin/python
import argparse
parser = argparse.ArgumentParser()

class Encoder():
    def __init__(self,states,parameters,q):
        O, T = read_states(states)
        parameters = read_parameters(parameters)
        print("numStates", (O+1)*(T+1))
        print("numActions", 5)
        end_states(O, T)
        generateMDP(O, T, parameters, q)
        print("mdptype episodic")
        print("discount  1.0")

def read_states(path):
    O = 0
    T = 0
    with open(path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            o = int(line[0:2])
            t = int(line[2:4])
            O = max(o, O)
            T = max(t, T)

    return O, T

def action_map(ac):
    action = {0: 0, 1: 1, 2: 2, 4: 3, 6: 4}
    return action[ac]

def state_map(o, t, O, T):
    return o * (T + 1) + t

def read_parameters(path):
    parameters = {}
    with open(path, 'r') as f:
        lines = f.readlines()
        for line in lines[1:]:
            split_line = line.strip().split()
            ac = int(split_line[0])
            parameters[ac] = {}
            parameters[ac][-1] = float(split_line[1])
            parameters[ac][0] = float(split_line[2])
            parameters[ac][1] = float(split_line[3])
            parameters[ac][2] = float(split_line[4])
            parameters[ac][3] = float(split_line[5])
            parameters[ac][4] = float(split_line[6])
            parameters[ac][6] = float(split_line[7])    

    return parameters

def generateMDP(O, T, parameters, q):
    for t in range(1, T+1):
        for o in range(1, O+1):
            # Player A in state (T, O)
            for ac in [0, 1, 2, 4, 6]:
                for runs in [-1, 0, 1, 2, 3, 4, 6]:
                    # Action 'ac' gives 'runs'
                    prob = parameters[ac][runs]
                    # print(prob)
                    if (runs == -1):
                        print_transition(o, t, ac, 0, t, 0, prob, O, T)
                    
                    else:
                        if (t-runs <= 0): # Target chased with balls left
                            print_transition(o, t, ac, o-1, 0, 1, prob, O, T)

                        else:
                            if (runs % 2 == 1): # runs = 1,3
                                if ((o-1) % 6 == 0): # Over is done but A keeps the strike
                                    print_transition(o, t, ac, o-1, t-runs, 0, prob, O, T)

                                else: # Rotate strike
                                    player_B(o, t, ac, o-1, t-runs, q, prob, O, T)

                            else: # runs = 0, 2, 4, 6
                                if not ((o-1) % 6 == 0): # Over is not done and A keeps the strike
                                    print_transition(o, t, ac, o-1, t-runs, 0, prob, O, T)

                                else: # Rotate strike
                                    if (o-1 == 0): # Game is over
                                        print_transition(o, t, ac, 0, t-runs, 0, prob, O, T)

                                    else:
                                        player_B(o, t, ac, o-1, t-runs, q, prob, O, T)

def player_B(o, t, ac, o_next, t_next, q, prob, O, T):
    if (o_next > 0 and t_next > 0):
        # Suppose B gets out
        print_transition(o, t, ac, 0, t_next, 0, prob*q, O, T)

        # Suppose B defends
        if ((o_next-1) % 6 == 0): # Over is done and A gets the strike
            print_transition(o, t, ac, o_next-1, t_next, 0, prob*(1-q)/2, O, T)

        else: # Over is not done and B keeps the strike
            player_B(o, t, ac, o_next-1, t_next, q, prob*(1-q)/2, O, T)

        # Suppose B scores one run
        if ((t_next-1) == 0): # Target chased with balls left
            print_transition(o, t, ac, o_next-1, 0, 1, prob*(1-q)/2, O, T)

        else:
            if ((o_next-1) % 6 == 0): # Over is done and B keeps the strike
                player_B(o, t, ac, o_next-1, t_next-1, q, prob*(1-q)/2, O, T)
            else: # Rotate strike
                print_transition(o, t, ac, o_next-1, t_next-1, 0, prob*(1-q)/2, O, T)

def print_transition(o, t, ac, o_next, t_next, r, p, O, T):
    if not (p == 0):
        print("transition " + str(state_map(o, t, O, T)) + " " + str(action_map(ac)) + " " + str(state_map(o_next, t_next, O, T)) + " " + str(r) + " " + str(p))

def end_states(O, T):
    end_states = "end "
    for o in range(0, O+1):
        end_states += str(state_map(o, 0, O, T))
        end_states += " "

    for t in range(1, T+1):
        end_states += str(state_map(0, t, O, T))
        end_states += " "

    print(end_states)

if __name__ == "__main__":
    parser.add_argument("--states",type=str,required=True,help="Path to cricket states file")
    parser.add_argument("--parameters",type=str,help="Path to player A's parameters file")
    parser.add_argument("--q",type=float,help="Weakness of player B",default=0.25)
    
    args = parser.parse_args()
    encoder = Encoder(args.states,args.parameters,args.q)
