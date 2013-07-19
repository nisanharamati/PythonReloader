import imp
def load_func(filename, funcname='func'):
    _m = imp.load_source('_m', filename)
    return getattr(_m, funcname)