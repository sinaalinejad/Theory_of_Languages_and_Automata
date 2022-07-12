The code recieves your finite automata which can be NFA or DFA and a word to validate.

form of input:
{A,B}
{a,b}
{B}
4
A,b,A
A,a,B
B,a,B
B,b,B
bbb

line 1: FA states
line 2: FA letters
line 3: FA final states
line 4: a number k, number of transitions
next k lines: a transition. A,a,B means that if machine is in state A, getting "a" can go to state B
last line: the word to check if it is accepted by the Finite Automata

hint: lambda is shown by "$" sign.

Thanks.
Sina Alinejad