This code recieves a turing machine using a string consisting of 0's and 1's, actually you can encode 
every turing machine by encoding states and letters and left-right directions. you can see the images.

Then it validates a number of words which are again encoded by zero and ones.

form of input:
101101011011001010110101
3

11011011
110111011

first line the encoded turing machine.
second line a number k, the number of words to validate by the turing machine.
Next k lines come with the words to validate. the first word in the example is the empty string or lambda.

The output is the word "Accepted" or "Rejected" for every word, in this example:
Accepted
Accepted
Rejected

hints: 
1- the initial state is shown by 1 and the single final state is shown by 1^(number of states) so 
if your machine has multiple final states, convert it to its equivalent single final state.
2- the blank character is shown by 1.
3- the turing machine given should halts on any input which means loops is not allowed, in other 
words this code works for recursive languages.


Thanks.
Sina Alinejad