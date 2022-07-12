states = input()[1: -1].split(',')
initial_state = states[0]
alphabet = input()[1: -1].split(',')
final_states = input()[1: -1].split(',')
n = int(input())
transitions = {}
for i in range(n):
    t = input().split(',')
    transitions[(t[0],t[1])] = t[2]


def has_new_reachable(state):
    for c in alphabet:
        if transitions[(state, c)] not in reachable:
            return True
    return False

def identify_reachable(state):
    result = []
    for c in alphabet:
        s = transitions[(state, c)]
        if s not in reachable:
            reachable[s] = True
            result.append(s)
    for s in result:
        if has_new_reachable(s):
            identify_reachable(s)
        
reachable = {}
reachable[states[0]] = True
identify_reachable(states[0])
temp = states.copy()
for state in temp:
    if state not in reachable:
        states.remove(state)

sta_cnt = len(states)
table = [[[0 for k in range(sta_cnt - 1)] for j in range(sta_cnt)] for i in range(sta_cnt)]
def check_equivalence(i, j, k):
    for c in alphabet:
        st1 = transitions[(states[i], c)]
        i1 = states.index(st1)
        st2 = transitions[(states[j], c)]
        j2 = states.index(st2)
        if table[i1][j2][k] == 0:
            return False
    return True
for i in range(sta_cnt):
    for j in range(sta_cnt):
        if states[i] in final_states and states[j] in final_states:
            table[i][j][0] = 1
        elif states[i] not in final_states and states[j] not in final_states:
            table[i][j][0] = 1

for k in range(1, sta_cnt - 1):
    for i in range(sta_cnt):
        for j in range(sta_cnt):
            if table[i][j][k-1] == 1 and check_equivalence(i, j, k-1):
                table[i][j][k] = 1

visited = [0 for i in range(sta_cnt)]
equ = []
for i in range(sta_cnt):
    if visited[i] == 1:
        continue
    visited[i] = 1
    equ.append([states[i]])
    for j in range(i+1, sta_cnt):
        if table[i][j][sta_cnt - 2] == 1:
            equ[-1].append(states[j])
            visited[j] = 1

simplified_transition = {}
new_final_states = []
for state in equ:
    for c in alphabet:
        for st in equ:
            if transitions[(state[0], c)] in st:
                simplified_transition[(tuple(state), c)] = tuple(st)
                break
for state in equ:
    if state[0] in final_states:
        new_final_states.append(state)

print("states:")
print(equ)
print("final_states:")
print(new_final_states)
print("Simplified transitions:")
for item in simplified_transition:
    print(f"{item} : {simplified_transition[item]}")
