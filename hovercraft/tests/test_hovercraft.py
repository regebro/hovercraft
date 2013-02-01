import os
import sys
from  tempfile import TemporaryDirectory
import unittest

from hovercraft import main

TEST_DATA = os.path.join(os.path.split(__file__)[0], 'test_data')

class HTMLTests(unittest.TestCase):
    """Test the procedure from rst to html"""
    
    def test_small(self):
        with TemporaryDirectory() as tmpdir:
            sys.argv = [
                'bin/hovercraft',
                '-t' + os.path.join(TEST_DATA, 'minimal'),
                os.path.join(TEST_DATA, 'simple.rst'),
                tmpdir, 
            ]
            
            main()
            
            with open(os.path.join(tmpdir, 'index.html')) as outfile:
                # We have verified the contents in test_geerator.py, let's
                # just check that it writes the right thing:
                self.assertEqual(len(outfile.read()), 561)
                
            js_files = os.listdir(os.path.join(tmpdir, 'js'))
            self.assertEqual(set(js_files), {'impress.js', 'hovercraft-minimal.js'})
            
    def test_big(self):
        with TemporaryDirectory() as tmpdir:
            sys.argv = [
                'bin/hovercraft',
                '-t' + os.path.join(TEST_DATA, 'maximal'),
                '-c' + os.path.join(TEST_DATA, 'extra.css'),
                os.path.join(TEST_DATA, 'advanced.rst'),
                tmpdir,
            ]
            
            main()
            
            with open(os.path.join(tmpdir, 'index.html')) as outfile:
                # We have verified the contents in test_geerator.py, let's
                # just check that it writes the right thing:
                self.assertEqual(len(outfile.read()), 1815)
                
            js_files = os.listdir(os.path.join(tmpdir, 'js'))
            self.assertEqual(set(js_files), {'impress.js', 'hovercraft.js', 'impressConsole.js', 'dummy.js'})
            css_files = os.listdir(os.path.join(tmpdir, 'css'))
            self.assertEqual(set(css_files), {'print.css', 'style.css', 'impressConsole.css', 'extra.css'})
            image_files = os.listdir(os.path.join(tmpdir, 'images'))
            self.assertEqual(set(image_files), {'python-logo-master-v3-TM.png'})
            
    def test_default_template(self):
        with TemporaryDirectory() as tmpdir:
            sys.argv = [
                'bin/hovercraft',
                os.path.join(TEST_DATA, 'advanced.rst'),
                tmpdir,
            ]
            
            main()
            
            with open(os.path.join(tmpdir, 'index.html')) as outfile:
                self.assertEqual(len(outfile.read()), 1586)
                
            js_files = os.listdir(os.path.join(tmpdir, 'js'))
            self.assertEqual(set(js_files), {'impress.js', 'hovercraft.js', 'impressConsole.js'})
            css_files = os.listdir(os.path.join(tmpdir, 'css'))
            self.assertEqual(set(css_files), {'style.css', 'impressConsole.css'})
            # Ni images = no image dir:
            self.assertFalse(os.path.exists(os.path.join(tmpdir, 'images')))
        
    
if __name__ == '__main__':
    unittest.main()
    
    