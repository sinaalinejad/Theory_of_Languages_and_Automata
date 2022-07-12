The code recieves a NFA and returns the equivalent DFA.

Form of input:
{q0,q1,q2,q3,q4}
{a,b}
{q1,q3}
6
q0,a,q1
q1,b,q2
q1,$,q3
q3,b,q4
q2,a,q3
q4,a,q2

line 1: NFA States
line 2: NFA alphabet
line 3: NFA final states
line 4: a number k, number of transitions
next k lines: a transition e.g. q1,b,q2 meaning that being in state q1, by getting "b" you can go to q2.

hint: lambda is shown by "$" sign.

the output is the equivalent DFA.

Thanks.
Sina Alinejad