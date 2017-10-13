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
        html, deps = rst2html(os.path.join(TEST_DATA, 'simple.rst'), template)
        self.assertEqual(html, HTML_OUTPUTS['simple'])

    def test_big(self):
        template = Template(os.path.join(TEST_DATA, 'maximal'))
        html, deps = rst2html(os.path.join(TEST_DATA, 'advanced.rst'), template)
        self.assertEqual(html, HTML_OUTPUTS['advanced'])

    def test_presenter_notes(self):
        template = Template(os.path.join(TEST_DATA, 'maximal'))
        html, deps = rst2html(os.path.join(TEST_DATA, 'presenter-notes.rst'), template)
        self.assertEqual(html, HTML_OUTPUTS['presenter-notes'])

    def test_skip_presenter_notes(self):
        template = Template(os.path.join(TEST_DATA, 'maximal'))
        html, deps = rst2html(os.path.join(TEST_DATA, 'presenter-notes.rst'), template, skip_notes=True)
        self.assertEqual(html, HTML_OUTPUTS['skip-presenter-notes'])

    def test_comments(self):
        template = Template(os.path.join(TEST_DATA, 'minimal'))
        html, deps = rst2html(os.path.join(TEST_DATA, 'comment.rst'), template)
        self.assertEqual(html, HTML_OUTPUTS['comment'])

    def test_slide_with_class(self):
        template = Template(os.path.join(TEST_DATA, 'minimal'))
        html, deps = rst2html(os.path.join(TEST_DATA, 'slide_class.rst'), template)
        self.assertEqual(html, HTML_OUTPUTS['slide_with_class'])

    def test_table(self):
        template = Template(os.path.join(TEST_DATA, 'minimal'))
        html, deps = rst2html(os.path.join(TEST_DATA, 'table.rst'), template)
        self.assertEqual(html, HTML_OUTPUTS['table'])

    def test_class_directive(self):
        template = Template(os.path.join(TEST_DATA, 'minimal'))
        html, deps = rst2html(os.path.join(TEST_DATA, 'class.rst'), template)
        self.assertEqual(html, HTML_OUTPUTS['class_directive'])

    def test_container_directive(self):
        template = Template(os.path.join(TEST_DATA, 'minimal'))
        html, deps = rst2html(os.path.join(TEST_DATA, 'container.rst'), template)
        self.assertEqual(html, HTML_OUTPUTS['container_directive'])

    def test_include(self):
        template = Template(os.path.join(TEST_DATA, 'minimal'))
        html, deps = rst2html(os.path.join(TEST_DATA, 'include.rst'), template)
        self.assertIn(b'Presentation with an include</h1>', html)
        # Make sure the simple presentation was included:
        self.assertIn(b'Simple Presentation</h1>', html)

if __name__ == '__main__':
    unittest.main()
