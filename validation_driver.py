
#dependencias comuns
import json

#dependencias adicionais
import parsers

def run(data):
    if isinstance(data, str):
        data = json.loads(data)
    dict_doc = data['doc']
    dict_base = data['base']
    dict_rules = data['regras']

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
    return response
