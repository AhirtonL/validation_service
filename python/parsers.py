from datetime import datetime, timedelta
import operators

def parseField(dyct, field):
    parts = field.split('.')
    value = dyct[parts[0]]
    if len(parts) == 1:
        return value
    else:
        return parseField(value, '.'.join(parts[1:]))

def parseTerm(term, dict_doc, dict_base, results):
    source = term['source']
    type = term['type']
    try:
        if source == 'constant':
            value = term['value']
        elif source == 'doc':
            value = parseField(dict_doc, term['value'])
        elif source == 'base':
            value = parseField(dict_base, term['value'])
        elif source == 'result':
            value = results[int(term['value'])]
        if type == 'str':
            return str(value)
        elif type == 'int':
            return int(value)
        elif type == 'float':
            return float(value)
        elif type == 'date':
            if len(value) == 10:
                format = '%Y-%m-%d'
            elif len(value) == 19:
                format = '%Y-%m-%d %H:%M:%S'
            return datetime.strptime(value,format)
        elif type == 'timedelta':
            if not isinstance(value, timedelta):
                amount, unit = value.split(' ')
                value = timedelta(**{unit:int(amount)})
            return value
    except:
        return None

def parseOperator(condition):
    if condition == 'equals':
        operator = operators.equals
    elif condition == 'different':
        operator = operators.different
    elif condition == 'less':
        operator = operators.less
    elif condition == 'more':
        operator = operators.more
    elif condition == 'exists':
        operator = operators.exists
    elif condition == 'not_exists':
        operator = operators.not_exists
    elif condition == 'more_eq':
        operator = operators.more_eq
    elif condition == 'less_eq':
        operator = operators.less
    elif condition == 'difference':
        operator = operators.difference
    return operator
