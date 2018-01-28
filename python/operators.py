
def And(a,b):
    return a and b

def Or(a,b):
    return a or b

def equals(a,b):
    return a == b

def different(a,b):
    return a != b

def more(a,b):
    return a > b

def more_eq(a,b):
    return a >= b

def less(a,b):
    return a < b

def less_eq(a,b):
    return a <= b

def exists(a):
    return a not in (None,'')

def not_exists(a):
    return a in (None,'')

def difference(a,b):
    return a - b

def apply(list_terms, list_operators):
    for operator in list_operators:
        result = operator(*list_terms)
        list_terms = [result]
    return result
