
#dependencias comuns
import sys, json

#dependencias adicionais
import parsers

#parseando argumentos
args = sys.argv[1:]
TEXT_DOC = args[0]
TEXT_BASE = args[1]
TEXT_RULES = args[2]

dict_doc = json.loads(TEXT_DOC)
dict_base = json.loads(TEXT_BASE)
dict_rules = json.loads(TEXT_RULES)

rules_validated = []

for rule in dict_rules['rules']:
    results = []
    for condition in rule['conditions']:
        operator = parsers.parseOperator(condition['operator'])
        terms = [parsers.parseTerm(x,dict_doc,dict_base,results) for x in condition['terms']]
        results.append(operator(*terms))
    rule['validation'] = results[-1]
    rules_validated.append(rule)

response = {}

for rule in rules_validated:
    response[str(rule['id'])] = str(rule['validation'])

print response
