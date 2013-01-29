import os
import unittest
from hovercraft.templating import get_template_info, template_info_node

TEST_DATA = os.path.join(os.path.split(__file__)[0], 'test_data')

class TemplateInfoTests(unittest.TestCase):
    
    def test_template_paths(self):
        # You can specify a folder or a cfg file and that's the same thing.
        template_info1 = get_template_info(os.path.join(TEST_DATA, 'minimal'))
        template_info2 = get_template_info(os.path.join(TEST_DATA, 'minimal', 'template.cfg'))
        self.assertEqual(template_info1, template_info2)
        
    def test_template_minimal(self):
        template_info = get_template_info(os.path.join(TEST_DATA, 'minimal'))
        with open(os.path.join(TEST_DATA, 'minimal', 'template.xsl'), 'rb') as xslfile:
            xsl = xslfile.read()
        self.assertEqual(template_info['xsl'], xsl)
        self.assertIn('js/impress.js', template_info['files'])
        self.assertIn('js/hovercraft-minimal.js', template_info['files'])
        self.assertEqual(len(template_info['css']), 0)

    def test_template_maximal(self):
        template_info = get_template_info(os.path.join(TEST_DATA, 'maximal'))
        with open(os.path.join(TEST_DATA, 'maximal', 'template.xsl'), 'rb') as xslfile:
            xsl = xslfile.read()
        self.assertEqual(template_info['xsl'], xsl)
        self.assertIn('js/impress.js', template_info['files'])
        self.assertIn('js/impressConsole.js', template_info['files'])
        self.assertIn('js/hovercraft.js', template_info['files'])

        self.assertIn('images/python-logo-master-v3-TM.png', template_info['files'])
        
        self.assertIn(('css/style.css', 'screen,print,projection'), template_info['css'])
        self.assertIn(('css/print.css', 'print'), template_info['css'])
        self.assertIn(('css/impressConsole.css', 'screen,projection'), template_info['css'])
        


class TemplateInfoNodeTests(unittest.TestCase):
    
    def test_make_node(self):
        info = {'css': [], 
                'js-header':[], 
                'js-footer': ['js/impress.js', 'js/hovercraft-minimal.js'],
                'files': {} }
        node = template_info_node(info)
        
        
        
        

if __name__ == '__main__':
    unittest.main()
    
    