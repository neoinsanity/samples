__author__ = 'neoinsanity'


class NamedValueError(KeyError):
    """
    Thrown in the event of a key lookup error. May also be thrown due to non-existent key.
    """
    pass


class _NoDefault:
    """
    This is a flag to denote the case where no defaut value is given.
    """
    pass


class NamedValueAccessible:
    """
    This is a mix-in class that provides a uniform access to methods and attributes implemented by a child
    """


    def valueForKey(self, key, default=_NoDefault):
        '''
        Suppose key is 'foo'. This method returns the value with the following precedence:
            1. Method before non-methods
            2. Public attributes before private attributes
        More specifically, this method then returns one of the following:
            * self.foo()
            * self._foo()
            * self.foo
            * self._foo
        ... or the default, if it was specified, otherwise raises an exception.

        >>> class MethodClass(NamedValueAccessible):
        ...     def hello(self):
        ...         return 'hola'
        >>> methodClass = MethodClass()
        >>> methodClass.valueForKey("hello")
        'hola'

        >>> class HiddenMethodClass(NamedValueAccessible):
        ...     def _hello(self):
        ...         return 'hola'
        >>> hiddenMethodClass = HiddenMethodClass()
        >>> hiddenMethodClass.valueForKey('hello')
        'hola'

        >>> class AttributeClass(NamedValueAccessible):
        ...     def __init__(self):
        ...         self.hello = 'hola'
        >>> attributeClass = AttributeClass()
        >>> attributeClass.valueForKey('hello')
        'hola'

        >>> class HiddenAttributeClass(NamedValueAccessible):
        ...     def __init__(self):
        ...         self._hello = 'hola'
        >>> hiddenAttributeClass = HiddenAttributeClass()
        >>> hiddenAttributeClass.valueForKey('hello')
        'hola'

        >>> class InvalidKeyClass(NamedValueAccessible):
        ...     pass
        >>> invalidKeyClass = InvalidKeyClass()
        >>> invalidKeyClass.valueForKey('key')
        Traceback (most recent call last):
        ...
        NamedValueError: 'key'

        >>> invalidKeyClass.valueForKey('key', 'hola')
        'hola'
        '''
        assert key
        clazz = self.__class__
        under_key = '_' + key
        attr = None
        method = getattr(clazz, key, None)
        if not method:
            method = getattr(clazz, under_key, None)
            if not method:
                attr = getattr(self, key, None)
                if not attr:
                    attr = getattr(self, under_key, None)
                    if not attr:
                        if default != _NoDefault:
                            return default
                        else:
                            raise NamedValueError, key
        if method:
            return method(self)
        if attr:
            return attr

class Transaction(NamedValueAccessible):
    def logColumns(self):
        return 'datetime requestId responseSize duration'.split()
    def logEntry(self):
        ''' Returns a list of values for the transaction
    log, consistent with logColumns(). '''
        return [self.valueForKey(column)
                for column in self.logColumns()]
