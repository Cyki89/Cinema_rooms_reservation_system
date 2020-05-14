import unittest
import helpers

CONVERTABLE_STRING_TO_INT = '2'
NO_CONVERTABLE_STRING_TO_INT = 'Two'
CONVERTABLE_FLOAT_STRING_TO_INT = '2.0'
NO_CONVERTABLE_FLOAT_STRING_TO_INT = '2.5'


# create test foo method with decorator
@helpers.try_except_decorator
def foo(x, y):
    ''' test method'''
    return x / y


# create test Foo class with decorator
@helpers.error_handling_class_decorator
class Foo():
    '''test class '''
    def __init__(self):
        pass

    def foo(self, x,y):
        return x / y


class MyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # create instance of Foo class
        cls.obj = Foo()

    def test_parse_str_to_int(self):
        '''check if string was corrected converted to int'''
        self.assertEqual(helpers.parse_str_to_int(CONVERTABLE_STRING_TO_INT), 2)
        with self.assertRaises(ValueError):
            helpers.parse_str_to_int(NO_CONVERTABLE_STRING_TO_INT)
            helpers.parse_str_to_int(CONVERTABLE_FLOAT_STRING_TO_INT)
            helpers.parse_str_to_int(NO_CONVERTABLE_FLOAT_STRING_TO_INT)

    def test_try_except_decorator(self, func=foo):
        '''check if decorator was corectly added to function'''
        self.assertEqual(func(4,2),2)
        with self.assertRaises(Exception):
            func(4,0)

    def test_error_handling_class_decorator(self):
        '''check if decorator was corectly added to function'''

        # check function names
        self.assertEqual(Foo.__dict__['__init__'].__name__, '__init__')
        self.assertEqual(Foo.__dict__['foo'].__name__, 'wrapper')

        # check foo function inside Foo class
        self.test_try_except_decorator(self.obj.foo)

if __name__ == '__main__':
    unittest.main()
