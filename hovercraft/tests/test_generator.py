import os
import unittest

from hovercraft.generate import rst2html
from hovercraft.template import get_template_info

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
            b'<body><div id="impress">'\
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
            b'<html xmlns="http://www.w3.org/1999/xhtml"><head><title>'\
            b'Presentation title</title><link rel="stylesheet" '\
            b'href="css/style.css" media="all"></link>'\
            b'<link rel="stylesheet" href="css/print.css" media="print">'\
            b'</link><link rel="stylesheet" href="css/impressConsole.css" '\
            b'media="screen,projection"></link><script type="text/javascript" '\
            b'src="js/dummy.js"></script></head><body '\
            b'class="impress-not-supported"><div id="impress" '\
            b'data-transition-duration="2000"><div class="step" step="0" data-x="0" '\
            b'data-y="0"><h1 id="advanced-presentation">Advanced Presentation'\
            b'</h1><p>Here we show the positioning feature, where we can '\
            b'explicitly set a position\non one of the steps.</p></div><div '\
            b'class="step" step="1" data-y="0" data-x="1600"><h1 '\
            b'id="formatting">Formatting</h1><p>Let us also try some basic '\
            b'formatting, like <em>italic</em>, and <strong>bold</strong>.</p>'\
            b'<ul><li>We can also</li><li>have a list</li><li>of things.</li>'\
            b'</ul></div><div class="step" step="2" data-y="0" data-x="3200">'\
            b'<pre>There should also be possible to '\
            b'have\npreformatted text for code.\n\nThis slide has only code, '\
            b'and the next step\nhas only an image. This is necessary for\n'\
            b'many types of presentations.</pre></div><div class="step" '\
            b'step="3" data-y="0" data-x="4800"><img '\
            b'src="images/python-logo-master-v3-TM.jpg" alt="" width="" '\
            b'height=""></img></div><div class="step" step="4" data-y="0" '\
            b'data-x="6400"><h1 id="character-sets">Character sets</h1>'\
            b'<p>The character set is UTF-8 as of now. Like this: '\
            b'&#xE5;&#xE4;&#xF6;.</p></div></div><script '\
            b'type="text/javascript" src="js/impress.js"></script><script '\
            b'type="text/javascript" src="js/impressConsole.js"></script>'\
            b'<script type="text/javascript" src="js/hovercraft.js"></script>'\
            b'</body></html>'
        
        self.assertEqual(html, target)


    def test_presenter_notes(self):
        with open(os.path.join(TEST_DATA, 'presenter-notes.rst'), 'rb') as infile:
            rst = infile.read()
        template = get_template_info(os.path.join(TEST_DATA, 'maximal'))
        
        html = rst2html(rst, template)
        target = b'<!DOCTYPE html SYSTEM "about:legacy-compat"><html '\
            b'xmlns="http://www.w3.org/1999/xhtml"><head><title>Document '\
            b'title</title><link rel="stylesheet" href="css/style.css" '\
            b'media="all"></link><link rel="stylesheet" '\
            b'href="css/print.css" media="print"></link><link rel="stylesheet" '\
            b'href="css/impressConsole.css" '\
            b'media="screen,projection"></link><script type="text/javascript" '\
            b'src="js/dummy.js"></script></head><body '\
            b'class="impress-not-supported"><div id="impress">'\
            b'<div class="step" step="0" data-y="0" '\
            b'data-x="0"><h1 id="hovercrafts-presenter-notes">Hovercrafts presenter '\
            b'notes</h1><p>Hovercraft supports presenter notes. It does this by '\
            b'taking anything in a\nwhat is calles a "notes-admonition" and making '\
            b'that into presenter notes.</p><div class="notes"><p>Hence, this will '\
            b'show up as presenter notes.\nYou have still access to a lot of '\
            b'formatting, like</p><ul><li>Bullet lists</li><li>And <em>all</em> '\
            b'types of <strong>inline formatting</strong></li></ul></div></div><div '\
            b'class="step" step="1" data-y="0" data-x="1600"><img '\
            b'src="images/python-logo-master-v3-TM.jpg" alt="" width="" '\
            b'height=""></img><div class="notes"><p>You don\'t have to start the '\
            b'text on the same line as\nthe note, but you can.</p><p>You can also '\
            b'have several paragraphs. You can not have any\nheadings of any kind '\
            b'though.</p><p><strong>But you can fake them through '\
            b'bold-text</strong></p><p>And that\'s useful enough for presentation '\
            b'notes.</p></div></div></div><script type="text/javascript" '\
            b'src="js/impress.js"></script><script type="text/javascript" '\
            b'src="js/impressConsole.js"></script><script type="text/javascript" '\
            b'src="js/hovercraft.js"></script></body></html>'
        self.assertEqual(html, target)

if __name__ == '__main__':
    unittest.main()
    
    