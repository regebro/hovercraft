import os
import unittest
from pkg_resources import resource_string
from docutils.core import publish_string
from docutils.writers.docutils_xml import Writer
from lxml import etree

from hovercraft import SlideMaker

#TEST_DATA = os.path.join(os.path.split(__file__)[0], 'test_data')

def make_tree(file_name):
    """Loads reStructuredText, outputs an lxml tree"""
    rst = resource_string(__name__, file_name)
    xml = publish_string(rst, writer=Writer())
    return etree.fromstring(xml)

class SlideMakerTests(unittest.TestCase):
    
    def test_simple(self): 
        tree = SlideMaker(make_tree('test_data/simple.rst')).walk()
        self.assertEqual(etree.tostring(tree),
            b'<document source="&lt;string&gt;"><step step="0">'\
            b'<section ids="simple-presentation" names="simple\\ presentation">'\
            b'<title>Simple Presentation</title><paragraph>This presentation '\
            b'has two slides, each with a header and some text.</paragraph>'\
            b'</section></step><step step="1"><section ids="second-slide" '\
            b'names="second\\ slide"><title>Second  slide</title><paragraph>'\
            b'There is no positioning or anything fancy.</paragraph>'\
            b'</section></step></document>')

if __name__ == '__main__':
    unittest.main()
    
    