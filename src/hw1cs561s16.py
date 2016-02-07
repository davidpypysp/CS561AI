# init
import copy
import sys
import os

infinity = 65536
grid_score = [[0 for col in range(5)] for row in range(5)]
adjacent_dir = [[1, 0], [0, -1], [0, 1], [-1, 0]]
X = ['A', 'B', 'C', 'D', 'E']
traverse_log_output = 0
next_state_output = 0
trace_state_output = 0
part2_flag = False


# function

def get_node(pos):
    "return node description of a position"
    return X[pos[1]] + str(pos[0] + 1)


def is_in_bound(pos):
    "check if pos is not over bound"
    return 0 <= pos[0] < 5 and 0 <= pos[1] < 5

def is_full(state):
    "check if the board is all occupied "
    for y in range(5):
        for x in range(5):
            if state[y][x] == '*': return False
    return True


def is_occupied(pos, state):
    "check if pos is occupied"
    return not state[pos[0]][pos[1]] == '*'

def is_same_side(pos, state, player):
    "check if pos is in the same side of our player"
    return player == state[pos[0]][pos[1]]

def get_opponent(player):
    "return the opponent player"
    if(player == 'O'): return 'X'
    else: return 'O'

def get_adjacent_pos_array(pos, state, player, same_side_flag):
    "return the adjacent nodes refer same_side_flag"
    pos_array = []
    for k in range(4):
        adj_pos = [pos[0] + adjacent_dir[k][0], pos[1] + adjacent_dir[k][1]]
        if(is_in_bound(adj_pos) and is_occupied(adj_pos, state)):
            if(same_side_flag and state[adj_pos[0]][adj_pos[1]] == player): pos_array.append(adj_pos)
            elif(not same_side_flag and state[adj_pos[0]][adj_pos[1]] == get_opponent(player)): pos_array.append(adj_pos)
    return pos_array

def is_raid(pos, state, player):
    "judge if this pos can act a raid for the player"
    return len(get_adjacent_pos_array(pos, state, player, True)) > 0

def get_available_pos_array(state):
    "search all available nodes can move in the given direction"
    pos_array = []
    add = 1
    for y in range(5):
        for x in range(5):
            if is_occupied([y, x], state) == False: pos_array.append([y, x])
    return pos_array


def evaluation(state, player):
    "evaluation function"
    e = 0
    for y in range(5):
        for x in range(5):
            pos = [y, x]
            if is_occupied(pos, state):
                if is_same_side(pos, state, player): e += grid_score[pos[0]][pos[1]]
                else: e -= grid_score[pos[0]][pos[1]]
    return e

def get_new_state(pos, state, player):
    "make a move for player in the 'pos' to get the new state"
    new_state = copy.deepcopy(state)
    new_state[pos[0]][pos[1]] = player
    if is_raid(pos, state, player):
        adj_pos_array = get_adjacent_pos_array(pos, state, player, False)
        for adj_pos in adj_pos_array:
            new_state[adj_pos[0]][adj_pos[1]] = player
    return new_state

def greedy(state, player):
    "greedy algorithm to get the new state"
    target_pos = [0, 0]
    e = evaluation(state, player)
    max_e = e
    for pos in get_available_pos_array(state):
        if is_raid(pos, state, player): #raid
            raid_e = e + grid_score[pos[0]][pos[1]]
            adj_pos_array = get_adjacent_pos_array(pos, state, player, False)
            for adj_pos in adj_pos_array:
                raid_e += grid_score[adj_pos[0]][adj_pos[1]] * 2
            if raid_e > max_e:
                max_e = raid_e
                target_pos = copy.copy(pos)
        else: #sneak
            if e + grid_score[pos[0]][pos[1]] > max_e:
                max_e = e + grid_score[pos[0]][pos[1]]
                target_pos = copy.copy(pos)
    new_state = get_new_state(target_pos, state, player)
    # print new_state
    return new_state

def to_infinity(value):
    "if value == infinity, turn to 'Infinity' or '-Infinity' string form"
    if value == infinity: value = 'Infinity'
    elif value == -infinity: value = '-Infinity'
    else: value = str(value)
    return value


def minimax_traverse_output(node, depth, value):
    "for traverse log output line"
    if part2_flag: return
    value = to_infinity(value)
    line = '\n' + node + ',' + str(depth) + ',' + value
    traverse_log_output.write(line)



def minimax(node, cur, depth, state, player, max_flag):
    "minimax algorithm"
    best_value = -infinity
    if max_flag == False: best_value = infinity
    if cur == depth or is_full(state): best_value = evaluation(state, player)

    minimax_traverse_output(node, cur, best_value)

    if cur == depth or is_full(state): return [best_value, state]
    target_state = copy.deepcopy(state)
    if(max_flag == True):
        for pos in get_available_pos_array(state):
            new_state = get_new_state(pos, state, player)
            new_node = get_node(pos)
            v = minimax(new_node, cur + 1, depth, new_state, player, False)[0]
            if v > best_value:
                best_value = v
                target_state = copy.deepcopy(new_state)

            minimax_traverse_output(node, cur, best_value)

        return [best_value, target_state]
    else:
        for pos in get_available_pos_array(state):
            new_state = get_new_state(pos, state, get_opponent(player))
            new_node = get_node(pos)
            v = minimax(new_node, cur + 1, depth, new_state, player, True)[0]
            if v < best_value:
                best_value = v
                target_state = copy.deepcopy(new_state)

            minimax_traverse_output(node, cur, best_value)

        return [best_value, target_state]

