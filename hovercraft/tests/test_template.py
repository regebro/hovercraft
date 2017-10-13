import os
import unittest
from lxml import etree

from hovercraft.template import (Template, CSS_RESOURCE, JS_RESOURCE,
                                 JS_POSITION_BODY, JS_POSITION_HEADER)

TEST_DATA = os.path.join(os.path.split(__file__)[0], 'test_data')


class TemplateInfoTests(unittest.TestCase):
    """Tests that template information is correctly parsed"""

    def test_template_paths(self):
        # You can specify a folder or a cfg file and that's the same thing.
        template_info1 = Template(os.path.join(TEST_DATA, 'minimal'))
        template_info2 = Template(os.path.join(TEST_DATA, 'minimal', 'template.cfg'))
        self.assertEqual(etree.tostring(template_info1.xml_node()),
                         etree.tostring(template_info2.xml_node()))

    def test_template_minimal(self):
        template_info = Template(os.path.join(TEST_DATA, 'minimal'))
        with open(os.path.join(TEST_DATA, 'minimal', 'template.xsl'), 'rb') as xslfile:
            xsl = xslfile.read()
        self.assertEqual(template_info.xsl, xsl)
        template_files = [each.filepath for each in template_info.resources]
        self.assertIn('js/impress.js', template_files)
        self.assertIn('js/hovercraft-minimal.js', template_files)
        css_files = list(each.filepath for each in template_info.resources if
                         each.resource_type == CSS_RESOURCE)
        self.assertEqual(len(css_files), 0)
        self.assertEqual(template_info.doctype, b'<!DOCTYPE html>')

    def test_template_maximal(self):
        template_info = Template(os.path.join(TEST_DATA, 'maximal'))
        with open(os.path.join(TEST_DATA, 'maximal', 'template.xsl'), 'rb') as xslfile:
            xsl = xslfile.read()
        self.assertEqual(template_info.xsl, xsl)

        template_files = [each.filepath for each in template_info.resources]
        self.assertIn('images/hovercraft_logo.png', template_files)
        self.assertIn('js/impress.js', template_files)
        self.assertIn('js/impressConsole.js', template_files)
        self.assertIn('js/hovercraft.js', template_files)

        js_bodies = [each.filepath for each in template_info.resources if
                     each.resource_type == JS_RESOURCE and
                     each.extra_info == JS_POSITION_BODY]
        self.assertIn('js/impress.js', js_bodies)
        self.assertIn('js/impressConsole.js', js_bodies)
        self.assertIn('js/hovercraft.js', js_bodies)

        js_headers = [each.filepath for each in template_info.resources if
                      each.resource_type == JS_RESOURCE and
                      each.extra_info == JS_POSITION_HEADER]
        self.assertIn('js/dummy.js', js_headers)

        self.assertEqual(template_info.resources[0].filepath, 'css/style.css')
        self.assertEqual(template_info.resources[0].extra_info, 'all')
        self.assertEqual(template_info.resources[1].filepath, 'css/print.css')
        self.assertEqual(template_info.resources[1].extra_info, 'print')
        self.assertEqual(template_info.resources[2].filepath, 'css/impressConsole.css')
        self.assertEqual(template_info.resources[2].extra_info, 'screen,projection')

        self.assertEqual(template_info.doctype, b'<!DOCTYPE html SYSTEM "about:legacy-compat">')


class TemplateInfoNodeTests(unittest.TestCase):
    """Tests that template information is correctly made into an xml nodes"""

    def test_minimal_template(self):
        template_info = Template(os.path.join(TEST_DATA, 'minimal'))
        node = template_info.xml_node()

        self.assertEqual(etree.tostring(node), (
            b'<templateinfo><header/><body>'
            b'<js src="js/impress.js"/><js src="js/hovercraft-minimal.js"/>'
            b'</body></templateinfo>'))

    def test_maximal_template(self):
        template_info = Template(os.path.join(TEST_DATA, 'maximal'))
        node = template_info.xml_node()

        self.assertEqual(etree.tostring(node), (
            b'<templateinfo><header>'
            b'<css href="css/style.css" media="all"/>'
            b'<css href="css/print.css" media="print"/>'
            b'<css href="css/impressConsole.css" media="screen,projection"/>'
            b'<js src="js/dummy.js"/></header>'
            b'<body><js src="js/impress.js"/><js src="js/impressConsole.js"/>'
            b'<js src="js/hovercraft.js"/>'
            b'</body></templateinfo>'))


if __name__ == '__main__':
    unittest.main()
