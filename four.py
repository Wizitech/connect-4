import random
import pickle
from sklearn.neural_network import MLPClassifier

model = pickle.load(open("four_model.sav", 'rb'))

MAX_SIZE = 6

def initial_state():
    return [[],
            [],
            [],
            [],
            [],
            [],
            []]

def transform(state):
    new = [[0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0]]
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j]:
                new[MAX_SIZE-j-1][i] = 1
            else:
                new[MAX_SIZE-j-1][i] = -1
    ans = []
    for i in new:
        for j in i:
            ans.append(j)
    return ans

def player(state):
    count = 0
    for i in state:
        count += len(i)
    return (count % 2 == 0)

def transpose(state):
    new = [['_','_','_','_','_','_','_'],
            ['_','_','_','_','_','_','_'],
            ['_','_','_','_','_','_','_'],
            ['_','_','_','_','_','_','_'],
            ['_','_','_','_','_','_','_'],
            ['_','_','_','_','_','_','_']]
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j]:
                new[MAX_SIZE-j-1][i] = 'X'
            else:
                new[MAX_SIZE-j-1][i] = 'O'        
    return new

def print_state(state):
    new = transpose(state)
    for i in new:
        for j in i:
            print(j, end = " ")
        print()

def actions(state):
    moves = []
    for i in range(len(state)):
        if len(state[i]) < MAX_SIZE:
            moves.append(i)
    return moves

def result(state, action):
    new = initial_state()
    for a in range(len(state)):
        for b in range(len(state[a])):
            new[a].append(state[a][b])
    new[action].append(player(state))
    return new

def winner(state):
    for i in range(len(state)):
        if len(state[i]) >= 4: # check vertical
            for j in range(len(state[i])):
                if len(state[i]) - j < 4:
                    break
                try:
                    if state[i][j] == state[i][j+1] and state[i][j+1] == state[i][j+2] and state[i][j+2] == state[i][j+3]:
                        return state[i][j]
                except:
                    pass
        #upward slant
        if i < 4:
            if len(state[i+3]) >= 4:
                for j in range(3, len(state[i+3])):
                    try:
                        if state[i+3][j] == state[i+2][j-1] and state[i+2][j-1] == state[i+1][j-2] and state[i+1][j-2] == state[i][j-3]:
                            return state[i+3][j]
                    except:
                        pass
            #downward slant
            if len(state[i]) >= 4:
                for j in range(3, len(state[i])):
                    try:
                        if state[i][j] == state[i+1][j-1] and state[i+1][j-1] == state[i+2][j-2] and state[i+2][j-2] == state[i+3][j-3]:
                            return state[i][j]
                    except:
                        pass
            #check horizontal
            for j in range(len(state[i])):
                try:
                     if state[i][j] == state[i+1][j] and state[i+1][j] == state[i+2][j] and state[i+2][j] == state[i+3][j]:
                        return state[i][j]
                except:
                    pass
            
                    
def terminal(state):
    if winner(state) != None:
        return True
    if actions(state) == []:
        return True
    return False

def utility(state):
    if winner(state) == True:
        return 1
    elif winner(state) == False:
        return -1
    else:
        if terminal(state):
            return 0
        a = transform(state)
        val = model.predict_proba([a])
        return val[0][2] - val[0][0]

depth_count = []
MAX = 5
MIN = 3
def maxi(board):
    global depth_count
    if terminal(board):
        return [utility(board)]
    v = [-2]
    depth_count.append(1)
    for action in actions(board):
        if len(depth_count) < random.randint(MIN,MAX):
            if mini(result(board, action))[0] > v[0]:
                v = [mini(result(board, action))[0], action]
        else:
            if utility(result(board, action)) > v[0]:
                v = [utility(result(board, action)), action]
    depth_count.pop(-1)
    return v
def mini(board):
    global depth_count
    if terminal(board):
        return [utility(board)]
    v = [2]
    depth_count.append(1)
    for action in actions(board):
        if len(depth_count) < random.randint(MIN,MAX):
            if maxi(result(board, action))[0] < v[0]:
                v = [maxi(result(board, action))[0], action]
        else:
            if utility(result(board, action)) < v[0]:
                v = [utility(result(board, action)), action]
    depth_count.pop(-1)
    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    global depth
    depth = 0
    if player(board) == True:
        ans = maxi(board)
        return ans[1]
    if player(board) == False:
        ans = mini(board)
        return ans[1]
