import sys

# init
SEP = '\n'
output_file_name = 'output.txt'


class AtomicSentence(object):
    def __init__(self, name, args):
        self.name = name
        self.args = args


# function
def is_var(s=''):
    """Judge if s is a variable"""
    return s.islower()

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
            kb_map[right.name] = {right: []}
        else:
            kb_map[right.name][right] = []
    else:
        left = s_array[0].split(' && ')
        right = s_array[1]
        right = get_atomic_sentence(right)
        left_array = []
        for i in range(len(left)):
            left_array.append(get_atomic_sentence(left[i]))
        if not kb_map.has_key(right.name):
            kb_map[right.name] = {right: left_array}
        else:
            kb_map[right.name][right] = left_array


def output_line(type='', sen=AtomicSentence()):
    if type == 'ASK':
        pass
    elif type == 'True':
        pass
    elif type == 'False':
        pass

def unify(q1 = AtomicSentence(), q2 = AtomicSentence()):
    """if q1 q2 can be unified, that means their arguments can be matched
        so we use q1's args replace q2's args and store to theta
    """
    if(q1.name != q2.name): return False
    theta = {}
    for i in range(len(q1.args)):
        if is_const(q1.args[i]):
            if is_const(q2.args[i]) and q1.args[i] != q2.args[i]:
                return False
            elif is_var(q2.args[i]):
                theta[q2.args[i]] = q1.args[i]
    return theta

def compose(theta1 = {}, theta2 = {}):
    """yield new theta that has same effect to theta1 and theta2"""


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






def back_chain_list(kb_map = {}, qlist = [], theta = {}):
    """backward_chaining"""
    """ps: theta is a map, but what we return is the set of theta, which means, a set of maps"""
    answers = []
    if len(qlist) == 0: return [theta]

    q = qlist[0]

    for qi in kb_map[q.name].keys():
        thetai = unify(q, qi)
        if(thetai == False): continue
        qi_list = kb_map[q.name][qi]
        if len(qi_list) == 0: # qi is a fact
            answers.append(compose(theta, thetai))
        else: # qi is an implication
            new_answers = back_chain_list(kb_map, subst(thetai, qi_list), compose(theta, thetai))
            #answers = answers and new_answers

    for thetai in answers:
        new_answers = back_chain_list(kb_map, qlist[1:], thetai)
        if new_answers != [thetai]:
            return






















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
