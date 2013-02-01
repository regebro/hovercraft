import os
from  tempfile import TemporaryDirectory
import unittest

from hovercraft.generate import main

TEST_DATA = os.path.join(os.path.split(__file__)[0], 'test_data')

class GeneratorTests(unittest.TestCase):
    
    def test_small(self):
        with TemporaryDirectory() as tmpdir:
            main(os.path.join(TEST_DATA, 'simple.rst'),
                 tmpdir, 
                 template=os.path.join(TEST_DATA, 'minimal')
                 )
            
            with open(os.path.join(tmpdir, 'index.html')) as outfile:
                # We have verified the contents in test_geerator.py, let's
                # just check that it writes the right thing:
                self.assertEqual(len(outfile.read()), 561)
                
            js_files = os.listdir(os.path.join(tmpdir, 'js'))
            self.assertEqual(set(js_files), {'impress.js', 'hovercraft-minimal.js'})
            
    def test_big(self):
        with TemporaryDirectory() as tmpdir:
            main(os.path.join(TEST_DATA, 'advanced.rst'),
                 tmpdir, 
                 template=os.path.join(TEST_DATA, 'maximal')
                 )
            
            with open(os.path.join(tmpdir, 'index.html')) as outfile:
                # We have verified the contents in test_geerator.py, let's
                # just check that it writes the right thing:
                self.assertEqual(len(outfile.read()), 1752)
                
            js_files = os.listdir(os.path.join(tmpdir, 'js'))
            self.assertEqual(set(js_files), {'impress.js', 'hovercraft.js', 'impressConsole.js', 'dummy.js'})
            css_files = os.listdir(os.path.join(tmpdir, 'css'))
            self.assertEqual(set(css_files), {'print.css', 'style.css', 'impressConsole.css'})
            image_files = os.listdir(os.path.join(tmpdir, 'images'))
            self.assertEqual(set(image_files), {'python-logo-master-v3-TM.png'})


    # TODO Add tests of the hovercraft command with parameters.
    
    
if __name__ == '__main__':
    unittest.main()
    
    