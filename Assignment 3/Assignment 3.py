import math

class AbstrCondPr():
    def __init__(self,dict,k):
        self.dict = dict
        self.k = k

class CondPr(AbstrCondPr):
    def __init__(self, dict, k):
        super().__init__(dict, k)
        self.cond_pr = {}
        self.total_count = {}

        keys = []
        for key in self.dict.keys():
            keys.append(key)
        
        for key in keys:
            unknown_key = (key[0],"unknown")
            self.dict[unknown_key] = 0

        for key,value in self.dict.items():
            if key[0] not in self.total_count:
                self.total_count[key[0]] = value
            else:
                self.total_count[key[0]] += value

        for key,value in self.dict.items():
            if key not in self.cond_pr:
                if self.k > 0:
                    self.cond_pr[key]= (value + k) / (self.total_count[key[0]] + k * len(set(self.dict.keys())))
                else:
                    self.cond_pr[key]=value / self.total_count[key[0]]
              
        
    
    def show(self):
        for key,value in self.cond_pr.items():
            w1 = key[0]
            w2 = key [1]
            if w2 == "unknown":
                pass
            else:
                print("Pr('{}'|'{}') = {}".format(w2, w1, value))

    def __getitem__(self,key):
        if key in self.cond_pr:
            return self.cond_pr[key]
        elif key[0] not in self.total_count.keys():
            return f"Pr('{key[1]}'|'{key[0]}' 'is not defined')"
        else:
            return self.log_cond_pr[(key[0],'unknown')]
            

class LogCondPr(AbstrCondPr):
    def __init__(self, dict, k):
        super().__init__(dict, k)
        self.log_cond_pr = {}
        self.total_count = {}
        keys = []
        for key in self.dict.keys():
            keys.append(key)
        
        for key in keys:
            unknown_key = (key[0],"unknown")
            self.dict[unknown_key] = 0

        for key,value in self.dict.items():
            if key[0] not in self.total_count:
                self.total_count[key[0]] = value
            else:
                self.total_count[key[0]] += value

        for key,value in self.dict.items():
            if key not in self.log_cond_pr:
                if self.k > 0 :
                    log = math.log((value + self.k)/ (self.total_count[key[0]]+ self.k* len(set(self.dict.keys()))))
                    self.log_cond_pr[key] = log 
                elif value > 0 :
                    log = math.log(value/self.total_count[key[0]])
                    if log == 0:
                        self.log_cond_pr[key]= float("-inf")
                    else:
                        self.log_cond_pr[key]= log
                else:
                    self.log_cond_pr[key]= float("-inf")
                         

    def show(self):
        for key,value in self.log_cond_pr.items():
            w1 = key[0]
            w2 = key [1]
            if w2 == "unknown":
                pass
            else:
                print("Pr('{}'|'{}') = {}".format(w2, w1, value))

    def __getitem__(self,key):
        if key in self.log_cond_pr.keys():
            if self.log_cond_pr[key] == 0:
                return float('-inf')
            else:
                return self.log_cond_pr[key]
                
        elif key[0] not in self.total_count.keys():
            return f"Pr('{key[1]}'|'{key[0]}' 'is not defined')"
        else:
            return self.log_cond_pr[(key[0],'unknown')]

 
def HMM():
    Q = []
    sentences =[]
    word_tag =[]
    with open ('tags.toks_tags', encoding='utf-8') as file:
        for sentence in file:
            words=sentence.strip().split()
            sentences.append(words)
            for word in words:
                all_words= word.split('|')
                word_tag.append((all_words[0].lower(),all_words[1]))
                if all_words[1] not in Q:
                    Q.append(all_words[1])
    
    tags = []
    for sentence in sentences:
        sentence.insert(0,'-|BOS') 
        sentence.append('-|EOS')
        for word in sentence:
            all_tags = word.split('|')
            tags.append(all_tags[1])
    
    tag_bigrams = {}
    bigrams = tuple(zip(tags,tags[1:]))
    for pair in bigrams:
        if pair not in tag_bigrams:
            tag_bigrams[pair] = 0
        tag_bigrams[pair]+=1
  
    
    #I had to edit the tuple otherwise the class was calculating the probabilities wrong.
    words_tags = {}
    for word in word_tag:
        edited_tuple = (word[1],word[0])
        if edited_tuple not in words_tags:
            words_tags[edited_tuple] = 0
        words_tags[edited_tuple] += 1
    
    return Q, tag_bigrams, words_tags

