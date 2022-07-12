Recieving the DFA, this code returns the simplest equvalent DFA.

Input form:
{q0,q1,q2,q3,q4}
{0,1}
{q4}
10
q0,0,q1
q0,1,q3
q1,0,q2
q1,1,q4
q2,0,q1
q2,1,q4
q3,1,q4
q3,0,q2
q4,0,q4
q4,1,q4

line 1: DFA states
line 2: DFA alphabet
line 3: DFA final states
line 4: a number k, number of transitions
next k lines: a transition e.g. q1,1,q4 means in state q1, getting the input "1" you should go to q4

Thanks.
Sina Alinejad