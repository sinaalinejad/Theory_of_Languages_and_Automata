import re

class PDA:
    def __init__(self, grammar, states):
        self.states = states
        self.last_made_variable = 0
        self.initial_state = states[0]
        self.remove_useless_productions(grammar)
        self.grammar = self.convert_to_chomsky(grammar)

    def parse_word(self, word):
        table = [ [[] for j in range(len(word)) ] for i in range(len(word)) ]
        for i in range(len(word)):
            for state in self.states:
                if word[i] in self.grammar[state]:
                    table[i][i].append(state)
        
        return self.Cyk(table, word)
    
    def Cyk(self, table, word):
        for l in range(2, len(word)+1):
            for i in range(len(word)-l+1):
                j = i+l-1
                for k in range(i, j):
                    for state in self.states:
                        if self.check_if_make_vars(table, state, i,j,k):
                            table[i][j].append(state)
        if self.initial_state in table[0][len(word)-1]:
            return True
        return False


    def check_if_make_vars(self,table, state, i, j, k):
        for trans in self.grammar[state]:
            _vars = re.findall(r'<[^>]+>', trans)
            if len(_vars)==2 and _vars[0] in table[i][k] and _vars[1] in table[k+1][j]:
                return True
        
        return False

    def remove_useless_productions(self, grammar):
        useful_vars = self.find_usefull_variables(grammar)
        for state in self.states:
            if state not in useful_vars:
                del grammar[state]
                self.states.remove(state)
            else:
                for trans in grammar[state]:
                    for match in re.findall(r'<\w>', trans):
                        if match not in useful_vars:
                            grammar[state].remove(trans)
                            break
        self.remove_non_reachable_variables(grammar)
        


    def find_usefull_variables(self, grammar):
        useful_vars = []
        changed = 1
        while changed == 1:
            changed = 0
            for state in self.states:
                for trans in grammar[state]:
                    is_useful = True
                    for match in re.findall(r'<\w>', trans):
                        if match not in useful_vars:
                            is_useful = False
                    if is_useful and state not in useful_vars:
                        useful_vars.append(state)
                        changed = 1
        return useful_vars
        
        
    def remove_non_reachable_variables(self, grammar):
        reachables = self.find_reachable_variables(grammar, self.initial_state)
        for state in self.states:
            if state not in reachables:
                del grammar[state]
                self.states.remove(state)

                
    def find_reachable_variables(self, grammar, reachable, reachables=[]):
        reachables.append(reachable)
        for trans in grammar[reachable]:
            for match in re.findall(r'<\w>', trans):
                if match not in reachables:
                    self.find_reachable_variables(grammar, match, reachables)
        return reachables

                    

    def convert_to_chomsky(self, grammar):
        self.remove_nullable_unit_productions(grammar)
        production = self.find_contradiction_with_chomsky(grammar) # A -> abcD
        while production != False:
            self.resolve_chomsky_contradiction(production, grammar)
            production = self.find_contradiction_with_chomsky(grammar)
        
        production = self.find_production_with_more_than_length_two(grammar) # A -> BCD
        while production != False:
            self.resolve_extra_length_production(production, grammar)
            production = self.find_production_with_more_than_length_two(grammar)
        return grammar
    
    def find_production_with_more_than_length_two(self, grammar):
        for state in self.states:
            for trans in grammar[state]:
                _vars = re.findall(r'<[\w,\W]>', trans)
                if len(_vars) > 2:
                    return state, trans
        return False
    def resolve_extra_length_production(self, production, grammar):
        _vars = re.findall(r'<[\w,\W]>', production[1])
        if len(_vars) == 2:
            return
        trans = "".join(_vars[1:])
        state = self.get_state_having_trans(trans, grammar)
        new_var = state if state != False else "<"+"xyz"+str(self.last_made_variable)+">"
        grammar[production[0]].append(_vars[0] + new_var)
        grammar[production[0]].remove(production[1])
        if new_var not in self.states:
            grammar[new_var] = [trans]
            self.states.append(new_var)
            self.last_made_variable+=1
        self.resolve_extra_length_production((new_var, trans), grammar)

    
    def find_contradiction_with_chomsky(self, grammar):
        for state in self.states:
            for trans in grammar[state]:
                if len(trans) > 1 and len(self.find_letters(trans))>0:
                    return state, trans
        return False
    
    
    
    def resolve_chomsky_contradiction(self, production, grammar):
        letters = self.find_letters(production[1])
        for let in letters:
            if "<"+let+">" not in grammar:
                grammar["<"+let+">"] = [let]
                self.states.append("<"+let+">")
        result = ""
        i = 0
        while i != len(production[1]):
            if production[1][i] == "<":
                result += "<"+production[1][i+1]+">"
                i+=2
            else:
                result += "<"+production[1][i]+">"
            i+=1

        ind = grammar[production[0]].index(production[1])
        grammar[production[0]][ind] = result

    def find_letters(self, string):
        letters = re.split(r'<[\w,\W]>', string)
        letters = list(set(letters))
        if "" in letters:
            letters.remove("")
        return letters
    def get_state_having_trans(self, trans, grammar):
        for state in self.states:
            if trans in grammar[state]:
                return state
        return False

    def remove_identity_transitions(self, grammar):
        for state in self.states:
            if state in grammar[state]:
                grammar[state].remove(state)
        
    def remove_nullable_unit_productions(self, grammar):
        u_p = self.find_unit_production(grammar)
        n_p = self.find_nullable_production(grammar)
        while u_p != False or n_p != False:
            while u_p != False:
                self.remove_unit_production(u_p, grammar)
                self.remove_identity_transitions(grammar)
                u_p = self.find_unit_production(grammar)
            while n_p != False:
                self.remove_nullable_production(n_p, grammar)
                self.remove_identity_transitions(grammar)
                n_p = self.find_nullable_production(grammar)
            u_p = self.find_unit_production(grammar)
            n_p = self.find_nullable_production(grammar)

    def find_unit_production(self, grammar):
        for state in self.states:
            for trans in grammar[state]:
                if len(trans) == 3 and trans[0] == "<": # check if it is unit production
                    return state, trans
        return False
    
    def remove_unit_production(self,production, grammar):
        if production[0] == self.initial_state:
            self.substitute_unit(production, grammar)
            grammar[production[0]] = list(set(grammar[production[0]]))
            return
        
        for state in self.states:
            grammar[state] = list(set(grammar[state])) # removing duplicate transitions
            leng = len(grammar[state])
            for ind,trans in enumerate(grammar[state]):
                if ind == leng:
                    break
                if production[0] in trans:
                    self.add_all_possible_combinations(state, production[0],trans, grammar, production[1])
            grammar[state] = list(set(grammar[state])) # removing duplicate transitions
        grammar[production[0]].remove(production[1])
    def substitute_unit(self, production, grammar):
        temp = grammar[production[1]]
        for t in temp:
            grammar[production[0]].append(t)
        grammar[production[0]].remove(production[1])
    def find_nullable_production(self, grammar):
        for state in self.states:
            for trans in grammar[state]:
                if trans == "#":
                    return state
        return False

    def remove_nullable_production(self, lambda_state, grammar):
        for state in self.states:
            grammar[state] = list(set(grammar[state]))
            for trans in grammar[state]:
                if lambda_state in trans:
                    self.add_all_possible_combinations(state, lambda_state, trans, grammar, "")
            
            grammar[state] = list(set(grammar[state]))
        grammar[lambda_state].remove("#")

    def add_all_possible_combinations(self,state, st_to_replace_with, trans, grammar, st_to_replace):
        cnt = trans.count(st_to_replace_with)
        indices = self.find_all_sub_indexes(trans, st_to_replace_with)
        result = list(trans)
        for i in range(1, cnt+1):
            for comb in self.combinations(indices, i):
                for j in comb:
                    if st_to_replace == "":
                        result[j] = ""
                        result[j+1] = ""
                        result[j+2] = ""
                    else:
                        result[j+1] = st_to_replace[1]
                grammar[state].append("".join(result))
                result = list(trans)

    def combinations(self, iterable, r):
        from itertools import permutations
        pool = tuple(iterable)
        n = len(pool)
        for indices in permutations(range(n), r):
            if sorted(indices) == list(indices):
                yield tuple(pool[i] for i in indices)


    def find_all_sub_indexes(self, a_str, sub):
        start = 0
        result = []
        while True:
            start = a_str.find(sub, start)
            if start == -1: return result
            result.append(start)
            start += len(sub)
        return result


grammar = {}
states = []
n = int(input())
for i in range(n):
    inp = input()
    temp = inp.split(" -> ")
    states.append(temp[0])
    trans = temp[1].split(" | ")
    grammar[temp[0]] = trans

pda = PDA(grammar, states)


print(pda.grammar)
if pda.parse_word(input()):
    print("Accepted")
else:
    print("Rejected")