def viterbi_algorithm (Q,A,B,O):
    for word in O:
        word = word.lower()

    time_steps = len(O)
    viterbi = {}
    backpointer = {}
    #initialization step
    for state in Q:
       viterbi[(state,0)] =  A[('BOS', state)] + B[state,O[0]]
       backpointer[(state,0)] = 0
    
    #recursion step
    for time_step in range(1, time_steps):
        for state in Q: 
            max_prob = float('-inf') 
            best_previous_step = None
            for previous_step in Q:
                prob = viterbi[(previous_step,time_step-1)] + A[previous_step,state] + B[state,O[time_step]]
                if prob > max_prob:
                    max_prob = prob
                    best_previous_step = previous_step 
                viterbi[(state,time_step)] = max_prob
                backpointer[(state,time_step)] = best_previous_step
    #print(viterbi)
    #print(backpointer)
        
    #termination step
    best_path_probability = float('-inf')
    best_final_step = None
    for state in Q:
        probability = viterbi[(state, time_steps-1)] + A[state,'EOS']
        if probability > best_path_probability:
            best_path_probability = probability
            best_final_step = state 
    
    best_path_pointer = [best_final_step]
    
    
    for time_step in range (time_steps -1 ,0,-1):
        best_path_pointer.append(backpointer[(best_path_pointer[-1],time_step)])

    best_path_pointer = best_path_pointer[::-1]

    return best_path_probability ,best_path_pointer


if __name__ == "__main__":
    obs = {('Maserati','green'):2, ('Ferrari','red'):3, ('Maserati','blue'): 4, ('Ferrari','black'): 1, ('Jaguar', 'green'): 10}
    col_given_brand = CondPr(obs,0)
    #col_given_brand.show()
    #print(col_given_brand[('Maserati','green')])
    col_given_brand_log = LogCondPr(obs,2)
    #col_given_brand_log.show()
    #print(col_given_brand_log[('Maserati','green')])
    Q , tag_bigrams, words_tags = HMM()
    #print(HMM)
    transition_prob = LogCondPr(tag_bigrams,0)
    #transition_prob.show()
    print('These are 5 examples of transition probabilities:')
    print(f'transition probability of (\'BOS\',\'VERB\'):')
    print(transition_prob['BOS','VERB']) 
    print(f'transition probability of (\'ADJ\',\'NOUN\'):')
    print(transition_prob['ADJ','NOUN'])
    print(f'transition probability of (\'PART\',\'VERB\'):')
    print(transition_prob['PART','VERB'])
    print(f'transition probability of (\'VERB\',\'VERB\'):')
    print(transition_prob['VERB','VERB'])
    print(f'transition probability of (\'NUM\',\'AUX\'):')
    print(transition_prob['NUM','AUX'])
    emission_prob = LogCondPr(words_tags,0)
    #emission_prob.show()
    print('These are 5 examples of emission probabilities:')
    print(f'emission probability of (\'mate\',\'NOUN\'):')
    print(emission_prob['NOUN','mate'])
    print(f'emission probability of (\'belong\',\'VERB\'):')
    print(emission_prob['VERB','belong'])
    print(f'emission probability of (\'the\',\'DET\'):')
    print(emission_prob['DET', 'the'])
    print(f'emission probability of (\'611\',\'NUM\'):')
    print(emission_prob['NUM','611'])
    print(f'emission probability of (\'they\',\'PRON\'):')
    print(emission_prob['PRON','they'])
    A = LogCondPr(tag_bigrams,2)
    B = LogCondPr(words_tags,2)
    O1 = ['the','river','flows','gently','under','the','bridge','.']
    O2 = ['this','book','is','the','best','.']
    O3 = ['the','cat','is','running','away','from','the','dog','.']
    print('The river flows gently under the bridge.:')
    print(viterbi_algorithm(Q,A,B,O1 ))
    print('This book is the best.:')
    print(viterbi_algorithm(Q,A,B,O2 ))
    print('The cat is running away from the cat.:')
    print(viterbi_algorithm(Q,A,B,O3 ))
 