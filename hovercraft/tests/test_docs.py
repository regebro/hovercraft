import manuel.doctest
import manuel.codeblock
import manuel.testing
import unittest


def additional_tests():
    m = manuel.doctest.Manuel()
    m += manuel.codeblock.Manuel()
    return manuel.testing.TestSuite(m, r'../../docs/examples/tutorial.rst')

if __name__ == '__main__':
    unittest.TextTestRunner().run(additional_tests())
