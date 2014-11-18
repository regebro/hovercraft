import os
import unittest

from hovercraft.generate import rst2html
from hovercraft.template import Template
from hovercraft.tests.test_data import HTML_OUTPUTS

TEST_DATA = os.path.join(os.path.split(__file__)[0], 'test_data')

class GeneratorTests(unittest.TestCase):
    """Tests that the resulting HTML is correct.

    This tests the whole path except the copying of files."""

    def test_small(self):
        template = Template(os.path.join(TEST_DATA, 'minimal'))
        html = rst2html(os.path.join(TEST_DATA, 'simple.rst'), template)
        self.assertEqual(html, HTML_OUTPUTS['simple'])

    def test_big(self):
        template = Template(os.path.join(TEST_DATA, 'maximal'))
        html = rst2html(os.path.join(TEST_DATA, 'advanced.rst'), template)
        self.assertEqual(html, HTML_OUTPUTS['advanced'])

    def test_presenter_notes(self):
        template = Template(os.path.join(TEST_DATA, 'maximal'))
        html = rst2html(os.path.join(TEST_DATA, 'presenter-notes.rst'), template)
        self.assertEqual(html, HTML_OUTPUTS['presenter-notes'])


    def test_skip_presenter_notes(self):
        template = Template(os.path.join(TEST_DATA, 'maximal'))
        html = rst2html(os.path.join(TEST_DATA, 'presenter-notes.rst'), template, skip_notes=True)
        self.assertEqual(html, HTML_OUTPUTS['skip-presenter-notes'])

    def test_comments(self):
        template = Template(os.path.join(TEST_DATA, 'minimal'))
        html = rst2html(os.path.join(TEST_DATA, 'comment.rst'), template)
        target = (
            b'<!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml">'
            b'<body><div id="impress">'
            b'<div class="step step-level-1" step="0" data-x="0" data-y="0">'
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
            b'<div class="step step-level-1 something-else" step="0" data-x="0" data-y="0">'
            b'<p>This is some text</p></div></div>'
            b'<script type="text/javascript" src="js/impress.js"></script>'
            b'<script type="text/javascript" src="js/hovercraft-minimal.js">'
            b'</script></body></html>')
        self.assertEqual(html, target)

    def test_tables(self):
        template = Template(os.path.join(TEST_DATA, 'minimal'))
        html = rst2html(os.path.join(TEST_DATA, 'table.rst'), template)
        target = (
            b'<!DOCTYPE html><html xmlns="http://www.w3.org/1999/xhtml">'
            b'<body><div id="impress">'
            b'<div class="step step-level-1" step="0" data-x="0" data-y="0">'
            b'<table cellpadding="0" cellspacing="0" class="my-table-class">'
            b'Truth table for "not"'
            b'<thead><tr><th><p>Name</p></th><th><p>Money Owed</p></th></tr>'
            b'</thead><tbody>'
            b'<tr><td><p>Adam Alpha</p></td><td><p>100</p></td></tr>'
            b'</tbody></table>'
            b'<table cellpadding="0" cellspacing="0" id="my-table">'
            b'<thead><tr><th><p>Number</p></th><th><p>Two</p></th></tr>'
            b'</thead><tbody>'
            b'<tr><td><p>Adam Alpha</p></td><td><p>100</p></td></tr>'
            b'</tbody></table>'
            b'</div></div>'
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
            b'<div class="step step-level-1" step="0" data-x="0" data-y="0">'
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
            b'<div class="step step-level-1" step="0" data-x="0" data-y="0">'
            b'<div class="my-class">'
            b'<p>This is some text in the container</p>'
            b'</div>'
            b'<div id="my-thing">'
            b'<p>This should have an id</p>'
            b'</div>'
            b'</div></div>'
            b'<script type="text/javascript" src="js/impress.js"></script>'
            b'<script type="text/javascript" src="js/hovercraft-minimal.js">'
            b'</script></body></html>')
        self.assertEqual(html, target)

if __name__ == '__main__':
    unittest.main()


