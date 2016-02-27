import unittest
from pkg_resources import resource_string
from lxml import etree

from hovercraft.parse import SlideMaker, rst2xml


def make_tree(file_name):
    """Loads reStructuredText, outputs an lxml tree"""
    rst = resource_string(__name__, file_name)
    xml, dependencies = rst2xml(rst)
    return etree.fromstring(xml)


class SlideMakerTests(unittest.TestCase):
    """Test the conversion of docutils XML into XML suitable to give to the templates"""

    def test_simple(self):
        tree = SlideMaker(make_tree('test_data/simple.rst')).walk()
        self.assertEqual(etree.tostring(tree), (
            b'<document source="&lt;string&gt;"><step class="step step-level-1" step="0">'
            b'<section ids="simple-presentation" names="simple\\ presentation">'
            b'<title>Simple Presentation</title><paragraph>This presentation '
            b'has two slides, each with a header and some text.</paragraph>'
            b'</section></step><step class="step step-level-1" step="1"><section '
            b'ids="second-slide" names="second\\ slide"><title>Second slide</title><paragraph>'
            b'There is no positioning or anything fancy.</paragraph>'
            b'</section></step></document>'))

    def test_advanced(self):
        tree = SlideMaker(make_tree('test_data/advanced.rst')).walk()
        xml = etree.tostring(tree)
        target = (
            b'<document source="&lt;string&gt;" title="Presentation title" '
            b'data-transition-duration="2000" auto-console="True" '
            b'css-screen="extra.css"><paragraph>This is an advanced '
            b'presentation. It doesn\'t have a section in the first\nstep, '
            b'meaning the first step will not be a step at all, but a sort of\n'
            b'introductory comment about the presentation, that will not show up '
            b'in the\npresentation at all.</paragraph><paragraph>It also sets a '
            b'title and a transition-duration.</paragraph><step class="step '
            b'step-level-1" step="0" data-x="1000" data-y="1600"><section '
            b'ids="advanced-presentation" names="advanced\\ presentation">'
            b'<title>Advanced Presentation</title><paragraph>Here we '
            b'show the positioning feature, where we can explicitly set a '
            b'position\non one of the steps.</paragraph></section></step><step '
            b'class="step step-level-1" step="1" id="name-this-step" '
            b'data-x="r1600"><section ids="formatting" names="formatting"><title>'
            b'Formatting</title><paragraph>Let us also try some basic '
            b'formatting, like <emphasis>italic</emphasis>, and <strong>bold'
            b'</strong>.</paragraph><bullet_list bullet="*"><list_item>'
            b'<paragraph>We can also</paragraph></list_item><list_item>'
            b'<paragraph>have a list</paragraph></list_item><list_item>'
            b'<paragraph>of things.</paragraph></list_item></bullet_list>'
            b'</section></step><step class="step step-level-1" step="2">'
            b'<paragraph>There should also be possible to have\n'
            b'preformatted text for code.</paragraph><literal_block '
            b'classes="code python" xml:space="preserve"><inline classes="k">'
            b'def</inline> <inline classes="nf">foo</inline><inline '
            b'classes="p">(</inline><inline classes="n">bar</inline><inline '
            b'classes="p">):</inline>\n    <inline classes="c1"># Comment'
            b'</inline>\n    <inline classes="n">a</inline> <inline '
            b'classes="o">=</inline> <inline classes="mi">1</inline> <inline '
            b'classes="o">+</inline> <inline classes="s2">"hubbub"</inline>'
            b'\n    <inline classes="k">return</inline> <inline classes="bp">'
            b'None</inline></literal_block></step><step class="step step-level-1"'
            b' step="3"><paragraph>An image, with attributes:</paragraph><image '
            b'classes="imageclass" uri="images/hovercraft_logo.png" width="50%"/>'
            b'</step><step class="step step-level-1" step="4"><section ids="character-sets" '
            b'names="character\\ sets"><title>Character sets</title><paragraph>'
            b'The character set is UTF-8 as of now. Like this: '
            b'&#229;&#228;&#246;.</paragraph></section></step></document>')
        self.assertEqual(xml, target)

    def test_presenter_notes(self):
        tree = SlideMaker(make_tree('test_data/presenter-notes.rst')).walk()
        target = (
            b'<document ids="document-title" names="document\\ title" '
            b'source="&lt;string&gt;" title="Document title"><title>Document '
            b'title</title><step '
            b'class="step step-level-1" step="0"><section ids="hovercrafts-presenter-notes" '
            b'names="hovercrafts\\ presenter\\ notes"><title>Hovercrafts presenter '
            b'notes</title><paragraph>Hovercraft! supports presenter notes. It does '
            b'this by taking anything in a\nwhat is calles a "notes-admonition" and '
            b'making that into presenter notes.</paragraph><note><paragraph>Hence, '
            b'this will show up as presenter notes.\nYou have still access to a lot '
            b'of formatting, like</paragraph><bullet_list bullet="*"><list_item>'
            b'<paragraph>Bullet lists</paragraph></list_item><list_item><paragraph>'
            b'And <emphasis>all</emphasis> types of <strong>inline formatting'
            b'</strong></paragraph></list_item></bullet_list></note></section>'
            b'</step><step class="step step-level-1" step="1"><image '
            b'uri="images/hovercraft_logo.png"/><note><paragraph>You '
            b'don\'t have to start the text on the same line as\nthe note, but '
            b'you can.</paragraph><paragraph>You can also have several paragraphs.'
            b' You can not have any\nheadings of any kind '
            b'though.</paragraph><paragraph><strong>But you can fake them through '
            b'bold-text</strong></paragraph><paragraph>And that\'s useful enough '
            b'for presentation notes.</paragraph></note></step></document>')
        self.assertEqual(etree.tostring(tree), target)

    def test_transition_levels(self):
        # Make the XML
        xml, deps = rst2xml(
            b'Intro\n\n====\n\nLevel 1\n\n====\n\nLevel 1\n\n----\n\nLevel 2\n\n'
            b'....\n\nLevel 3\n\n----\n\nLevel 2\n\n....\n\nLevel 3\n\n'
            b'====\n\nLevel 1')

        target = (
            b'<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE document PUBLIC "+'
            b'//IDN docutils.sourceforge.net//DTD Docutils Generic//EN//XML" '
            b'"http://docutils.sourceforge.net/docs/ref/docutils.dtd">\n'
            b'<!-- Generated by Docutils 0.12 -->\n'
            b'<document source="&lt;string&gt;"><paragraph>Intro</paragraph>'
            b'<transition level="1"></transition><paragraph>Level 1</paragraph>'
            b'<transition level="1"></transition><paragraph>Level 1</paragraph>'
            b'<transition level="2"></transition><paragraph>Level 2</paragraph>'
            b'<transition level="3"></transition><paragraph>Level 3</paragraph>'
            b'<transition level="2"></transition><paragraph>Level 2</paragraph>'
            b'<transition level="3"></transition><paragraph>Level 3</paragraph>'
            b'<transition level="1"></transition><paragraph>Level 1</paragraph>'
            b'</document>'
        )
        self.assertEqual(xml, target)

        # Make the slides:
        tree = SlideMaker(etree.fromstring(xml)).walk()

        target = (
            b'<document source="&lt;string&gt;"><paragraph>Intro</paragraph>'
            b'<step class="step step-level-1" step="0"><paragraph>Level 1</paragraph></step>'
            b'<step class="step step-level-1" step="1"><paragraph>Level 1</paragraph>'
            b'<step class="step step-level-2" step="2"><paragraph>Level 2</paragraph>'
            b'<step class="step step-level-3" step="3"><paragraph>Level 3</paragraph></step>'
            b'</step><step class="step step-level-2" step="4"><paragraph>Level 2</paragraph>'
            b'<step class="step step-level-3" step="5"><paragraph>Level 3</paragraph></step>'
            b'</step></step><step class="step step-level-1" step="6"><paragraph>Level 1'
            b'</paragraph></step></document>'
        )
        self.assertEqual(etree.tostring(tree), target)

if __name__ == '__main__':
    unittest.main()
