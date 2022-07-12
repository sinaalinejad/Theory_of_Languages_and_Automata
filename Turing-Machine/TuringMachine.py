
class TuringMachine:
    def __init__(self, turing_machine : str):
        self.turing_machine = turing_machine
        self.initial_state = '1'
        self.final_state = '1'
        self.transitions = self.find_transitions()

    def find_transitions(self) -> dict[tuple[str,str], tuple[str,str,str]]:
        trans = self.turing_machine.split('00')
        transitions = {}
        for t in trans:
            t = t.split('0')
            transitions[(t[0], t[1])] = (t[2], t[3], t[4])
            if len(t[2]) > len(self.final_state):
                self.final_state = t[2]
        return transitions
    
    def check_word(self, word : str) -> bool:
        word = word.split('0')
        if len(word)==1 and word[0]=='' :
            word = ['1']
        head = 0
        state = self.initial_state
        while True:
            head = self.check_head(head, word)
            if state == self.final_state:
                return True
            if not (state, word[head]) in self.transitions:
                return False
            next_move = self.transitions[(state, word[head])]
            state = next_move[0]
            word[head] = next_move[1]
            head = head - 1 if next_move[2] == '1' else head + 1


    def check_head(self, head : int, word : list[str]):
        if head == -1:
            word.insert(0, '1')
            return 0
        elif head == len(word):
            word.append('1')
            return len(word) - 1
        else:
            return head

turing_machine = input()
turing = TuringMachine(turing_machine)
n = int(input())
for i in range(n):
    if turing.check_word(input()):
        print("Accepted")
    else:
        print("Rejected")




