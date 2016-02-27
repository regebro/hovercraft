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
    xml, deps = rst2xml(rst)
    return SlideMaker(etree.fromstring(xml)).walk()


class GatherTests(unittest.TestCase):
    """Tests that position information is correctly parsed"""

    def test_gathering(self):
        tree = make_tree('positioning.rst')

        positions = list(gather_positions(tree))

        self.assertEqual(positions, [
            {'data-x': 'r0', 'data-y': 'r0', 'data-z': 'r0',
             'data-rotate-x': 'r0', 'data-rotate-y': 'r0',
             'data-rotate-z': 'r0', 'data-scale': '1', 'is_path': False},
            {'data-x': 'r1600', 'data-y': 'r0', 'data-z': 'r0',
             'data-rotate-x': 'r0', 'data-rotate-y': 'r0',
             'data-rotate-z': 'r0', 'data-scale': 'r0', 'is_path': False},
            {'data-x': 'r1600', 'data-y': 'r0', 'data-z': 'r0',
             'data-rotate-x': 'r0', 'data-rotate-y': 'r0',
             'data-rotate-z': 'r0', 'data-scale': 'r0', 'is_path': True,
             'path': 'm 100 100 l 200 0 l 0 200'},
            {'data-x': 'r1600', 'data-y': 'r0', 'data-z': 'r0',
             'data-rotate-x': 'r0', 'data-rotate-y': 'r0',
             'data-rotate-z': 'r0', 'data-scale': 'r0', 'is_path': True},
            {'data-x': 'r1600', 'data-y': 'r0', 'data-z': 'r0',
             'data-rotate-x': 'r0', 'data-rotate-y': 'r0',
             'data-rotate-z': 'r0', 'data-scale': 'r0', 'is_path': True},
            {'data-x': '0', 'data-y': '0', 'data-z': 'r0',
             'data-rotate-x': 'r0', 'data-rotate-y': 'r0',
             'data-rotate-z': 'r0', 'data-scale': 'r0', 'is_path': False},
            {'data-x': 'r0', 'data-y': 'r0', 'data-z': 'r0',
             'data-rotate-x': 'r0', 'data-rotate-y': 'r0',
             'data-rotate-z': '90', 'data-scale': 'r0', 'is_path': False},
            {'data-x': 'r0', 'data-y': 'r0', 'data-z': 'r0',
             'data-rotate-x': 'r0', 'data-rotate-y': 'r0',
             'data-rotate-z': 'r0', 'data-scale': 'r0', 'is_path': False},
            {'data-x': 'r0', 'data-y': 'r0', 'data-z': 'r0',
             'data-rotate-x': 'r0', 'data-rotate-y': 'r0',
             'data-rotate-z': 'r0', 'data-scale': 'r0', 'is_path': True,
             'path': 'm 100 100 l 200 0 l 0 200'},
            {'data-x': 'r0', 'data-y': 'r0', 'data-z': 'r0',
             'data-rotate-x': 'r0', 'data-rotate-y': 'r0',
             'data-rotate-z': 'r0', 'data-scale': 'r0', 'is_path': True},
            {'data-x': 'r0', 'data-y': 'r0', 'data-z': '1000',
             'data-rotate-x': '180', 'data-rotate-y': 'r0',
             'data-rotate-z': 'r0', 'data-scale': 'r0', 'is_path': True},
            {'data-x': '3000', 'data-y': '1000', 'data-z': 'r0',
             'data-rotate-x': 'r0', 'data-rotate-y': 'r0',
             'data-rotate-z': 'r0', 'data-scale': 'r0', 'is_path': False},
        ])


