import os
import unittest
from lxml import etree

from hovercraft.generate import rst2html
from hovercraft.template import get_template_info

TEST_DATA = os.path.join(os.path.split(__file__)[0], 'test_data')

class GeneratorTests(unittest.TestCase):
    
    def test_small(self):
        pass
        #rst = resource_string(os.path.join(TEST_DATA, 'simple.rst'))
        #template = template_info(os.path.join(TEST_DATA, 'minimal'))
        
        #html = rst2html(rst, template)

if __name__ == '__main__':
    unittest.main()
    
    