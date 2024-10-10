Q = [0,1,2,3,4]
Sigma = ["b","a","!"]
q0 = 0
F = [4]
delta = {(0,"b"):1,
         (1,"a"):2,
         (2,"a"):3,
         (3,"a"):3,
         (3,"!"):4}

DFA = (Q,Sigma,q0,F,delta)

def d_recognize(T,M):
    M = DFA

    index = 0
    current_state = q0

    while True:
        if index == len(T):
            if current_state in F:
                return True
            else :
                return False
        elif (current_state,T[index]) not in delta:
            return False
        else:
            current_state = delta[current_state,T[index]]
            index +=1
print(d_recognize("baaaaaa!",DFA))