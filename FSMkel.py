from random import randint


class state:
    
    def __init__(self, name, function, transition):
        self.name = name
        self.function = function
        self.transition = transition

        
class StateMachine:
    def __init__(self):
        self.stateSet = []
        self.curState = None
        self.startState = None
        self.initialized = False

        
    def addState(self, state, isStart=False):
        self.stateSet.append(state)
        if isStart:
            self.startState = state
            if self.startState is not None:
                print('start state already defined, overwriting...')

                
    def initialize(self):
        if self.initialized:
            print('can only be initialized once')
            return
        if not self.startState:
            print('set a start state')
            return
        self.curState = self.startState
        self.initialized = True

        
    def tick(self):
        if not self.initialized:
            print('initialize first')
            return False
        if not self.curState:
            print('no state')
            return False
        self.curState.function()
        self.curState = self.curState.transition()
        return True



def temp():
    return None

def stateB_transition():
    if randint(0, 1) == 0:
        return state_d
    else:
        return state_e

def stateA_transition():
    if randint(0, 1) == 0:
        return state_b
    else:
        return state_c


state_f = state('f', lambda : print('f'), temp)
state_e = state('e', lambda : print('e'), temp)
state_d = state('d', lambda : print('d'), temp)
state_c = state('c', lambda : print('c'), lambda : state_f)
state_b = state('b', lambda : print('b'), stateB_transition)
state_a = state('a', lambda : print('a'), stateA_transition)

state_f.transition = lambda : state_a

SM = StateMachine()
SM.addState(state_f)
SM.addState(state_e)
SM.addState(state_d)
SM.addState(state_c)
SM.addState(state_b)
SM.addState(state_a, True)
SM.initialize()

while SM.tick():
    pass
    
print('StateMachine Complete.')

