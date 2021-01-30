import qiskit
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import Aer, execute
from qiskit.quantum_info.operators import Operator
from qiskit.extensions import UnitaryGate, Initialize
from qiskit import IBMQ
import math

backend = Aer.get_backend('qasm_simulator')

class quantum_obj:

    def __init__(self, pos, piece):
        self.piece =  piece
        self.qnum = { '0': [pos, 1] }
        self.ent = []

    def split(self, i_add, pos1, pos2):
        ## i_pos = self.qnum[i_add][0]
        self.qnum[i_add + '0'] = ["", 0]
        self.qnum[i_add + '1'] = ["", 0]
        self.qnum[i_add + '0'][0] = pos1
        self.qnum[i_add + '1'][0] = pos2
        self.qnum[i_add + '0'][1] = self.qnum[i_add][1]/2.0             #probability of split piece is half of original piece
        self.qnum[i_add + '1'][1] = self.qnum[i_add][1]/2.0
        del self.qnum[i_add]  

    def entangle_oneblock(self, i_add, pos1, obj, obj_add):            
        
        # return quantumobj, pos of quantumobj from in_bw_pieces
        
        '''
            1 2 3 
        a | P Q _
        b | _ _ _
        c | _ _ _

        a1 to a3
        If Q is classical, move cannot be made.
        If Q is not classical, P and Q get entangled.
        
        Let P[P at a1] = x
        Let P[Q at a2] = y

        After the move,
        P[P at a3] = x * (1 - y)
        P[P at a1] = x * y
        '''

        prob_blocked_piece = self.qnum[i_add][1]
        prob_blocking_piece = obj.qnum[obj_add][1]

        x = prob_blocked_piece
        y = prob_blocking_piece

        a = x*y               # prob_not_moved = prob_blocked*prob_blocking      
        b = x*(1-y)           # prob_moved = prob_blocked_piece*(1-prob_blocking_piece)

        self.qnum[i_add + '0'] = ["", 0]
        self.qnum[i_add + '1'] = ["", 0]
        self.qnum[i_add + '0'][0] = self.qnum[i_add][0]       
        self.qnum[i_add + '1'][0] = pos1
        self.qnum[i_add + '0'][1] = a       
        self.qnum[i_add + '1'][1] = b 
        del self.qnum[i_add]

        obj.ent += [(self, i_add+'1', obj_add)]   # make sure that obj is quantumobj while calling!
        self.ent += [(obj, obj_add, i_add+'1')]


    def entangle_twoblock(self, i_add, pos1, pos2, obj1, obj1_add, obj2, obj2_add):  #change pos parameter to address
        
        # Applicable when 
        #    - both positions are blocked, so entanglement with 2 pieces
        
        # obj1 is blocking pos1 and obj2 is blocking pos2
        # return quantumobj, pos of quantumobj from in_bw_pieces
        '''
        
            1 2 3 
        a | P Y R
        b | X _ _
        c | Q _ _

        a1 to split (c1, a3)
        If both Q and R are classical, no move.
        Else, weighted split.

        Let P[P at a1] = x
        Let P[Y at a2] = y
        Let P[X at b1] = z

        After the move, 
        P[P at a1] = x * P[both Q and R are there] = x*y*z
        P[P at a3] = x * ( P[Q not at a2, R at b1] + 0.5 * P[Q, R not there] ) = x*(1-y)*z + 0.5*x*(1-y)*(1-z)
        P[P at c1] = x * ( P[Q at a2, R not at b1] + 0.5 * P[Q, R not there] ) = x*y *(1-z) + 0.5*x*(1-y)*(1-z)
        
        #check
        Total prob = xyz + xz - xyz + xy - xyz + x - xy - xz + xyz
                   = x

        # these hold up even if P, Q, R are classical
        '''
        
        prob_i_pos = self.qnum[i_add][1]
        prob_ob1 = obj1.qnum[obj1_add][1]
        prob_ob2 = obj2.qnum[obj2_add][1]

        '''
        1. ob1 there, ob2 there - not possible (0)
        2. ob1 there, ob2 not there - p(ob1)
        3. ob1 not there, ob2 there - p(ob2)
        4. ob1 not there, ob2 not there - (1-p(ob1))(1-p(ob2))

        at pos1 when ob1 not there - c3 + 0.5*c4
        at pos2 when ob2 not there - c2 + 0.5*c4
        at ipos when ob1, ob2 there - c1

        '''

        if obj1 == obj2:
            prob_pos1 = prob_i_pos*prob_ob2 + 0.5*prob_i_pos*(1 - prob_ob1 - prob_ob2)
            prob_pos2 = prob_i_pos*prob_ob1 + 0.5*prob_i_pos*(1 - prob_ob1 - prob_ob2)
            
            self.qnum[i_add + '0'] = ["", 0]     
            self.qnum[i_add + '1'] = ["", 0]
            self.qnum[i_add + '0'][0] = pos1
            self.qnum[i_add + '0'][1] = prob_pos1  
            self.qnum[i_add + '1'][0] = pos2
            self.qnum[i_add + '1'][1] = prob_pos2  
            obj1.ent += [(self, i_add+'0', obj1_add)]             # obj1 cannot coexist with i_add+'0'
            obj2.ent += [(self, i_add+'1', obj2_add)]             # obj2 cannot coexist with i_add+'1'
            self.ent += [(obj1, obj1_add, i_add+'0'), (obj2, obj2_add, i_add+'1')]
        
        else:
            prob_unmoved = prob_i_pos*prob_ob1*prob_ob2 
            prob_pos1 = prob_i_pos*(1-prob_ob1)*prob_ob2 + 0.5*prob_i_pos*(1-prob_ob1)*(1-prob_ob2)
            prob_pos2 = prob_i_pos*prob_ob1*(1-prob_ob2) + 0.5*prob_i_pos*(1-prob_ob1)*(1-prob_ob2)
            
            # a(bc+c-bc+b-bc+1-b-c+bc) = a

            self.qnum[i_add + '00'] = ["", 0]     
            self.qnum[i_add + '01'] = ["", 0]
            self.qnum[i_add + '10'] = ["", 0]
            self.qnum[i_add + '00'][0] = self.qnum[i_add][0]
            self.qnum[i_add + '01'][0] = pos1
            self.qnum[i_add + '10'][0] = pos2
            self.qnum[i_add + '00'][1] = prob_unmoved  
            self.qnum[i_add + '01'][1] = prob_pos1
            self.qnum[i_add + '10'][1] = prob_pos2

            obj1.ent += [(self, i_add+'01', obj1_add)]          # obj1 cannot coexist with i_add+'01'
            obj2.ent += [(self, i_add+'10', obj2_add)]          # obj2 cannot coexist with i_add+'10'
            self.ent += [(obj1, obj1_add, i_add+'01'), (obj2, obj2_add, i_add+'10')]

        del self.qnum[i_add]
        
        # classical cases matter here
        

    '''
    Scaling up probabilities:
    A - 0.5 - found to not exist
    B - 0.25 --> (after killing A) 0.5 = 0.25/(0.25+0.25) = B/(B+C)
    C - 0.25 --> (after killing A) 0.5 
    '''

    def detangle(self, add):
        probs = 0
        all_states = list(self.qnum.keys())
        for i in all_states:
            if i.startswith(add):
                print('delete', i)
                del self.qnum[i]
            else:
                probs += self.qnum[i][1]
        for i in self.qnum:
            self.qnum[i][1] /= probs
        

    def meas(self):
        '''
            1 2 3 
        a | X Q Y
        b | R _ _
        c | Z _ W

        PIECE1
        P(b2, 0) - 1
        P.split(a2, b1)
        # final
        Q(a2, 00) - 0.5
        R(b1, 01) - 0.5

        PIECE2
        W(c3, 00) - 1/2
        X(a1, 01) - 1/2
        X.split(a3, c1)
        # final
        W(c3, 00) - 1/2
        X(a1, 0100) - 1/8
        Y(a3, 0101) - 3/16
        Z(c1, 0110) - 3/16

        PIECE2 is killer
        How to measure?
        Cannot pad 00 with zeroes, last 2 qubits can be anything (don't care condition)
        0000 - 1/4*1/2
        0001 - 1/4*1/2
        0010 - 1/4*1/2
        0011 - 1/4*1/2
        0100 - 1/8
        0101 - 3/16
        0110 - 3/16
        0111 - 0

            1     2     3     4
        0   1     1/2   9/16  9/16
        1   0     1/2   7/16  7/16
        '''

        level = 0
        for i in self.qnum:
            if len(i) > level:  
                level = len(i)

        # probs = [(0,0)]*level

        # for i in self.qnum:
        #     for j in range(0, len(i)):
        #         if self.qnum[j][0] == '0':
        #             probs[j][0] += 1
        #         else:
        #             probs[j][1] += 1

        # all_add = self.qnum.keys()
        # n = len(all_add)
        # for i in range(0, n):
        #     if all_add[i]

        ## print(level)
        

        ''' 
        states:  
        000
        001
        010
        011
        100
        101
        110
        111

        poss_states:
        00
        01
        11
        100
        101
        '''

        params = [0+0.j]*(2**(level-1))
        states = [bin(i)[2:].zfill(level-1) for i in range(0, 2**(level-1))]
        poss_states = list(self.qnum.keys())
        poss_states = [poss_states[i][1:] for i in range(0, len(poss_states))]
        
        for i in range(0, len(poss_states)):
            if(len(poss_states[i]) < level):
                index = states.index(poss_states[i] + '0'*(level - 1 - len(poss_states[i])))
                params[index] = self.qnum['0'+poss_states[i]][1]**0.5 + 0.j
        
        #Initializing:
        qr = QuantumRegister(level-1)
        cr = ClassicalRegister(level-1)
        ckt = QuantumCircuit(qr, cr)
        ckt.initialize(params, [qr[i] for i in range(level-1)])

        # init_gate = Initialize(params)
        # init_gate.label = "init"
        # ckt.append(init_gate, [i for i in range(level-1)])

        ckt.measure_all()
        ## print(ckt)
        job = execute(ckt, backend, shots = 1)
        res = job.result()
        # print(res.get_counts())
        final_state = list(res.get_counts().keys())[0][:(level-1)]
        ## print(final_state)

        ## print(all_add)

        while(True):
            if(final_state in poss_states):
                break
            final_state = final_state[:-1]
        
        final_state = '0' + final_state
        print('Final state of piece2 : ', final_state)

        ## detangle
        
        print("Piece2 ent list : ", self.ent)
        for i in range(len(self.ent)):
            if final_state.startswith(self.ent[i][2]):
                print("Piece1 ent list : ", self.ent[i][0].ent)
                print("Entangled guy's states : ", self.ent[i][0].qnum)
                self.ent[i][0].detangle(self.ent[i][1])    
                print("Entangled guy's states : ", self.ent[i][0].qnum)
                
        final_pos = self.qnum[final_state][0]
        self.qnum.clear()
        self.qnum['0'] = [final_pos, 1]
        print("States of piece2 after measuring : ", self.qnum)

