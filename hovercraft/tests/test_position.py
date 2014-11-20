import os
import unittest
from pkg_resources import resource_string
from lxml import etree

from hovercraft.parse import rst2xml, SlideMaker
from hovercraft.position import gather_positions, calculate_positions, position_slides

TEST_DATA = os.path.join(os.path.split(__file__)[0], 'test_data')

def make_tree(file_name):
    """Loads reStructuredText, outputs an lxml tree"""
    rst = resource_string(__name__, os.path.join('test_data', file_name))
    xml = rst2xml(rst)
    return SlideMaker(etree.fromstring(xml)).walk()

class GatherTests(unittest.TestCase):
    """Tests that position information is correctly parsed"""

    def test_gathering(self):
        tree = make_tree('positioning.rst')

        positions = list(gather_positions(tree))

        self.assertEqual(positions,[
            None,
            None,
             ('m 100 100 l 200 0 l 0 200', {'data-x': 'r0', 'data-y': 'r0'}),
            None,
            None,
            {'data-x': '0', 'data-y': '0'},
            None,
            None,
            ('m 100 100 l 200 0 l 0 200', {'data-x': 'r0', 'data-y': 'r0'}),
            None,
            None,
            {'data-x': '3000', 'data-y': '1000'},
        ])

class CalculateTests(unittest.TestCase):
    """Tests that positions are correctly calculated"""

    maxDiff = None

    def test_no_position(self):
        # Ten slides, none have any position information:
        positions = [None] * 10

        positions = list(calculate_positions(positions))

        self.assertEqual(positions, [
            {'data-x': '0', 'data-y': '0'},
            {'data-x': '1600', 'data-y': '0'},
            {'data-x': '3200', 'data-y': '0'},
            {'data-x': '4800', 'data-y': '0'},
            {'data-x': '6400', 'data-y': '0'},
            {'data-x': '8000', 'data-y': '0'},
            {'data-x': '9600', 'data-y': '0'},
            {'data-x': '11200', 'data-y': '0'},
            {'data-x': '12800', 'data-y': '0'},
            {'data-x': '14400', 'data-y': '0'},
        ])


    def test_square(self):
        # Slides, positioned in a square
        positions = [
            {'data-x': '0', 'data-y': '0'},
            {'data-x': '1200', 'data-y': '0'},
            None,
            None,
            {'data-x': '3600', 'data-y': '-1000'},
            None,
            None,
            {'data-x': '2400', 'data-y': '-3000'},
            None,
            None,
            {'data-x': '0', 'data-y': '-2000'},
            None,
        ]

        positions = list(calculate_positions(positions))

        self.assertEqual(positions, [
            {'data-x': '0', 'data-y': '0'},
            {'data-x': '1200', 'data-y': '0'},
            {'data-x': '2400', 'data-y': '0'},
            {'data-x': '3600', 'data-y': '0'},
            {'data-x': '3600', 'data-y': '-1000'},
            {'data-x': '3600', 'data-y': '-2000'},
            {'data-x': '3600', 'data-y': '-3000'},
            {'data-x': '2400', 'data-y': '-3000'},
            {'data-x': '1200', 'data-y': '-3000'},
            {'data-x': '0', 'data-y': '-3000'},
            {'data-x': '0', 'data-y': '-2000'},
            {'data-x': '0', 'data-y': '-1000'},
        ])


    def test_relative_positioning(self):
        # Relative positioning is probably the most useful positioning.
        # It allows you to insert or remove a slide, and everything adjusts.
        positions = [
            # First some automatic positions.
            None,
            None,
            # Then suddenly we move vertically!
            {'data-x': 'r0', 'data-y': 'r1000'},
            # Continue the same way one slide.
            None,
            # Stand still
            {'data-x': 'r0', 'data-y': 'r0'},
            # Stand still again!
            None,
            # Move a little bit
            {'data-x': 'r-40', 'data-y': 'r-200'},
            # Go back to normal movement to the right
            {'data-x': 'r1600', 'data-y': 'r0'},
            None,
            None,
            # Absolute movement back to start!
            {'data-x': '0', 'data-y': '0'},
            # Absolute movement to a center for end (with zoomout for example)
            {'data-x': '3000', 'data-y': '1000'},
        ]

        positions = list(calculate_positions(positions))

        self.assertEqual(positions, [
            {'data-x': '0', 'data-y': '0'},
            {'data-x': '1600', 'data-y': '0'},
            {'data-x': '1600', 'data-y': '1000'},
            {'data-x': '1600', 'data-y': '2000'},
            {'data-x': '1600', 'data-y': '2000'},
            {'data-x': '1600', 'data-y': '2000'},
            {'data-x': '1560', 'data-y': '1800'},
            {'data-x': '3160', 'data-y': '1800'},
            {'data-x': '4760', 'data-y': '1800'},
            {'data-x': '6360', 'data-y': '1800'},
            {'data-x': '0', 'data-y': '0'},
            {'data-x': '3000', 'data-y': '1000'},
        ])

    def test_absolute_path(self):
        # Position slides along a path
        positions = [
            ('M 100 100 L 300 100 L 300 300',  {'data-x': 'r0', 'data-y': 'r0'}),
            None,
            None,
            None,
            None,
        ]

        positions = list(calculate_positions(positions))

        self.assertEqual(positions, [
            {'data-rotate': 0, 'data-x': '0', 'data-y': '0'},
            {'data-rotate': 0, 'data-x': '2000', 'data-y': '0'},
            {'data-rotate': 44.99999999999999, 'data-x': '4000', 'data-y': '0'},
            {'data-rotate': 90.0, 'data-x': '4000', 'data-y': '2000'},
            {'data-rotate': 90.0, 'data-x': '4000', 'data-y': '4000'},
        ])

    def test_relative_path(self):
        positions = [
            None,
            None,
            ('m 100 100 l 200 0 l 0 200',  {'data-x': 'r0', 'data-y': 'r0'}),
            None,
            None,
            None,
            None,
        ]

        positions = list(calculate_positions(positions))

        self.assertEqual(positions, [
            {'data-x': '0', 'data-y': '0'},
            {'data-x': '1600', 'data-y': '0'},
            {'data-rotate': 0, 'data-x': '3200', 'data-y': '0'},
            {'data-rotate': 0, 'data-x': '5200', 'data-y': '0'},
            {'data-rotate': 44.99999999999999, 'data-x': '7200', 'data-y': '0'},
            {'data-rotate': 90.0, 'data-x': '7200', 'data-y': '2000'},
            {'data-rotate': 90.0, 'data-x': '7200', 'data-y': '4000'}
        ])


    def test_complex_path(self):
        positions = [
            None,
            None,
            ('m 100 100 l 200 0 l 0 200',  {'data-x': 'r0', 'data-y': 'r0'}),
            None,
            None,
            {'data-x': '0', 'data-y': '0'},
            None,
            ('m 100 100 l 200 0 l 0 200',  {'data-x': 'r0', 'data-y': 'r0'}),
            None,
            None,
            {'data-x': '3000', 'data-y': '1000'},
        ]

        positions = list(calculate_positions(positions))

        self.assertEqual(positions, [
            {'data-x': '0', 'data-y': '0'},
            {'data-x': '1600', 'data-y': '0'},
            {'data-rotate': 0, 'data-x': '3200', 'data-y': '0'},
            {'data-rotate': 44.99999999999999, 'data-x': '5600', 'data-y': '0'},
            {'data-rotate': 90.0, 'data-x': '5600', 'data-y': '2400'},
            {'data-x': '0', 'data-y': '0'},
            {'data-x': '-5600', 'data-y': '-2400'},
            {'data-rotate': 0, 'data-x': '-11200', 'data-y': '-4800'},
            {'data-rotate': 44.99999999999999, 'data-x': '-8800', 'data-y': '-4800'},
            {'data-rotate': 90.0, 'data-x': '-8800', 'data-y': '-2400'},
            {'data-x': '3000', 'data-y': '1000'}
        ])

