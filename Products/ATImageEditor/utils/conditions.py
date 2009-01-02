
def between(one, two):
    def con(val):
        assert val >= one and val <= two, "Value is not between %s and %s" % (one, two)
        
    return con
    
def precondition(precondition, use_conditions=True):
    """
    copied decorator from http://wiki.python.org/moin/PythonDecoratorLibrary#head-e1a9273f88f2fc4e39faf297279f4d1dc8b2ae66
    """
    return conditions(precondition, None, use_conditions)
 
def postcondition(postcondition, use_conditions=True):
    """
    copied decorator from http://wiki.python.org/moin/PythonDecoratorLibrary#head-e1a9273f88f2fc4e39faf297279f4d1dc8b2ae66
    """
    return conditions(None, postcondition, use_conditions)
 
class conditions(object):
    """
    copied decorator from http://wiki.python.org/moin/PythonDecoratorLibrary#head-e1a9273f88f2fc4e39faf297279f4d1dc8b2ae66
    """
    __slots__ = ('__precondition', '__postcondition')
    
    def __init__(self, pre, post, use_conditions=True):
        if not use_conditions:
            pre, post = None, None

        self.__precondition  = pre
        self.__postcondition = post

    def __call__(self, function):
        # combine recursive wrappers (@precondition + @postcondition == @conditions)
        pres  = set((self.__precondition,))
        posts = set((self.__postcondition,))
        
        # unwrap function, collect distinct pre-/post conditions
        while type(function) is FunctionWrapper:
            pres.add(function._pre)
            posts.add(function._post)
            function = function._func

        # filter out None conditions and build pairs of pre- and postconditions
        conditions = map(None, filter(None, pres), filter(None, posts))
        
        # add a wrapper for each pair (note that 'conditions' may be empty)
        for pre, post in conditions:
            function = FunctionWrapper(pre, post, function)
            
        return function
        
class FunctionWrapper(object):
    """
    copied decorator from http://wiki.python.org/moin/PythonDecoratorLibrary#head-e1a9273f88f2fc4e39faf297279f4d1dc8b2ae66
    """
    def __init__(self, precondition, postcondition, function):
        self._pre  = precondition
        self._post = postcondition
        self._func = function

    def __call__(self, *args, **kwargs):
        precondition  = self._pre
        postcondition = self._post

        if precondition:
            precondition(*args, **kwargs)
        result = self._func(*args, **kwargs)
        if postcondition:
            postcondition(result, *args, **kwargs)
        return result