# Test cases
# '''
#     1 2 3 
# a | _ _ Q
# b | P R _
# c | _ S _

# P - 00 (0.5)
# Q - 010 (0.25)
# R - 0110 (0.125)
# S - 0111 (0.125)
# '''

# piece1 = quantum_obj("a2")
# piece1.split("0", "b1", "b2")
# piece1.split("01", "a3", "c1")
# piece1.split("011", "b2", "c2")

# '''
#     1 2 3 
# a | Z _ Q
# b | P R _ 
# c | X S Y

# P - 00 (0.5)
# Q - 010 (0.25)
# R - 0110 (0.125)
# S - 0111 (0.125)

# X - 000 (1/16 = 0.0625) [ignore X since obj1==obj2 for this test case]
# Y - 00 (0.5 + 0.5*(1-0.5-0.125) = 0.6875)
# Z - 01 (0.125 + 0.5*(1-0.5-0.125) = 0.3125)

# piece1.ent - [piece2, "0", "00"]
# piece2.ent - [piece1, "00", "0"]
# '''

# piece2 = quantum_obj("c1")
# piece2.entangle_twoblock("0", "c3", "a1", piece1, "0111", piece1, "00")
# piece2.meas()

# '''
# to-do
# - restore old addresses after detangle (reduce level)
# - ent_twoblock obj1 = obj2 case: prob (both being there) = 0 [done]
# - integrate with main code
# '''