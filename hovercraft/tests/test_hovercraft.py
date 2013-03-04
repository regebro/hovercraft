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
                # We have verified the contents in test_generator.py, let's
                # just check that it writes the right thing:
                self.assertEqual(len(outfile.read()), 2429)
                
            out_files = os.listdir(tmpdir)
            self.assertEqual(set(out_files), {'extra.css', 'index.html', 'js', 'css', 'images', 'fonts'})
            js_files = os.listdir(os.path.join(tmpdir, 'js'))
            self.assertEqual(set(js_files), {'impress.js', 'hovercraft.js', 'impressConsole.js', 'dummy.js'})
            css_files = os.listdir(os.path.join(tmpdir, 'css'))
            self.assertEqual(set(css_files), {'print.css', 'style.css', 'impressConsole.css'})
            image_files = os.listdir(os.path.join(tmpdir, 'images'))
            self.assertEqual(set(image_files), {'python-logo-master-v3-TM.png'})
            font_files = os.listdir(os.path.join(tmpdir, 'fonts'))
            self.assertEqual(set(font_files), {
                'texgyreschola-regular-webfont.ttf',
                'texgyreschola-regular-webfont.eot',
                'texgyreschola-regular-webfont.woff',
                'texgyreschola-regular-webfont.svg',
            })


    def test_skip_notes(self):
        with TemporaryDirectory() as tmpdir:
            sys.argv = [
                'bin/hovercraft',
                '-t' + os.path.join(TEST_DATA, 'maximal'),
                '-c' + os.path.join(TEST_DATA, 'extra.css'),
                '-n', 
                os.path.join(TEST_DATA, 'presenter-notes.rst'),
                tmpdir,
            ]
            
            main()
            
            with open(os.path.join(tmpdir, 'index.html')) as outfile:
                # We have verified the contents in test_generator.py, let's
                # just check that it writes the right thing:
                self.assertEqual(len(outfile.read()), 1368)
                
            out_files = os.listdir(tmpdir)
            self.assertEqual(set(out_files), {'extra.css', 'index.html', 'js', 'css', 'images', 'fonts'})
            js_files = os.listdir(os.path.join(tmpdir, 'js'))
            self.assertEqual(set(js_files), {'impress.js', 'hovercraft.js', 'impressConsole.js', 'dummy.js'})
            css_files = os.listdir(os.path.join(tmpdir, 'css'))
            self.assertEqual(set(css_files), {'print.css', 'style.css', 'impressConsole.css'})
            image_files = os.listdir(os.path.join(tmpdir, 'images'))
            self.assertEqual(set(image_files), {'python-logo-master-v3-TM.png'})
            font_files = os.listdir(os.path.join(tmpdir, 'fonts'))
            self.assertEqual(set(font_files), {
                'texgyreschola-regular-webfont.ttf',
                'texgyreschola-regular-webfont.eot',
                'texgyreschola-regular-webfont.woff',
                'texgyreschola-regular-webfont.svg',
            })
            
    def test_default_template(self):
        with TemporaryDirectory() as tmpdir:
            # Adding a non-existant subdir, to test that it gets created.
            tmpdir = os.path.join(tmpdir, 'foo')
            
            sys.argv = [
                'bin/hovercraft',
                os.path.join(TEST_DATA, 'advanced.rst'),
                tmpdir,
            ]
            main()
            
            with open(os.path.join(tmpdir, 'index.html')) as outfile:
                self.assertEqual(len(outfile.read()), 2438)
                
            js_files = os.listdir(os.path.join(tmpdir, 'js'))
            self.assertEqual(set(js_files), {'impress.js', 'hovercraft.js',
                                             'impressConsole.js'})
            css_files = os.listdir(os.path.join(tmpdir, 'css'))
            self.assertEqual(set(css_files), {'hovercraft.css',
                                              'impressConsole.css', 'highlight.css'})
            image_files = os.listdir(os.path.join(tmpdir, 'images'))
            self.assertEqual(set(image_files), {'python-logo-master-v3-TM.png'})            

    def test_auto_console(self):
        with TemporaryDirectory() as tmpdir:
            # Adding a non-existant subdir, to test that it gets created.
            tmpdir = os.path.join(tmpdir, 'foo')
            
            sys.argv = [
                'bin/hovercraft',
                '-a',
                os.path.join(TEST_DATA, 'simple.rst'),
                tmpdir, 
            ]
            main()
            
            with open(os.path.join(tmpdir, 'index.html')) as outfile:
                result = outfile.read()
                self.assertIn('auto-console="True"', result)


    def test_subdirectory_css(self):
        with TemporaryDirectory() as tmpdir:
            sys.argv = [
                'bin/hovercraft',
                os.path.join(TEST_DATA, 'subdir-css.rst'),
                tmpdir,
            ]

            main()

            out_files = os.listdir(tmpdir)
            self.assertEqual(set(out_files), {'index.html', 'js', 'css', 'images'})
            css_files = os.listdir(os.path.join(tmpdir, 'css'))
            self.assertEqual(set(css_files), {'hovercraft.css', 'highlight.css', 'sub.css', 'impressConsole.css'})
            image_files = os.listdir(os.path.join(tmpdir, 'images'))
            self.assertEqual(set(image_files), {'python-logo-master-v3-TM.png'})


if __name__ == '__main__':
    unittest.main()
