import os
import sys
from tempfile import TemporaryDirectory
import unittest

from hovercraft import main
from hovercraft.tests.test_data import HTML_OUTPUTS

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

            with open(os.path.join(tmpdir, 'index.html'), 'rb') as outfile:
                self.assertEqual(outfile.read(), HTML_OUTPUTS['simple'])

            js_files = os.listdir(os.path.join(tmpdir, 'js'))
            self.assertEqual(set(js_files), {'impress.js', 'hovercraft-minimal.js'})

    def test_extra_css(self):
        with TemporaryDirectory() as tmpdir:
            sys.argv = [
                'bin/hovercraft',
                '-t' + os.path.join(TEST_DATA, 'maximal'),
                '-c' + os.path.join(TEST_DATA, 'extra.css'),
                '-n',
                os.path.join(TEST_DATA, 'simple.rst'),
                tmpdir,
            ]

            main()

            with open(os.path.join(tmpdir, 'index.html'), 'rb') as outfile:
                self.assertEqual(outfile.read(), HTML_OUTPUTS['extra_css'])

            out_files = os.listdir(tmpdir)
            self.assertEqual(set(out_files),
                             {'extra.css', 'index.html', 'js', 'css', 'images', 'fonts', 'directory'})

    def test_extra_js(self):
        with TemporaryDirectory() as tmpdir:
            sys.argv = [
                'bin/hovercraft',
                '-t' + os.path.join(TEST_DATA, 'maximal'),
                '-j' + os.path.join(TEST_DATA, 'extra.js'),
                '-n',
                os.path.join(TEST_DATA, 'simple.rst'),
                tmpdir,
            ]

            main()

            with open(os.path.join(tmpdir, 'index.html'), 'rb') as outfile:
                self.assertEqual(outfile.read(), HTML_OUTPUTS['extra_js'])

            out_files = os.listdir(tmpdir)
            self.assertEqual(set(out_files),
                             {'extra.js', 'index.html', 'js', 'css', 'images', 'fonts', 'directory'})

    def test_big(self):
        with TemporaryDirectory() as tmpdir:
            sys.argv = [
                'bin/hovercraft',
                '-t' + os.path.join(TEST_DATA, 'maximal', 'template.cfg'),
                os.path.join(TEST_DATA, 'advanced.rst'),
                tmpdir,
            ]

            main()

            with open(os.path.join(tmpdir, 'index.html'), 'rb') as outfile:
                # We have verified the contents in test_generator.py, let's
                # just check that it writes the right thing:
                self.assertEqual(outfile.read(), HTML_OUTPUTS['advanced'])

            out_files = os.listdir(tmpdir)
            self.assertEqual(set(out_files),
                             {'extra.css', 'extra.js', 'index.html', 'js', 'css', 'images', 'fonts', 'directory'})

            # Make sure the whole tree of the directory resource was copies,
            # except .dont-include, which should not be included.
            out_files = os.listdir(os.path.join(tmpdir, 'directory'))
            self.assertEqual(set(out_files),
                             {'subdir', 'hovercraft_logo.png', 'print.css'})
            out_files = os.listdir(os.path.join(tmpdir, 'directory', 'subdir'))
            self.assertEqual(set(out_files),
                             {'afile'})

            js_files = os.listdir(os.path.join(tmpdir, 'js'))
            self.assertEqual(set(js_files),
                             {'impress.js', 'hovercraft.js', 'impressConsole.js', 'dummy.js'})
            css_files = os.listdir(os.path.join(tmpdir, 'css'))
            self.assertEqual(set(css_files), {'print.css', 'style.css', 'impressConsole.css'})
            image_files = os.listdir(os.path.join(tmpdir, 'images'))
            self.assertEqual(set(image_files), {'hovercraft_logo.png'})
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
                '-n',
                os.path.join(TEST_DATA, 'presenter-notes.rst'),
                tmpdir,
            ]

            main()

            with open(os.path.join(tmpdir, 'index.html'), 'rb') as outfile:
                # We have verified the contents in test_generator.py, let's
                # just check that it writes the right thing:
                self.assertEqual(outfile.read(), HTML_OUTPUTS['skip-presenter-notes'])

            out_files = os.listdir(tmpdir)
            self.assertEqual(set(out_files), {'index.html', 'js', 'css', 'images', 'fonts', 'directory'})
            js_files = os.listdir(os.path.join(tmpdir, 'js'))
            self.assertEqual(set(js_files),
                             {'impress.js', 'hovercraft.js', 'impressConsole.js', 'dummy.js'})
            css_files = os.listdir(os.path.join(tmpdir, 'css'))
            self.assertEqual(set(css_files), {'print.css', 'style.css', 'impressConsole.css'})
            image_files = os.listdir(os.path.join(tmpdir, 'images'))
            self.assertEqual(set(image_files), {'hovercraft_logo.png'})
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

            with open(os.path.join(tmpdir, 'index.html'), 'rb') as outfile:
                self.assertEqual(outfile.read(), HTML_OUTPUTS['default-template'])

            js_files = os.listdir(os.path.join(tmpdir, 'js'))
            self.assertEqual(set(js_files), {'impress.js', 'hovercraft.js',
                                             'impressConsole.js'})
            css_files = os.listdir(os.path.join(tmpdir, 'css'))
            self.assertEqual(set(css_files), {'hovercraft.css',
                                              'impressConsole.css', 'highlight.css'})
            image_files = os.listdir(os.path.join(tmpdir, 'images'))
            self.assertEqual(set(image_files), {'hovercraft_logo.png'})

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

            with open(os.path.join(tmpdir, 'index.html'), 'rb') as outfile:
                result = outfile.read()
                self.assertIn(b'auto-console="True"', result)

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
            self.assertEqual(set(css_files),
                             {'hovercraft.css', 'highlight.css', 'sub.css', 'sub2.css', 'impressConsole.css'})
            image_files = os.listdir(os.path.join(tmpdir, 'images'))
            self.assertEqual(set(image_files), {'hovercraft_logo.png'})

    def test_mathjax(self):
        with TemporaryDirectory() as tmpdir:
            sys.argv = [
                'bin/hovercraft',
                os.path.join(TEST_DATA, 'math.rst'),
                tmpdir,
            ]

            main()

            with open(os.path.join(tmpdir, 'index.html'), 'rb') as outfile:
                result = outfile.read()
                self.assertIn(b'<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-MML-AM_CHTML">', result)
                self.assertIn(br'<div class="math-block ">$$\begin{align}dS = \frac{dQ}{T}\end{align}$$</div>', result)
                self.assertIn(br'<span class="math ">\(S = k \log W\)</span>', result)

if __name__ == '__main__':
    unittest.main()