def alphabeta_traverse_output(node, depth, value, a, b):
    "alphabeta traverse output one line"
    if part2_flag: return
    value = to_infinity(value)
    a = to_infinity(a)
    b = to_infinity(b)
    line = '\n' + node + ',' + str(depth) + ',' + value + ',' + a + ',' + b
    traverse_log_output.write(line)



def alphabeta(node, cur, depth, state, player, a, b, max_flag):
    "alphabeta algorithm"
    best_value = -infinity
    if max_flag == False: best_value = infinity
    if cur == depth or is_full(state): best_value = evaluation(state, player)

    alphabeta_traverse_output(node, cur, best_value, a, b)

    if cur == depth or is_full(state): return [best_value, state]
    target_state = copy.deepcopy(state)
    if max_flag == True:
        for pos in get_available_pos_array(state):
            new_state = get_new_state(pos, state, player)
            new_node = get_node(pos)
            v = alphabeta(new_node, cur + 1, depth, new_state, player, a, b, False)[0]
            if v > best_value:
                best_value = v
                target_state = copy.deepcopy(new_state)
            prev_a = a
            a = max(a, best_value)
            if b <= a:
                alphabeta(node, cur, best_value, prev_a, b)
                break
            alphabeta_traverse_output(node, cur, best_value, a, b)
        return [best_value, target_state]
    else:
        for pos in get_available_pos_array(state):
            new_state = get_new_state(pos, state, get_opponent(player))
            new_node = get_node(pos)
            v = alphabeta(new_node, cur + 1, depth, new_state, player, a, b, True)[0]
            if v < best_value:
                best_value = v
                target_state = copy.deepcopy(new_state)
            #print
            prev_b = b
            b = min(b, best_value)
            if b <= a:
                alphabeta_traverse_output(node, cur, best_value, a, prev_b)
                break
            alphabeta_traverse_output(node, cur, best_value, a, b)
        return [best_value, target_state]










# input
#filename = 'data/5/input.txt'
filename = sys.argv[2]
input = open(filename, 'r')
task = int(input.readline().strip('\n'))
if task != 4: # part1
    player = input.readline().strip('\n')
    depth = int(input.readline().strip('\n'))
    for i in range(5):
        line = input.readline().strip('\n').split(' ')
        for j in range(5):
            grid_score[i][j] = int(line[j])
    init_state = [['*' for col in range(5)] for row in range(5)]
    for i in range(5):
        line = input.readline().strip('\n')
        for j in range(5):
            init_state[i][j] = line[j]
    input.close()

    # calculate
    traverse_log_output = open('traverse_log.txt', 'w')
    next_state_output = open('next_state.txt', 'w')
    if task == 1:
        target_state = greedy(init_state, player)
    elif task == 2:
        traverse_log_output.write('Node,Depth,Value')
        target_state = minimax('root', 0, depth, init_state, player, True)[1]
    elif task == 3:
        traverse_log_output.write('Node,Depth,Value,Alpha,Beta')
        target_state = alphabeta('root', 0, depth, init_state, player, -infinity, infinity, True)[1]

    # result output to next_state.txt
    first_line_flag = True
    for i in range(5):
        line = ''
        if first_line_flag == True:
            first_line_flag = False
        else:
            line += '\n'
        for j in range(5):
            line += target_state[i][j]
        next_state_output.write(line)
    traverse_log_output.close()
    next_state_output.close()

else: # part2
    part2_flag = True

    # input
    player1 = input.readline().strip('\n')
    algo1 = int(input.readline().strip('\n'))
    depth1 = int(input.readline().strip('\n'))
    player2 = input.readline().strip('\n')
    algo2 = int(input.readline().strip('\n'))
    depth2 = int(input.readline().strip('\n'))
    for i in range(5):
        line = input.readline().strip('\n').split(' ')
        for j in range(5):
            grid_score[i][j] = int(line[j])
    init_state = [['*' for col in range(5)] for row in range(5)]
    for i in range(5):
        line = input.readline().strip('\n')
        for j in range(5):
            init_state[i][j] = line[j]
    input.close()

    # calculate
    traverse_log_output = open('traverse_log.txt', 'w')
    trace_state_output = open('trace_state.txt', 'w')
    state = copy.deepcopy(init_state)
    player1_turn = True
    first_line_flag = True
    while is_full(state) == False:
        if player1_turn:
            player = player1
            algo = algo1
            depth = depth1
        else:
            player = player2
            algo = algo2
            depth = depth2
        if algo == 1:
            state = greedy(state, player)
        elif algo == 2:
            state = minimax('root', 0, depth, state, player, True)[1]
        elif algo == 3:
            state == alphabeta('root', 0, depth, state, player, -infinity, infinity, True)[1]

        # output to trace_state.txt
        for y in range(5):
            line = ''
            if first_line_flag == False:
                line += '\n'
            first_line_flag = False
            for x in range(5):
                line += state[y][x]
            trace_state_output.write(line)

        player1_turn = not player1_turn

    traverse_log_output.close()
    trace_state_output.close()






















