import sys

# init
SEP = '\n'
output_file_name = 'output.txt'
s_v_counter = 0

class AtomicSentence(object):
    def __init__(self, name, args):
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
    q = []
    for i in range(len(s_array)):
        q.append(get_atomic_sentence(s_array[i]))
    return q


def get_sentence_from_kb(s='', kb_map={}):
    """Get sentence (class type) from knowledge base"""
    s_array = s.split(' => ')
    if (len(s_array) == 1):
        right = get_atomic_sentence(s_array[0])
        if not kb_map.has_key(right.name):
            kb_map[right.name] = [right]
        else:
            kb_map[right.name].append[right]
    else:
        left = s_array[0].split(' && ')
        right = s_array[1]
        right = get_atomic_sentence(right)
        impl_array = [right]
        for i in range(len(left)):
            impl_array.append(get_atomic_sentence(left[i]))
        if not kb_map.has_key(right.name):
            kb_map[right.name] = impl_array
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
                new_theta = unify(arg2, arg1, new_theta)
        elif is_var(arg1):
            new_theta = unify(arg1, arg2, new_theta)
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


def compose(theta1 = {}, theta2 = {}):
    """yield new theta that has same effect to theta1 and theta2"""

    # SUBST(COMPOSE(theta1, theta2), p) = SUBST(theta2, SUBST(theta1, p))

    compose_theta = {}
    for l in theta1.keys():
        if(theta2.has_key(theta1[l])):
            compose_theta[l] = theta2[theta1[l]]

    for l in theta2.keys():
        if(not theta1.has_key(l)):
            compose_theta[l] = theta2[l]





def subst(theta = {}, qlist = []):
    """use theta to substitute qlist, return the new replaced qlist"""
    new_qlist = []
    for qi in qlist:
        new_qi = AtomicSentence(qi.name, qi.args)
        for i in range(len(qi.args)):
            if(theta.has_key(qi.args[i])):
                qi.args[i] = theta[qi.args[i]]
        new_qlist.append(new_qi)
    return new_qi



def standardized_variable(rule):
    """replcae all variable in rule to v1, v2... form"""
    dict = {}
    new_rule = []
    for sen in rule:
        new_sen = AtomicSentence(sen.name, sen.args)
        for i in range(len(sen.args)):
            if is_const(sen.args): continue
            if sen.args[i] not in dict:
                v = "v_" + str(s_v_counter)
                s_v_counter = s_v_counter + 1
                dict[sen.args[i]] = v
                new_sen.args[i] = v

            else:
                new_sen.args[i] = dict[sen.args[i]]
        new_rule.append(new_sen)
    return new_rule


def output_line(type='', sen=AtomicSentence(), theta = {}):
    new_sen = subst(theta, sen)
    line = type + ': ' + new_sen.name + '('
    for i in range(len(new_sen.args)):
        if i != 0: line = line + ', '
        if is_const(new_sen.args[i]):
            line = line + sen.args[i]
        elif is_var(new_sen.args[i]):
            line = line + '_'
    line = line + ')'

    output.write(line)




def bc_ask(kb_map = {}, query = []):
    """"""
    return bc_or(kb_map, query, {})


def bc_or(kb_map = {}, goal = AtomicSentence(), theta = {}):
    """goal is rhs"""
    output_line('ASK', goal, theta)
    if not kb_map.has_key(goal.name):
        output_line("False", goal, theta)
    flag = False
    for rule in kb_map[goal.name]:
        standardized_rule = standardized_variable(rule)
        lhs = standardized_rule[1:]
        rhs = standardized_rule[0]
        for theta1 in bc_and(kb_map, lhs, unify(rhs, goal, theta)):
            flag = True
            output_line('True', goal, theta1)
            yield theta1
    if flag == False:
        output_line('False', goal, theta)





def bc_and(kb_map = {}, goals = [], theta = {}):
    """goals is lhs"""
    if theta is None:
        pass
    elif not goals:
        yield theta
    else:
        first, rest = goals[0], goals[1:]
        for theta1 in bc_or(kb_map, subst(theta, first), theta):
            for theta2 in bc_and(kb_map, rest, theta1):
                yield theta2


























# main program

# input
file_name = sys.argv[2]
input = open(file_name, 'r')
output = open(output_file_name, 'w')

query = input.readline().strip(SEP)
n = int(input.readline().strip(SEP))
knowledge_base = []
for i in range(n):
    knowledge_base.append(input.readline().strip(SEP))

kb_map = {}
q = get_query(query)
for i in range(len(knowledge_base)):
    get_sentence_from_kb(knowledge_base[i], kb_map)
