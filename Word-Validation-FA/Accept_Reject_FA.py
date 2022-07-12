def is_accepted(init_sta, string, caller_sta):
    results = []
    if len(string) == 1 and transitions.get((init_sta, string)):
        for state in transitions[(init_sta, string)]:
            if state in final_states:
                return True
    else:
        if transitions.get((init_sta, string[0])):
            for state in transitions[(init_sta, string[0])]:
                results.append(is_accepted(state, string[1: ], init_sta))
    if transitions.get((init_sta, '$')):
        for state in transitions[(init_sta, '$')]:
            if state != init_sta and state != caller_sta:
                results.append(is_accepted(state, string, init_sta))
    if True in results : 
        return True
    return False

    
states = input()[1: -1].split(',')
initial_state = states[0]
alphabet = input()[1: -1].split(',')
final_states = input()[1: -1].split(',')
n = int(input())
transitions = {}
for i in range(n):
    t = input().split(',')
    if (t[0], t[1]) in transitions:
        transitions[(t[0], t[1])].append(t[2])
    else:
        transitions[(t[0],t[1])] = [t[2]]

string = input()


if is_accepted(initial_state, string, initial_state):
    print("Accepted")
else:
    print("Rejected")