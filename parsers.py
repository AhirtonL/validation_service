# -*- coding: utf-8 -*-

import re
from datetime import datetime, timedelta
import operators

def lookupField(dyct, field, default=None):
    if '+' in field:
        to_return = ''.join([str(lookupField(dyct, x, default='')) for x in field.split('+')])
        return to_return if to_return != '' else default
    parts = field.split('.')
    try:
        value = dyct[parts[0]]
    except KeyError:
        value = default
    if len(parts) == 1:
        return value
    else:
        return lookupField(value, '.'.join(parts[1:]), default)

def forceType(value, tipe):
    if value is None:
        return None
    elif tipe == 'str':
        return value.encode('utf-8')
    elif tipe == 'int':
        return int(value)
    elif tipe == 'boolean':
        return bool(value)
    elif tipe == 'float':
        if isinstance(value, str) or isinstance(value, unicode):
            value = re.sub(r'[^0-9]', '', value)
            value = value[0:-2] + '.' + value[-2:]
        return float(value)
    elif tipe == 'date':
        if len(value) == 10:
            format = '%d/%m/%Y'
        elif len(value) == 19:
            format = '%Y-%m-%d %H:%M:%S'
        return datetime.strptime(value, format)
    elif tipe == 'timedelta':
        if not isinstance(value, timedelta):
            amount, unit = value.split(' ')
            value = timedelta(**{unit: int(amount)})
        return value

def parseField(dyct, field, tipe, default=None):
    value = lookupField(dyct, field, default)
    value = forceType(value, tipe)
    return value

def parseTerm(term, dict_doc, dict_base, results):
    source = term['source']
    tipe = term['type']
    try:
        if source == 'constant':
            value = term['value']
        elif source == 'doc':
            return parseField(dict_doc, term['value'], tipe)
        elif source == 'base':
            return parseField(dict_base, term['value'], tipe)
        elif source == 'result':
            return results[int(term['value'])]
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
    elif condition == 'and':
        operator = operators.And
    elif condition == 'or':
        operator = operators.Or
    elif condition == 'mock_true':
        operator = operators.mockTrue
    return operator
