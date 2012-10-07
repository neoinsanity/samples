"""
In the first example, dynamic binding of mixin functionality is demonstrated. This is done by adding the
HelloMixin.hello() method to the Foo class at runtime.

To begin we see what error occurs when the mthod is not available to instances of Foo.
>>> foo = Foo()
>>> foo.hello()
Traceback (most recent call last):
...
AttributeError: Foo instance has no attribute 'hello'

Next the HelloMixin class is added to the bases of the
>>> Foo.__bases__ += (HelloMixin,)
>>> foo.hello()
Hello

Note that the class is added to the Foo.bases__ with a += so as not to override any existing base class behavior.

It is also possible to construct classes with HelloMixin behavior as in the Bar example.
>>> bar = Bar()
>>> bar.hello()
Hello
"""
__author__ = 'neoinsanity'


class HelloMixin:
    def hello(self):
        print 'Hello'


class Foo:
    pass


class Bar(HelloMixin):
    pass
