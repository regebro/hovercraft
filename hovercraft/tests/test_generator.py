import os
import unittest
from lxml import etree

from hovercraft.generate import rst2html
from hovercraft.template import get_template_info, template_info_node

TEST_DATA = os.path.join(os.path.split(__file__)[0], 'test_data')

class GeneratorTests(unittest.TestCase):
    """Tests that the resulting HTML is correct.
    
    This tests the whole path except the copying of files."""
    
    def test_small(self):
        with open(os.path.join(TEST_DATA, 'simple.rst'), 'rb') as infile:
            rst = infile.read()
        template = get_template_info(os.path.join(TEST_DATA, 'minimal'))
        
        html = rst2html(rst, template)
        target = b'<!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml">'\
            b'<body><div id="impress" '\
            b'transition-duration=""><div class="step" step="0" data-y="0" '\
            b'data-x="0"><h1 id="simple-presentation">Simple Presentation</h1>'\
            b'<p>This presentation has two slides, each with a header and '\
            b'some text.</p></div><div class="step" step="1" data-y="0" '\
            b'data-x="1600"><h1 id="second-slide">Second slide</h1>'\
            b'<p>There is no positioning or anything fancy.</p></div></div>'\
            b'<script src="js/impress.js"></script>'\
            b'<script src="js/hovercraft-minimal.js"></script></body></html>'
        import pdb;pdb.set_trace()
        self.assertEqual(html, target)

    def test_big(self):
        with open(os.path.join(TEST_DATA, 'advanced.rst'), 'rb') as infile:
            rst = infile.read()
        template = get_template_info(os.path.join(TEST_DATA, 'maximal'))
        
        html = rst2html(rst, template)
        target = b'<!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml">'\
            b'<head><title></title></head><body '\
            b'class="impress-not-supported"><div id="impress" '\
            b'transition-duration=""><div class="step" step="0" data-y="0" '\
            b'data-x="0"><h1 id="simple-presentation">Simple Presentation</h1>'\
            b'<p>This presentation has two slides, each with a header and '\
            b'some text.</p></div><div class="step" step="1" data-y="0" '\
            b'data-x="1600"><h1 id="second-slide">Second slide</h1>'\
            b'<p>There is no positioning or anything fancy.</p></div></div>'\
            b'<script src="js/impress.js"></script>'\
            b'<script src="js/hovercraft-minimal.js"></script></body></html>'
        self.assertEqual(html, target)

if __name__ == '__main__':
    unittest.main()
    
    