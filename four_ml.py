from four import trasform, initial_state
import four

import pickle
from sklearn.neural_network import MLPClassifier

model = pickle.load(open("four_model.sav", 'rb'))
'''
a = transform(initial_state())

print(model.predict_proba([a]))
print(model.predict([a]))
'''
def utility(state):
    if four.winner(state) == True:
        return 1
    elif four.winner(state) == False:
        return -1
    else:
        if terminal(state):
            return 0
        a = transform(state)
        val = model.predict_proba([a])
        return val[0][2] - val[0][0]
        
