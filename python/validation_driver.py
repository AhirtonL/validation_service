
#dependencias comuns
import sys, json, re

#dependencias adicionais
sys.path.append('dependencies.egg')
import parsers

#parseando argumentos
args = sys.argv[1:]
n_args = len(args)
if n_args == 3:
    TEXT_DOC = args[0]
    TEXT_BASE = args[1]
    TEXT_RULES = args[2]
    dict_doc = json.loads(TEXT_DOC)
    dict_base = json.loads(TEXT_BASE)
    dict_rules = json.loads(TEXT_RULES)
elif n_args == 1:
    dyct = json.loads(re.sub(r'[\t\n\r]','',open(args[0]).read()))
    dict_doc = dyct['doc']
    dict_base = dyct['base']
    dict_rules = dyct['regras']

rules_validated = []

for rule in dict_rules['rules']:
    results = []
    for condition in rule['conditions']:
        operator = parsers.parseOperator(condition['operator'])
        terms = [parsers.parseTerm(x,dict_doc,dict_base,results) for x in condition['terms']]
        try:
            result = operator(*terms)
        except:
           result = False
        results.append(result)
    rule['validation'] = results[-1]
    rules_validated.append(rule)

response = []

for rule in rules_validated:
    response.append({
        'id_regra': rule['id'],
        'description': rule['description'],
        'validated': str(rule['validation'])
    })

print response