class CalculateTests(unittest.TestCase):
    """Tests that positions are correctly calculated"""

    def test_square(self):
        # Slides, positioned in a square
        positions = [
            {'data-x': '0', 'data-y': '0'},
            {'data-x': 'r1200', 'data-y': '0'},
            {'data-x': 'r1200', 'data-y': '0'},
            {'data-x': 'r1200', 'data-y': '0'},
            {'data-x': 'r0', 'data-y': 'r-1000'},
            {'data-x': 'r0', 'data-y': 'r-1000'},
            {'data-x': 'r0', 'data-y': 'r-1000'},
            {'data-x': 'r-1200', 'data-y': 'r0'},
            {'data-x': 'r-1200', 'data-y': 'r0'},
            {'data-x': 'r-1200', 'data-y': 'r0'},
            {'data-x': 'r0', 'data-y': 'r1000'},
            {'data-x': 'r0', 'data-y': 'r1000'},
        ]

        positions = list(calculate_positions(positions))

        self.assertEqual(positions, [
            {'data-x': 0, 'data-y': 0, 'data-z': 0,
             'data-rotate-x': 0, 'data-rotate-y': 0,
             'data-rotate-z': 0, 'data-scale': 1},
            {'data-x': 1200, 'data-y': 0, 'data-z': 0,
             'data-rotate-x': 0, 'data-rotate-y': 0,
             'data-rotate-z': 0, 'data-scale': 1},
            {'data-x': 2400, 'data-y': 0, 'data-z': 0,
             'data-rotate-x': 0, 'data-rotate-y': 0,
             'data-rotate-z': 0, 'data-scale': 1},
            {'data-x': 3600, 'data-y': 0, 'data-z': 0,
             'data-rotate-x': 0, 'data-rotate-y': 0,
             'data-rotate-z': 0, 'data-scale': 1},
            {'data-x': 3600, 'data-y': -1000, 'data-z': 0,
             'data-rotate-x': 0, 'data-rotate-y': 0,
             'data-rotate-z': 0, 'data-scale': 1},
            {'data-x': 3600, 'data-y': -2000, 'data-z': 0,
             'data-rotate-x': 0, 'data-rotate-y': 0,
             'data-rotate-z': 0, 'data-scale': 1},
            {'data-x': 3600, 'data-y': -3000, 'data-z': 0,
             'data-rotate-x': 0, 'data-rotate-y': 0,
             'data-rotate-z': 0, 'data-scale': 1},
            {'data-x': 2400, 'data-y': -3000, 'data-z': 0,
             'data-rotate-x': 0, 'data-rotate-y': 0,
             'data-rotate-z': 0, 'data-scale': 1},
            {'data-x': 1200, 'data-y': -3000, 'data-z': 0,
             'data-rotate-x': 0, 'data-rotate-y': 0,
             'data-rotate-z': 0, 'data-scale': 1},
            {'data-x': 0, 'data-y': -3000, 'data-z': 0,
             'data-rotate-x': 0, 'data-rotate-y': 0,
             'data-rotate-z': 0, 'data-scale': 1},
            {'data-x': 0, 'data-y': -2000, 'data-z': 0,
             'data-rotate-x': 0, 'data-rotate-y': 0,
             'data-rotate-z': 0, 'data-scale': 1},
            {'data-x': 0, 'data-y': -1000, 'data-z': 0,
             'data-rotate-x': 0, 'data-rotate-y': 0,
             'data-rotate-z': 0, 'data-scale': 1},
        ])

    def test_relative_positioning(self):
        # Relative positioning is probably the most useful positioning.
        # It allows you to insert or remove a slide, and everything adjusts.
        positions = [
            # The first two slides are just default positons
            {'data-x': 'r0', 'data-y': 'r0'},
            {'data-x': 'r1600', 'data-y': 'r0'},
            # Then suddenly we move vertically!
            {'data-x': 'r0', 'data-y': 'r1000'},
            # Continue the same way one slide.
            {'data-x': 'r0', 'data-y': 'r1000'},
            # Stand still
            {'data-x': 'r0', 'data-y': 'r0'},
            # Stand still again!
            {'data-x': 'r0', 'data-y': 'r0'},
            # Move a little bit
            {'data-x': 'r-40', 'data-y': 'r-200'},
            # Go back to normal movement to the right
            {'data-x': 'r1600', 'data-y': 'r0'},
            {'data-x': 'r1600', 'data-y': 'r0'},
            {'data-x': 'r1600', 'data-y': 'r0'},
            # Absolute movement back to start!
            {'data-x': '0', 'data-y': '0'},
            # Absolute movement to a center for end (with zoomout for example)
            {'data-x': '3000', 'data-y': '1000'},
        ]

        positions = list(calculate_positions(positions))

        self.assertEqual(positions, [
            {'data-x': 0, 'data-y': 0, 'data-z': 0,
             'data-rotate-x': 0, 'data-rotate-y': 0,
             'data-rotate-z': 0, 'data-scale': 1},
            {'data-x': 1600, 'data-y': 0, 'data-z': 0,
             'data-rotate-x': 0, 'data-rotate-y': 0,
             'data-rotate-z': 0, 'data-scale': 1},
            {'data-x': 1600, 'data-y': 1000, 'data-z': 0,
             'data-rotate-x': 0, 'data-rotate-y': 0,
             'data-rotate-z': 0, 'data-scale': 1},
            {'data-x': 1600, 'data-y': 2000, 'data-z': 0,
             'data-rotate-x': 0, 'data-rotate-y': 0,
             'data-rotate-z': 0, 'data-scale': 1},
            {'data-x': 1600, 'data-y': 2000, 'data-z': 0,
             'data-rotate-x': 0, 'data-rotate-y': 0,
             'data-rotate-z': 0, 'data-scale': 1},
            {'data-x': 1600, 'data-y': 2000, 'data-z': 0,
             'data-rotate-x': 0, 'data-rotate-y': 0,
             'data-rotate-z': 0, 'data-scale': 1},
            {'data-x': 1560, 'data-y': 1800, 'data-z': 0,
             'data-rotate-x': 0, 'data-rotate-y': 0,
             'data-rotate-z': 0, 'data-scale': 1},
            {'data-x': 3160, 'data-y': 1800, 'data-z': 0,
             'data-rotate-x': 0, 'data-rotate-y': 0,
             'data-rotate-z': 0, 'data-scale': 1},
            {'data-x': 4760, 'data-y': 1800, 'data-z': 0,
             'data-rotate-x': 0, 'data-rotate-y': 0,
             'data-rotate-z': 0, 'data-scale': 1},
            {'data-x': 6360, 'data-y': 1800, 'data-z': 0,
             'data-rotate-x': 0, 'data-rotate-y': 0,
             'data-rotate-z': 0, 'data-scale': 1},
            {'data-x': 0, 'data-y': 0, 'data-z': 0,
             'data-rotate-x': 0, 'data-rotate-y': 0,
             'data-rotate-z': 0, 'data-scale': 1},
            {'data-x': 3000, 'data-y': 1000, 'data-z': 0,
             'data-rotate-x': 0, 'data-rotate-y': 0,
             'data-rotate-z': 0, 'data-scale': 1},
        ])

    def test_absolute_path(self):
        # Position slides along a path
        positions = [
            {'data-x': 'r0', 'data-y': 'r0', 'path': 'M 100 100 L 300 100 L 300 300',
             'is_path': True},
            {'is_path': True},
            {'is_path': True},
            {'is_path': True},
            {'is_path': True},
        ]

        positions = list(calculate_positions(positions))

        self.assertEqual(positions, [
            {'data-x': 0, 'data-y': 0, 'data-z': 0,
             'data-rotate-x': 0, 'data-rotate-y': 0,
             'data-rotate-z': 0, 'data-scale': 1},
            {'data-x': 2000, 'data-y': 0, 'data-z': 0,
             'data-rotate-x': 0, 'data-rotate-y': 0,
             'data-rotate-z': 0, 'data-scale': 1},
            {'data-x': 4000, 'data-y': 0, 'data-z': 0,
             'data-rotate-x': 0, 'data-rotate-y': 0,
             'data-rotate-z': 44.99999999999999, 'data-scale': 1},
            {'data-x': 4000, 'data-y': 2000, 'data-z': 0,
             'data-rotate-x': 0, 'data-rotate-y': 0,
             'data-rotate-z': 90.0, 'data-scale': 1},
            {'data-x': 4000, 'data-y': 4000, 'data-z': 0,
             'data-rotate-x': 0, 'data-rotate-y': 0,
             'data-rotate-z': 90.0, 'data-scale': 1},
        ])

    def test_relative_path(self):
        positions = [
            {'data-x': 'r0', 'data-y': 'r0'},
            {'data-x': 'r1600', 'data-y': 'r0'},
            {'data-x': 'r1600', 'data-y': 'r0', 'is_path': True,
             'path': 'm 100 100 l 200 0 l 0 200', },
            {'data-x': 'r0', 'data-y': 'r0', 'is_path': True},
            {'data-x': 'r0', 'data-y': 'r0', 'is_path': True},
            {'data-x': 'r1600', 'data-y': 'r0'},
            {'data-x': 'r0', 'data-y': 'r2400'},
        ]

        positions = list(calculate_positions(positions))

        self.assertEqual(positions, [
            {'data-x': 0, 'data-y': 0, 'data-z': 0,
             'data-rotate-x': 0, 'data-rotate-y': 0,
             'data-rotate-z': 0, 'data-scale': 1},
            {'data-x': 1600, 'data-y': 0, 'data-z': 0,
             'data-rotate-x': 0, 'data-rotate-y': 0,
             'data-rotate-z': 0, 'data-scale': 1},
            {'data-x': 3200, 'data-y': 0, 'data-z': 0,
             'data-rotate-x': 0, 'data-rotate-y': 0,
             'data-rotate-z': 0, 'data-scale': 1},
            # This point is exactly on a 90 degree angle. Therefore,
            # it's angle is calculated as 45 degrees, it being the
            # average.
            {'data-x': 5600, 'data-y': 0, 'data-z': 0,
             'data-rotate-x': 0, 'data-rotate-y': 0,
             'data-rotate-z': 44.99999999999999, 'data-scale': 1},
            {'data-x': 5600, 'data-y': 2400, 'data-z': 0,
             'data-rotate-x': 0, 'data-rotate-y': 0,
             'data-rotate-z': 90.0, 'data-scale': 1},
            {'data-x': 7200, 'data-y': 2400, 'data-z': 0,
             'data-rotate-x': 0, 'data-rotate-y': 0,
             'data-rotate-z': 90.0, 'data-scale': 1},
            {'data-x': 7200, 'data-y': 4800, 'data-z': 0,
             'data-rotate-x': 0, 'data-rotate-y': 0,
             'data-rotate-z': 90.0, 'data-scale': 1},
        ])

    def test_complex_path(self):
        positions = [
            {'data-x': 'r0', 'data-y': 'r0'},
            {'data-x': 'r1600', 'data-y': 'r0'},
            {'data-x': 'r1600', 'data-y': 'r0', 'path': 'm 100 100 l 200 0 l 0 200',
             'is_path': True},
            {'is_path': True},
            {'is_path': True},
            # Note that we don't change the rotation, so it stays at 90, here.
            {'data-x': '0', 'data-y': '0'},
            # No new x and y, previous was absolute: Stay still!
            {},
            {'data-x': 'r0', 'data-y': 'r0', 'path': 'm 100 100 l 200 0 l 0 200', 'is_path': True},
            {'is_path': True},
            {'is_path': True},
            {'data-x': '3000', 'data-y': '1000', 'data-rotate-z': '0'},
        ]

        positions = list(calculate_positions(positions))

        self.assertEqual(positions, [
            {'data-x': 0, 'data-y': 0, 'data-z': 0,
             'data-rotate-x': 0, 'data-rotate-y': 0,
             'data-rotate-z': 0, 'data-scale': 1},
            {'data-x': 1600, 'data-y': 0, 'data-z': 0,
             'data-rotate-x': 0, 'data-rotate-y': 0,
             'data-rotate-z': 0, 'data-scale': 1},
            {'data-x': 3200, 'data-y': 0, 'data-z': 0,
             'data-rotate-x': 0, 'data-rotate-y': 0,
             'data-rotate-z': 0, 'data-scale': 1},
            {'data-x': 5600, 'data-y': 0, 'data-z': 0,
             'data-rotate-x': 0, 'data-rotate-y': 0,
             'data-rotate-z': 44.99999999999999, 'data-scale': 1},
            {'data-x': 5600, 'data-y': 2400, 'data-z': 0,
             'data-rotate-x': 0, 'data-rotate-y': 0,
             'data-rotate-z': 90.0, 'data-scale': 1},
            # Note that we don't change the rotation, so it stays at 90, here.
            {'data-x': 0, 'data-y': 0, 'data-z': 0,
             'data-rotate-x': 0, 'data-rotate-y': 0,
             'data-rotate-z': 90.0, 'data-scale': 1},
            # No settings, still same place and rotation.
            {'data-x': 0, 'data-y': 0, 'data-z': 0,
             'data-rotate-x': 0, 'data-rotate-y': 0,
             'data-rotate-z': 90.0, 'data-scale': 1},
            # We start a path, but x and y are r0, so no movement.
            # However, the rotation will come from the path, so it resets to 0.
            {'data-x': 0, 'data-y': 0, 'data-z': 0,
             'data-rotate-x': 0, 'data-rotate-y': 0,
             'data-rotate-z': 0, 'data-scale': 1},
            {'data-x': 2400, 'data-y': 0, 'data-z': 0,
             'data-rotate-x': 0, 'data-rotate-y': 0,
             'data-rotate-z': 44.99999999999999, 'data-scale': 1},
            {'data-x': 2400, 'data-y': 2400, 'data-z': 0,
             'data-rotate-x': 0, 'data-rotate-y': 0,
             'data-rotate-z': 90.0, 'data-scale': 1},
            {'data-x': 3000, 'data-y': 1000, 'data-z': 0,
             'data-rotate-x': 0, 'data-rotate-y': 0,
             'data-rotate-z': 0, 'data-scale': 1},
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

            positions.append(pos)

        self.assertEqual(positions, [
            {'data-x': '0', 'data-y': '0', 'data-z': '0',
             'data-rotate-x': '0', 'data-rotate-y': '0',
             'data-rotate-z': '0', 'data-scale': '1'},
            {'data-x': '1600', 'data-y': '0', 'data-z': '0',
             'data-rotate-x': '0', 'data-rotate-y': '0',
             'data-rotate-z': '0', 'data-scale': '1'},
            # Because of the path, we now get an explicit rotation:
            {'data-x': '3200', 'data-y': '0', 'data-z': '0',
             'data-rotate-x': '0', 'data-rotate-y': '0',
             'data-rotate-z': '0', 'data-scale': '1'},
            {'data-x': '5600', 'data-y': '0', 'data-z': '0',
             'data-rotate-x': '0', 'data-rotate-y': '0',
             'data-rotate-z': '44.99999999999999', 'data-scale': '1'},
            {'data-x': '5600', 'data-y': '2400', 'data-z': '0',
             'data-rotate-x': '0', 'data-rotate-y': '0',
             'data-rotate-z': '90.0', 'data-scale': '1'},
            # Rotation carries over from last part of path.
            {'data-x': '0', 'data-y': '0', 'data-z': '0',
             'data-rotate-x': '0', 'data-rotate-y': '0',
             'data-rotate-z': '90.0', 'data-scale': '1'},
            # No position change
            {'data-x': '0', 'data-y': '0', 'data-z': '0',
             'data-rotate-x': '0', 'data-rotate-y': '0',
             'data-rotate-z': '90', 'data-scale': '1'},
            # No change at all.
            {'data-x': '0', 'data-y': '0', 'data-z': '0',
             'data-rotate-x': '0', 'data-rotate-y': '0',
             'data-rotate-z': '90', 'data-scale': '1'},
            # Path starts, rotation comes from path:
            {'data-x': '0', 'data-y': '0', 'data-z': '0',
             'data-rotate-x': '0', 'data-rotate-y': '0',
             'data-rotate-z': '0', 'data-scale': '1'},
            {'data-x': '2400', 'data-y': '0', 'data-z': '0',
             'data-rotate-x': '0', 'data-rotate-y': '0',
             'data-rotate-z': '44.99999999999999', 'data-scale': '1'},
            # Explicit rotate-x and z, automatic position including rotate-z from path.
            {'data-x': '2400', 'data-y': '2400', 'data-z': '1000',
             'data-rotate-x': '180', 'data-rotate-y': '0',
             'data-rotate-z': '90.0', 'data-scale': '1'},
            # Explicit x and y, all other carry over from last slide.
            {'data-x': '3000', 'data-y': '1000', 'data-z': '1000',
             'data-rotate-x': '180', 'data-rotate-y': '0',
             'data-rotate-z': '90.0', 'data-scale': '1'},
        ])


if __name__ == '__main__':
    unittest.main()
