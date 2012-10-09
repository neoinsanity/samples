"""
>>> obj = WrapperClass()
The base: <class 'walkin_bases_mixin.WrapperClass'>
<BLANKLINE>
The base: <class 'walkin_bases_mixin.WalkinBasesMixin'>
WalkinBasesMixin.the_func
The base: <class 'walkin_bases_mixin.NoOpMixin'>
The base: <class 'walkin_bases_mixin.RootBaseMixin'>
RootBaseMixin.the_func
[<class 'walkin_bases_mixin.WrapperClass'>, <class 'walkin_bases_mixin.WalkinBasesMixin'>, <class 'walkin_bases_mixin.NoOpMixin'>, <class 'walkin_bases_mixin.RootBaseMixin'>]
"""
__author__ = 'neoinsanity'


class RootBaseMixin(object):
    def __init__(self):
        pass


    def the_func(self):
        print 'RootBaseMixin.the_func'


class NoOpMixin(RootBaseMixin):
    def __init__(self):
        RootBaseMixin.__init__(self)


class WalkinBasesMixin(NoOpMixin):
    def __init__(self):
        RootBaseMixin.__init__(self)

        class_hierarchy = []
        base = self.__class__ # The root in the chain
        while base is not None and base is not object:
            print 'The base:', base
            class_hierarchy.append(base)
            if 'the_func' in base.__dict__:
                base.the_func(self)
            base = base.__base__

        print str(class_hierarchy)


    def the_func(self):
        print 'WalkinBasesMixin.the_func'


class WrapperClass(WalkinBasesMixin):
    def __init__(self):
        WalkinBasesMixin.__init__(self)


    def the_func(self):
        print ''


obj = WrapperClass()
