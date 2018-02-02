# -*- coding: utf-8 -*-

import re
from datetime import datetime, timedelta
import operators

RE_NOT_NUMBER = re.compile(r'[^0-9]')

def forceNDigits(value, digits):
	if isinstance(value, int):
		value = str(value)
	zeros_to_add = digits - len(value)
	return zeros_to_add*"0" + value

def castToText(value, encoding='utf-8'):
	if isinstance(value, int):
		value = str(value)
	elif isinstance(value, unicode):
		value = value.encode(encoding)
	return value

def castToNumSeq(value):
	value = castToText(value)
	return RE_NOT_NUMBER.sub('', value)

def castToDate(value):
	value = castToText(value)
	parts = RE_NOT_NUMBER.split(value)
	parts = filter(lambda x: x, parts)
	parts = [forceNDigits(x,2) for x in parts]
	if len(parts[0]) == 4:
		parts = list(reversed(parts))
	value = ''.join(parts)
	for format_date in ('%d%m%Y','%Y%m%d','%m%d%Y'):
		try:
			return datetime.strptime(value,format_date)
		except:
			continue
	raise ValueError('Formato de data invalido: '+value)

def castToFloat(value):
	value = castToNumSeq(value)
	value = value[0:-2] + '.' + value[-2:]
	return float(value)

def castToCurrency(value):
	value = castToFloat(value)
	return str(round(value,2))

def lookupField(dyct, field, default=None):
	if '+' in field:
		to_return = ''.join([lookupField(dyct, x, default='') for x in field.split('+')])
		return to_return if to_return != '' else default
	parts = field.split('.')
	try:
		value = dyct[parts[0]] #.encode('utf-8')
	except KeyError:
		value = default
	if len(parts) == 1:
		return value
	else:
		return lookupField(value, '.'.join(parts[1:]), default)

def forceType(value, tipe):
	if value is None:
		return None
	elif tipe == 'text':
		return castToText(value)
	elif tipe == 'num_seq':
		return castToNumSeq(value)
	elif tipe == 'int':
		return int(value)
	elif tipe == 'boolean':
		return bool(value)
	elif tipe == 'float':
		return castToFloat(value)
	elif tipe == 'currency':
		return castToCurrency(value)
	elif tipe == 'date':
		return castToDate(value)
	elif tipe == 'array':
		return value.split(',')
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
			return forceType(term['value'], tipe)
		elif source == 'doc':
			return parseField(dict_doc, term['value'], tipe)
		elif source == 'base':
			return parseField(dict_base, term['value'], tipe)
		elif source == 'result':
			return results[int(term['value'])]
	except Exception as e:
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
	elif condition == 'segment':
		operator = operators.segment
	return operator
