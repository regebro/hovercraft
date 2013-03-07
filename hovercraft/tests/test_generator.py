import os
import unittest

from hovercraft.generate import rst2html
from hovercraft.template import Template

TEST_DATA = os.path.join(os.path.split(__file__)[0], 'test_data')

class GeneratorTests(unittest.TestCase):
    """Tests that the resulting HTML is correct.
    
    This tests the whole path except the copying of files."""
    
    def test_small(self):
        template = Template(os.path.join(TEST_DATA, 'minimal'))
        html = rst2html(os.path.join(TEST_DATA, 'simple.rst'), template)
        target = (
            b'<!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml">'
            b'<body><div id="impress">'
            b'<div class="step" step="0" data-x="0" data-y="0">'
            b'<h1 id="simple-presentation">Simple Presentation</h1>'
            b'<p>This presentation has two slides, each with a header and '
            b'some text.</p></div><div class="step" step="1" data-x="1600" '
            b'data-y="0"><h1 id="second-slide">Second slide</h1>'
            b'<p>There is no positioning or anything fancy.</p></div></div>'
            b'<script type="text/javascript" src="js/impress.js"></script>'
            b'<script type="text/javascript" src="js/hovercraft-minimal.js">'
            b'</script></body></html>')
        
        self.assertEqual(html, target)

    def test_big(self):
        template = Template(os.path.join(TEST_DATA, 'maximal'))
        html = rst2html(os.path.join(TEST_DATA, 'advanced.rst'), template)
        target = (
            b'<!DOCTYPE html SYSTEM "about:legacy-compat">'
            b'<html xmlns="http://www.w3.org/1999/xhtml"><head><title>'
            b'Presentation title</title><link rel="stylesheet" '
            b'href="css/style.css" media="all"></link>'
            b'<link rel="stylesheet" href="css/print.css" media="print">'
            b'</link><link rel="stylesheet" href="css/impressConsole.css" '
            b'media="screen,projection"></link><link rel="stylesheet" href="extra.css" '
            b'media="screen"></link><script type="text/javascript" '
            b'src="js/dummy.js"></script></head><body '
            b'class="impress-not-supported"><div id="impress" '
            b'data-transition-duration="2000" auto-console="True"><div class="step" step="0" data-x="1000" '
            b'data-y="1600"><h1 id="advanced-presentation">Advanced Presentation'
            b'</h1><p>Here we show the positioning feature, where we can '
            b'explicitly set a position\non one of the steps.</p></div><div '
            b'class="step" step="1" id="name-this-step" data-x="2600" data-y="1600"><h1 '
            b'id="formatting">Formatting</h1><p>Let us also try some basic '
            b'formatting, like <em>italic</em>, and <strong>bold</strong>.</p>'
            b'<ul><li>We can also</li><li>have a list</li><li>of things.</li>'
            b'</ul></div><div class="step" step="2" data-x="4200" data-y="1600">'
            b'<p>There should also be possible to have\npreformatted text for '
            b'code.</p><pre class="highlight code python"><span class="k">def'
            b'</span> <span class="nf">foo</span><span class="p">(</span><span '
            b'class="n">bar</span><span class="p">):</span>\n    <span class="c">'
            b'# Comment</span>\n    <span class="n">a</span> <span class="o">='
            b'</span> <span class="mi">1</span> <span class="o">+</span> <span '
            b'class="s">"hubbub"</span>\n    <span class="k">return</span> '
            b'<span class="bp">None</span></pre></div><div class="step" '
            b'step="3" data-x="5800" data-y="1600"><img '
            b'src="images/python-logo-master-v3-TM.png" alt="" width="" '
            b'height=""></img></div><div class="step" step="4" data-x="7400" '
            b'data-y="1600"><h1 id="character-sets">Character sets</h1>'
            b'<p>The character set is UTF-8 as of now. Like this: '
            b'&#xE5;&#xE4;&#xF6;.</p></div></div>'
            b'<div id="hovercraft-help" class="show"><table><tr>'
            b'<th>Left, Down, Page Down, Space</th><td>Next slide</td></tr><tr>'
            b'<th>Right, Up, Page Up</th><td>Previous slide</td></tr><tr><th>H</th>'
            b'<td>Toggle this help</td></tr></table></div><script type="text/javascript" '
            b'src="js/impress.js"></script><script type="text/javascript" '
            b'src="js/impressConsole.js"></script><script type="text/javascript" '
            b'src="js/hovercraft.js"></script></body></html>')
        
        self.assertEqual(html, target)

    def test_presenter_notes(self):
        template = Template(os.path.join(TEST_DATA, 'maximal'))
        html = rst2html(os.path.join(TEST_DATA, 'presenter-notes.rst'), template)
        target = (
            b'<!DOCTYPE html SYSTEM "about:legacy-compat"><html '
            b'xmlns="http://www.w3.org/1999/xhtml"><head><title>Document '
            b'title</title><link rel="stylesheet" href="css/style.css" '
            b'media="all"></link><link rel="stylesheet" '
            b'href="css/print.css" media="print"></link><link rel="stylesheet" '
            b'href="css/impressConsole.css" '
            b'media="screen,projection"></link><script type="text/javascript" '
            b'src="js/dummy.js"></script></head><body '
            b'class="impress-not-supported"><div id="impress">'
            b'<div class="step" step="0" data-x="0" '
            b'data-y="0"><h1 id="hovercrafts-presenter-notes">Hovercrafts presenter '
            b'notes</h1><p>Hovercraft! supports presenter notes. It does this by '
            b'taking anything in a\nwhat is calles a "notes-admonition" and making '
            b'that into presenter notes.</p><div class="notes"><p>Hence, this will '
            b'show up as presenter notes.\nYou have still access to a lot of '
            b'formatting, like</p><ul><li>Bullet lists</li><li>And <em>all</em> '
            b'types of <strong>inline formatting</strong></li></ul></div></div><div '
            b'class="step" step="1" data-x="1600" data-y="0"><img '
            b'src="images/python-logo-master-v3-TM.png" alt="" width="" '
            b'height=""></img><div class="notes"><p>You don\'t have to start the '
            b'text on the same line as\nthe note, but you can.</p><p>You can also '
            b'have several paragraphs. You can not have any\nheadings of any kind '
            b'though.</p><p><strong>But you can fake them through '
            b'bold-text</strong></p><p>And that\'s useful enough for presentation '
            b'notes.</p></div></div></div>'
            b'<div id="hovercraft-help" class="show"><table><tr>'
            b'<th>Left, Down, Page Down, Space</th><td>Next slide</td></tr><tr>'
            b'<th>Right, Up, Page Up</th><td>Previous slide</td></tr><tr><th>H</th>'
            b'<td>Toggle this help</td></tr></table></div><script type="text/javascript" '
            b'src="js/impress.js"></script><script type="text/javascript" '
            b'src="js/impressConsole.js"></script><script type="text/javascript" '
            b'src="js/hovercraft.js"></script></body></html>')
        
        self.assertEqual(html, target)


    def test_skip_presenter_notes(self):
        template = Template(os.path.join(TEST_DATA, 'maximal'))
        html = rst2html(os.path.join(TEST_DATA, 'presenter-notes.rst'), template, skip_notes=True)
        
        target = (
            b'<!DOCTYPE html SYSTEM "about:legacy-compat"><html '
            b'xmlns="http://www.w3.org/1999/xhtml"><head><title>Document '
            b'title</title><link rel="stylesheet" href="css/style.css" '
            b'media="all"></link><link rel="stylesheet" '
            b'href="css/print.css" media="print"></link><link rel="stylesheet" '
            b'href="css/impressConsole.css" '
            b'media="screen,projection"></link><script type="text/javascript" '
            b'src="js/dummy.js"></script></head><body '
            b'class="impress-not-supported"><div id="impress">'
            b'<div class="step" step="0" data-x="0" '
            b'data-y="0"><h1 id="hovercrafts-presenter-notes">Hovercrafts presenter '
            b'notes</h1><p>Hovercraft! supports presenter notes. It does this by '
            b'taking anything in a\nwhat is calles a "notes-admonition" and making '
            b'that into presenter notes.</p></div><div '
            b'class="step" step="1" data-x="1600" data-y="0"><img '
            b'src="images/python-logo-master-v3-TM.png" alt="" width="" height="">'
            b'</img></div></div><div id="hovercraft-help" class="show"><table><tr>'
            b'<th>Left, Down, Page Down, Space</th><td>Next slide</td></tr><tr>'
            b'<th>Right, Up, Page Up</th><td>Previous slide</td></tr><tr><th>H</th>'
            b'<td>Toggle this help</td></tr></table></div><script type="text/javascript" '
            b'src="js/impress.js"></script><script type="text/javascript" '
            b'src="js/impressConsole.js"></script><script type="text/javascript" '
            b'src="js/hovercraft.js"></script></body></html>')
        
        self.assertEqual(html, target)

    def test_comments(self):
        template = Template(os.path.join(TEST_DATA, 'minimal'))
        html = rst2html(os.path.join(TEST_DATA, 'comment.rst'), template)
        target = (
            b'<!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml">'
            b'<body><div id="impress">'
            b'<div class="step" step="0" data-x="0" data-y="0">'
            b'<p>This text should appear.</p></div></div>'
            b'<script type="text/javascript" src="js/impress.js"></script>'
            b'<script type="text/javascript" src="js/hovercraft-minimal.js">'
            b'</script></body></html>')
        
        self.assertEqual(html, target)

    def test_slide_with_class(self):
        template = Template(os.path.join(TEST_DATA, 'minimal'))
        html = rst2html(os.path.join(TEST_DATA, 'slide_class.rst'), template)
        target = (
            b'<!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml">'
            b'<body><div id="impress">'
            b'<div class="step something-else" step="0" data-x="0" data-y="0">'
            b'<p>This is some text</p></div></div>'
            b'<script type="text/javascript" src="js/impress.js"></script>'
            b'<script type="text/javascript" src="js/hovercraft-minimal.js">'
            b'</script></body></html>')
        self.assertEqual(html, target)
        
    def test_table_class(self):
        template = Template(os.path.join(TEST_DATA, 'minimal'))
        html = rst2html(os.path.join(TEST_DATA, 'table.rst'), template)
        target = (
            b'<!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml">'
            b'<body><div id="impress">'
            b'<div class="step" step="0" data-x="0" data-y="0">'
            b'<table cellpadding="0" cellspacing="0" class="my-table-class">'
            b'Truth table for "not"'
            b'<thead><tr><th><p>Name</p></th><th><p>Money Owed</p></th></tr>'
            b'</thead><tbody>'
            b'<tr><td><p>Adam Alpha</p></td><td><p>100</p></td></tr>'
            b'</tbody></table></div></div>'
            b'<script type="text/javascript" src="js/impress.js"></script>'
            b'<script type="text/javascript" src="js/hovercraft-minimal.js">'
            b'</script></body></html>')
        self.assertEqual(html, target)

    def test_class_directive(self):
        template = Template(os.path.join(TEST_DATA, 'minimal'))
        html = rst2html(os.path.join(TEST_DATA, 'class.rst'), template)
        target = (
            b'<!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml">'
            b'<body><div id="impress">'
            b'<div class="step" step="0" data-x="0" data-y="0">'
            b'<p class="my-class">This is some text in the class</p>'
            b'</div></div>'
            b'<script type="text/javascript" src="js/impress.js"></script>'
            b'<script type="text/javascript" src="js/hovercraft-minimal.js">'
            b'</script></body></html>')
        self.assertEqual(html, target)

    def test_container_directive(self):
        template = Template(os.path.join(TEST_DATA, 'minimal'))
        html = rst2html(os.path.join(TEST_DATA, 'container.rst'), template)
        target = (
            b'<!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml">'
            b'<body><div id="impress">'
            b'<div class="step" step="0" data-x="0" data-y="0">'
            b'<div class="my-class">'
            b'<p>This is some text in the container</p>'
            b'</div></div></div>'
            b'<script type="text/javascript" src="js/impress.js"></script>'
            b'<script type="text/javascript" src="js/hovercraft-minimal.js">'
            b'</script></body></html>')
        self.assertEqual(html, target)

if __name__ == '__main__':
    unittest.main()
    
    
