using this code, you can give your context free grammar and a word and it returns you if the word is
accepted or rejected by the context free grammar.

it works by converting your grammar to a chomsky normal form grammar and then validating by the CYK
algorithm.

form of input:
3
<S> -> a<S>b | a<A> | b<B>
<A> -> a<A> | #
<B> -> b<B> | #
aaab

first line k the number of variables and in next k lines transitions of those variables which are 
seperated by "|" symbol. variables are surrounded by <> signs and lambda symbol is shown with "#".

In the last line a word to validate comes in this example "aaab".

The output is the word "Accepted" or "Rejected".

hint: all variables and letters has the length 1, if your grammar doesn't observe it, convert it 
so that it will.

Thanks.
Sina Alinejad