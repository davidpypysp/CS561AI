# init

import copy

task = 0
player = 'O'
depth = 0
grid_state = [['' for col in range(5)] for row in range(5)]
grid_score = [[0 for col in range(5)] for row in range(5)]
dir = [[1, 0], [0, -1], [0, 1], [-1, 0]]
infinite = 1000000


#function
def is_in_bound(pos):


    "check if pos is not over bound"
    return 0 <= pos[0] < 5 and 0 <= pos[1] < 5

def is_occupied(pos, grid_state):
    "check if pos is occupied"
    return not grid_state[pos[0]][pos[1]] == '*'

def is_same_side(pos, grid_state):
    "check if pos is in the same side of our player"
    return grid_state[pos[0]][pos[1]] == player

def get_opponent(player):
    "return the opponent player"
    if(player == 'O'): return 'X'
    return 'O'

def get_adjacent_nodes(pos, grid_state, player, same_side_flag):
    "return the adjacent nodes refer same_side_flag"
    nodes = []
    for k in range(4):
        adj_pos = [pos[0] + dir[k][0], pos[1] + dir[k][1]]
        if(is_in_bound(adj_pos) and is_occupied(adj_pos, grid_state)):
            if(same_side_flag and grid_state[adj_pos[0]][adj_pos[1]] == player): nodes.append(adj_pos)
            elif(not same_side_flag and grid_state[adj_pos[0]][adj_pos[1]] == get_opponent(player)): nodes.append(adj_pos)
    return nodes

def is_raid(pos, grid_state):
    "judge if this pos can act a raid"
    return len(get_adjacent_nodes(pos, grid_state, player, True)) > 0

def get_available_nodes(grid_state):
    "search all available nodes can move in the given direction"
    nodes = []
    add = 1
    x = 0
    for y in range(5):
        for k in range(5):
            if is_occupied([y, x], grid_state) == False: nodes.append([y, x])
            if k != 4: x += add
            else: add = -add
    return nodes

def evaluation(grid_state):
    "evaluation function"
    e = 0
    for y in range(5):
        for x in range(5):
            pos = [y, x]
            if is_occupied(pos, grid_state):
                if is_same_side(pos, grid_state): e += grid_score[pos[0]][pos[1]]
                else: e -= grid_score[pos[0]][pos[1]]
    return e

def get_new_state(pos, grid_state, same_side_flag):
    "make a move in the 'pos' to get the new state"
    side = player
    if same_side_flag == False: side = get_opponent(player)
    new_state = copy.deepcopy(grid_state)
    new_state[pos[0]][pos[1]] = side
    if is_raid(pos, grid_state):
        adj_nodes = get_adjacent_nodes(pos, new_state, side, False)
        for new_pos in adj_nodes:
            new_state[new_pos[0]][new_pos[1]] = side
    return new_state

def greedy(grid_state):
    "greedy algorithm to get the target_pos"
    target_pos = [0, 0]
    e = evaluation(grid_state)
    maxe = e
    for pos in get_available_nodes(grid_state):
        if is_raid(pos, grid_state): # raid move
            raid_e = e
            adj_nodes = get_adjacent_nodes(pos, grid_state, player, False)
            for node in adj_nodes:
                raid_e += grid_score[node[0]][node[1]]
            if raid_e > maxe:
                maxe = raid_e
                target_pos = copy.copy(pos)
        else: # sneak move
            if e + grid_score[pos[0]][pos[1]] > maxe:
                maxe = e + grid_score[pos[0]][pos[1]]
                target_pos = copy.copy(pos)
    new_state = get_new_state(target_pos, grid_state, True)
    return new_state



def move(depth, grid_state, max_flag):
    "minimax algorithm"
    if depth == 0: return [evaluation(grid_state), grid_state]
    target_state = copy.copy(grid_state)
    if(max_flag == True): # max_flag also means our side move
        max_score = -infinite
        for node in get_available_nodes(grid_state):
            new_state = get_new_state(node, grid_state, True)
            new_state_score = move(depth - 1, new_state, False)[0] # recursive search, this round we use Min
            if new_state_score > max_score:
                max_score = new_state_score
                target_state = copy.copy(new_state)
        return [max_score, target_state]
    else: # min and opponent side's move
        min_score = infinite
        for node in get_available_nodes(grid_state):
            new_state = get_new_state(node, grid_state, False)
            new_state_score = move(depth - 1, new_state, True)[0]
            if new_state_score < min_score:
                min_score = new_state_score
                target_state = copy.copy(new_state)
        return [min_score, target_state]


def alphabeta_move(depth, grid_state, a, b, max_flag):
    "alphabeta algorithm action"
    if(depth == 0): return [evaluation(grid_state), grid_state]
    target_state = copy.copy(grid_state)
    if max_flag == True:
        max_score = -infinite
        for node in get_available_nodes(grid_state):
            new_state = get_new_state(node, grid_state, True)
            new_state_score = alphabeta_move(depth - 1, new_state, a, b, False)
            if(new_state_score > max_score):
                max_score = new_state_score
                target_state = new_state
            a = max(a, max_score)
            if(b <= a): break; # b cut-off
            return [max_score, target_state]
    else:
        min_score = infinite
        for node in get_available_nodes(grid_state):
            new_state = get_new_state(node, grid_state, False)
            new_state_score = alphabeta_move(depth - 1, new_state, a, b, True)
            if(new_state_score < min_score):
                min_score = new_state_score
                target_state = new_state
            b = min(b, min_score)
            if(b <= a): break # a cut-off
        return [min_score, target_state]









#input
filename = 'data/3/input.txt'
input = open(filename, 'r')
task = int(input.readline().strip('\n'))
player = input.readline().strip('\n')
depth = int(input.readline().strip('\n'))
for i in range(5):
    temp = input.readline().strip('\n').split(' ')
    for j in range(5):
        grid_score[i][j] = int(temp[j])
for i in range(5):
    temp = input.readline().strip('\n')
    for j in range(5):
        grid_state[i][j] = temp[j]


input.close()

print task
print player
print depth
for i in range(5):
    for j in range(5):
        print grid_score[i][j],
    print
for i in range(5):
    temp = ''
    for j in range(5):
        temp += grid_state[i][j]
    print temp






#calculate
if task == 1:
    target_state = greedy(grid_state)
elif task == 2:
    target_state = move(depth, grid_state, True)[1]
elif task == 3:
    target_state = alphabeta_move(depth, grid_state, -infinite, infinite, True)[1]


print "Result: "
for i in range(5):
    temp = ''
    for j in range(5):
        temp += target_state[i][j]
    print temp





