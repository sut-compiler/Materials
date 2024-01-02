import re
import json
import os


# you can uncomment this once you have
# made sure bison 3.8.2 is installed.
os.system('bison grammar.y --report=all')
os.system('rm grammar.tab.c')


def correct_form(token):
    token = re.sub('[\'"]', '', token)
    if token == '$end':
        return '$'
    return token


f = open("grammar.output", "r")
content = f.read()
content = content.replace('ε', 'epsilon')
f.close()
x = content.split('\n\n\n')

table = {'terminals': [], 'non_terminals': [], 'first': {}, 'follow': {}, 'grammar': {}, 'parse_table': {}}

# extract grammar rules
for rule in x[0].split('\n\n')[1:]:
    rule_number = None
    non_terminal = None
    flag = False
    s = []
    for t in rule.split():
        if t.isnumeric():
            rule_number = int(t)
            flag = True
        elif flag and not non_terminal:
            non_terminal = correct_form(t.replace(':', ''))
        elif t == '|':
            table['grammar'][rule_number - 1] = [non_terminal, '->'] + s
            s = []
        else:
            s.append(correct_form(t))
    table['grammar'][rule_number] = [non_terminal, '->'] + s

# extract terminals
for terminal in x[1].split('\n')[2:]:
    t = correct_form(terminal.split()[0])
    if t != 'error':  # bison adds an error terminal to the grammar
        table['terminals'].append(t)

# extract non terminals
for non_terminal in x[2].split('\n')[2:]:
    nt = correct_form(non_terminal.split()[0])
    if nt != 'on':
        table['non_terminals'].append(nt)


# create first and follow set
# bison does not show which non-terminal to reduce at
# so we need the follow set of the non-terminals

def union(x1, x2):
    n = len(x1)
    x1 |= x2
    return len(x1) != n


first = {i: set() for i in table['non_terminals']}
first.update((i, {i}) for i in table['terminals'])
follow = {i: set() for i in table['non_terminals']}
follow['program'] = set('$')
epsilon = set()
while True:
    updated = False

    for rule in table['grammar'].values():
        nt, expression = rule[0], rule[2:]

        # first
        for symbol in expression:
            if symbol == 'epsilon':
                updated |= union(epsilon, {nt})
                break
            updated |= union(first[nt], first[symbol])
            if symbol not in epsilon:
                break

        # follow
        aux = follow[nt]
        for symbol in reversed(expression):
            if symbol == 'epsilon':
                break
            if symbol in follow:
                updated |= union(follow[symbol], aux)
            if symbol in epsilon:
                aux = aux.union(first[symbol])
            else:
                aux = first[symbol]

    if not updated:
        break

table['first'] = first
table['follow'] = follow

# create the parse table
for state, content in enumerate(x[3:]):
    table['parse_table'][state] = {}
    if '$default  accept' in content:
        table['parse_table'][state]['$'] = 'accept'
        continue
    shifts = re.findall(r"(\S*)\s*shift, and go to state (\d+)", content)
    gotos = re.findall(r"  (\S*)\s*go to state (\d+)", content)
    reduces = re.findall(r"reduce using rule (\d+) \S*", content)
    for terminal, dst in shifts:
        table['parse_table'][state][correct_form(terminal)] = f'shift_{dst}'
    for non_terminal, dst in gotos:
        table['parse_table'][state][correct_form(non_terminal)] = f'goto_{dst}'
    for reduce_rule in reduces:
        nt = table['grammar'][int(reduce_rule)][0]
        for symbol in table['follow'][nt]:
            table['parse_table'][state][correct_form(symbol)] = f'reduce_{reduce_rule}'

# create a json file containing the information
# set are not json serializable, so we convert them to lists
for t in table['non_terminals'] + table['terminals']:
    table['first'][t] = list(table['first'][t])
    if t in table['follow']:
        table['follow'][t] = list(table['follow'][t])
json_object = json.dumps(table, indent=4)
with open("table.json", "w") as outfile:
    outfile.write(json_object)
