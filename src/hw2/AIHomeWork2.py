import sys
import copy

# init
SEP = '\n'
output_file_name = 'output.txt'
s_v_counter = 0


class AtomicSentence(object):
    def __init__(self, name = None, args = None):
        self.name = name
        self.args = args




# function
def is_var(s=''):
    """Judge if s is a variable"""
    return s[0].islower()

def is_const(s = ''):
    """Judge if s is a constant"""
    return not is_var(s)


def get_atomic_sentence(s=''):
    """Switch the string s to the class type"""
    name = s.split('(')[0]
    args = s[s.index('(') + 1: -1]
    args = args.split(', ')
    sen = AtomicSentence(name, args)
    return sen


def get_query(s=''):
    'Switch the query string s to AtomicSentence class array'
    s_array = s.split(' && ')
    qlist = []
    for i in range(len(s_array)):
        qlist.append(get_atomic_sentence(s_array[i]))
    return qlist


def get_sentence_from_kb(s='', kb_map={}):
    """Get sentence (class type) from knowledge base"""
    s_array = s.split(' => ')
    if (len(s_array) == 1):
        right = get_atomic_sentence(s_array[0])
        if not kb_map.has_key(right.name):
            kb_map[right.name] = [[right]]
        else:
            kb_map[right.name].append([right])
    else:
        left = s_array[0].split(' && ')
        right = s_array[1]
        right = get_atomic_sentence(right)
        impl_array = [right]
        for i in range(len(left)):
            left_sen = get_atomic_sentence(left[i])
            impl_array.append(left_sen)

        if not kb_map.has_key(right.name):
            kb_map[right.name] = [impl_array]
        else:
            kb_map[right.name].append(impl_array)




def unify(q1, q2, theta = {}):
    """if q1 q2 can be unified, that means their arguments can be matched
    """
    if theta is None:
        return None
    if q1.name != q2.name:
        return None
    new_theta = theta
    for i in range(len(q1.args)):
        arg1 = q1.args[i]
        arg2 = q2.args[i]
        if is_const(arg1):
            if is_const(arg2) and arg1 != arg2:
                return None
            elif is_var(arg2):
                new_theta = unify_var(arg2, arg1, new_theta)
        elif is_var(arg1):
            new_theta = unify_var(arg1, arg2, new_theta)
    return new_theta




def unify_var(var, val, theta = {}):
    if var in theta:
        if is_var(theta[var]):
            return unify_var(theta[var], val, theta)
        elif is_const(theta[var]):
            return theta
    new_theta = theta.copy()
    new_theta[var] = val
    return new_theta






def subst(theta = {}, sen = AtomicSentence()):
    """use theta to substitute qlist, return the new replaced qlist"""
    new_sen = copy.deepcopy(sen)
    for i in range(len(new_sen.args)):
        while theta.has_key(new_sen.args[i]):  ####
            new_sen.args[i] = theta[new_sen.args[i]]
    return new_sen



def standardized_variable(rule): ### problem
    """replcae all variable in rule to v1, v2... form"""
    dict = {}
    new_rule = []
    for sen in rule:
        new_sen = copy.deepcopy(sen)
        for i in range(len(new_sen.args)):
            if is_var(new_sen.args[i]):
                if new_sen.args[i] not in dict:
                    v = "v_" + str(standardized_variable.counter)
                    standardized_variable.counter = standardized_variable.counter + 1
                    dict[new_sen.args[i]] = v
                    new_sen.args[i] = v

                else:
                    new_sen.args[i] = dict[new_sen.args[i]]
        new_rule.append(new_sen)
    return new_rule
standardized_variable.counter = 0

def output_line(type='', sen=AtomicSentence(), theta = {}):
    if type != 'Ask': new_sen = subst(theta, sen)
    else: new_sen = sen
    line = type + ': ' + new_sen.name + '('
    for i in range(len(new_sen.args)):
        if i != 0: line = line + ', '
        if is_const(new_sen.args[i]):
            line = line + new_sen.args[i]
        elif is_var(new_sen.args[i]):
            line = line + '_'
    line = line + ')'
    print line
    output.write(line + SEP)




def bc_ask(kb_map = {}, query = []):
    """"""
    ans = bc_and(kb_map, query, {})
    #ans = bc_or(kb_map, query[0], {})
    return ans


def bc_or(kb_map = {}, goal = AtomicSentence(), theta = {}):
    """goal is rhs"""
    output_line('Ask', goal, theta)
    flag = False
    if not kb_map.has_key(goal.name):
        output_line("False", goal, theta)
        pass
    unified = False
    yielded = False
    first = True
    for rule in kb_map[goal.name]:
        standardized_rule = standardized_variable(rule)
        lhs = standardized_rule[1:]
        rhs = standardized_rule[0]
        uni_theta = unify(rhs, goal, theta)
        if uni_theta == None: continue
        if not first:
            output_line('Ask', goal, theta)
        for theta1 in bc_and(kb_map, lhs, uni_theta):
            flag = True
            yielded = True
            output_line('True', goal, theta1)
            yield theta1
        first = False

    if flag == False: # not yield any success theta
        output_line('False', goal, theta)


def is_reference(first, rest = []):
    """"In bc_and generator, judge if first and rest has same args"""
    for sen in rest:
        for arg in sen.args:
            if is_var(arg) and arg in first.args:
                return True
    return False


def bc_and(kb_map = {}, goals = [], theta = {}):
    """goals is lhs"""
    if theta is None:
        pass
    elif not goals:
        yield theta
    else:
        first, rest = goals[0], goals[1:]
        reference_flag = is_reference(first, rest)
        sub_first = subst(theta, first)
        for theta1 in bc_or(kb_map, sub_first, theta):
            theta2_has_solution = False
            for theta2 in bc_and(kb_map, rest, theta1):
                theta2_has_solution = True
                yield theta2
            if not reference_flag and not theta2_has_solution:
                break




























# main program

# input
#file_name = sys.argv[2]
file_name = 'samples_v4/sample05.txt'
input = open(file_name, 'r')
output = open(output_file_name, 'w')

query = input.readline().strip(SEP)
n = int(input.readline().strip(SEP))
knowledge_base = []
for i in range(n):
    knowledge_base.append(input.readline().strip(SEP))

kb_map = {}
qlist = get_query(query)
for i in range(len(knowledge_base)):
    get_sentence_from_kb(knowledge_base[i], kb_map)

t = bc_ask(kb_map, qlist)
try:
    t.next()
except StopIteration:
    output.write('False')
else:
    output.write('True')
output.close()
input.close()

