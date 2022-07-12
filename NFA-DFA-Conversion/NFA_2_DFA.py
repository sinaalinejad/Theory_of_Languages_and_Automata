def where_go_by_lambda(state):
    result = []
    if transitions.get( (state, '$') ):
        for item in transitions[(state, '$')]:
            if item not in result:
                result.append(item)
    for item in result:
        res = where_go_by_lambda(item)
        for t in res:
            result.append(t)
    return result


def where_go(state, c, result):
    if transitions.get( (state, c) ):
        for item in transitions[(state, c)]:
            if item not in result:
                result.append(item)
    temp = result.copy()
    for s in temp:
        res = where_go_by_lambda(s)
        for t in res:
            if t not in result:
                result.append(t)

    res = where_go_by_lambda(state)
    for item in res:
        where_go(item, c, result)
    return result
    


def start(start_sta):
    for c in alphabet:
        result = []
        for s in start_sta:
            res = where_go(s, c, [])
            for item in res:
                if item not in result:
                    result.append(item)
        result = sorted(result)
        dfa_transitions[ (tuple(start_sta), c) ] = result
        if result not in dfa_states:      
            dfa_states.append(result)
            if len(result) > 0:
                new_explored_states.append(result)





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

dfa_initial_state = [initial_state]
dfa_transitions = {}
dfa_final_states = []
dfa_states = [dfa_initial_state]
new_explored_states = [dfa_initial_state]



for item in new_explored_states:
    start(item)
for item in dfa_states:
    for fs in final_states:
        if fs in item:
            dfa_final_states.append(item)
            break

        

print(f"dfa states: {dfa_states}")
print(f"dfa initial states: {dfa_initial_state}")
print(f"dfa final states: {dfa_final_states}")
print(f"dfa transitions:")
for item in dfa_transitions:
    print(f"{item} : {dfa_transitions[item]}")