class PositionTest(unittest.TestCase):

    def test_complete(self):
        tree = make_tree('positioning.rst')
        # Position the slides:
        position_slides(tree)

        # Get all slide position data:

        positions = []
        for step in tree.findall('step'):
            pos = {}
            for key in step.attrib:
                if key.startswith('data-'):
                    pos[key] = step.attrib[key]

            if 'hovercraft-path' in step.attrib:
                positions.append((step.attrib['hovercraft-path'], pos))
            else:
                positions.append(pos)

        self.assertEqual(positions, [
            {'data-x': '0', 'data-y': '0'},
             {'data-x': '1600', 'data-y': '0'},
             # Because of the path, we now get an explicit rotation:
             {'data-x': '3200', 'data-y': '0', 'data-rotate-z': '0'},
             {'data-x': '5600', 'data-y': '0', 'data-rotate-z': '44.99999999999999'},
             {'data-x': '5600', 'data-y': '2400', 'data-rotate-z': '90.0'},
             # Rotation carries over from last part of path.
             {'data-x': '0', 'data-y': '0', 'data-rotate-z': '90.0'},
             {'data-x': '-5600', 'data-y': '-2400', 'data-rotate-z': '90'},
             # The explicit rotate should continue here:
             {'data-x': '-11200', 'data-y': '-4800', 'data-rotate-z': '90'},
             # Path starts, rotation comes from path:
             {'data-x': '-16800', 'data-y': '-7200', 'data-rotate-z': '0'},
             {'data-x': '-14400', 'data-y': '-7200', 'data-rotate-z': '44.99999999999999'},
             # Explicit rotate-x and z, automatic position including rotate-z from path.
             {'data-x': '-14400', 'data-y': '-4800', 'data-rotate-z': '90.0', 'data-rotate-x': '180', 'data-z': '1000'},
             # Explicit x and y, all other carry over from last slide.
             {'data-x': '3000', 'data-y': '1000', 'data-rotate-z': '90.0', 'data-rotate-x': '180', 'data-z': '1000'},
        ])


if __name__ == '__main__':
    unittest.main()

