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
            b'<body><div id="impress" transition-duration="">'\
            b'<div class="step" step="0" data-y="0" data-x="0">'\
            b'<h1 id="simple-presentation">Simple Presentation</h1>'\
            b'<p>This presentation has two slides, each with a header and '\
            b'some text.</p></div><div class="step" step="1" data-y="0" '\
            b'data-x="1600"><h1 id="second-slide">Second slide</h1>'\
            b'<p>There is no positioning or anything fancy.</p></div></div>'\
            b'<script type="text/javascript" src="js/impress.js"></script>'\
            b'<script type="text/javascript" src="js/hovercraft-minimal.js">'\
            b'</script></body></html>'
        self.assertEqual(html, target)

    def test_big(self):
        with open(os.path.join(TEST_DATA, 'advanced.rst'), 'rb') as infile:
            rst = infile.read()
        template = get_template_info(os.path.join(TEST_DATA, 'maximal'))
        
        html = rst2html(rst, template)
        target = b'<!DOCTYPE html SYSTEM "about:legacy-compat">'\
            b'<html xmlns="http://www.w3.org/1999/xhtml">'\
            b'<head><title>Presentation title</title>'\
            b'<link rel="stylesheet" href="css/style.css" '\
            b'media="screen,print,projection"></link>'\
            b'<link rel="stylesheet" href="css/print.css" media="print"></link>'\
            b'<link rel="stylesheet" href="css/impressConsole.css" '\
            b'media="screen,projection"></link>'\
            b'<script type="text/javascript" src="js/dummy.js"></script></head>'\
            b'<body class="impress-not-supported"><div id="impress" '\
            b'transition-duration=""><div class="step" step="0" data-x="0" '\
            b'data-y="0"><h1 id="advanced-presentation">Advanced Presentation</h1>'\
            b'<p>Here we show the positioning feature, where we can '\
            b'explicitly set a position\non one of the steps.</p></div>'\
            b'<div class="step" step="1" data-y="0" data-x="1600">'\
            b'<h1 id="formatting">Formatting</h1><p>Let us also try some '\
            b'basic formatting, like <em>italic</em>, and <strong>bold</strong>.'\
            b'</p><ul><li>We can also</li><li>have a list</li><li>of things.</li>'\
            b'</ul></div><div class="step" step="2" data-y="0" data-x="3200">'\
            b'</div><div class="step" step="3" data-y="0" data-x="4800"></div>'\
            b'<div class="step" step="4" data-y="0" data-x="6400">'\
            b'<h1 id="character-sets">Character sets</h1><p>The character set is '\
            b'UTF-8 as of now. Like this: &#xE5;&#xE4;&#xF6;.</p></div></div>'\
            b'<script type="text/javascript" src="js/impress.js"></script>'\
            b'<script type="text/javascript" src="js/impressConsole.js"></script>'\
            b'<script type="text/javascript" src="js/hovercraft.js"></script>'\
            b'</body></html>'
        
        self.assertEqual(html, target)

if __name__ == '__main__':
    unittest.main()
    
    