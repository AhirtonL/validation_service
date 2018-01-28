
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
    return a is not None

def not_exists(a):
    return a is None

def difference(a,b):
    return a - b

def apply(list_terms, list_operators):
    for operator in list_operators:
        result = operator(*list_terms)
        list_terms = [result]
    return result
