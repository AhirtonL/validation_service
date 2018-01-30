# -*- coding: utf-8 -*-

#dependencias comuns
import json, re

#dependencias adicionais
import parsers

def run(data):
    if isinstance(data, str):
        data = json.loads(data)
    dict_doc = data['doc']
    dict_base = data['base']
    try:
        dict_rules = data['regras']
    except KeyError:
        dict_rules = None

    if not dict_rules:
        dict_rules = json.loads(re.sub(r'[\t\n\r]','',open('regras.json').read()))

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
