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
            'm 100 100 l 200 0 l 0 200',
            None, 
            None,
            {'data-x': '0', 'data-y': '0'},
            None,
            'm 100 100 l 200 0 l 0 200',
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
            'M 100 100 L 300 100 L 300 300',
            None, 
            None,
            None,
            None,
        ]
        
        positions = list(calculate_positions(positions))
        
        self.assertEqual(positions, [
            {'data-x': '100', 'data-y': '100'},
            {'data-x': '200', 'data-y': '100'},
            {'data-x': '300', 'data-y': '100'},
            {'data-x': '300', 'data-y': '200'},
            {'data-x': '300', 'data-y': '300'},        
        ])

    def test_relative_path(self):
        positions = [
            None,
            None,
            'm 100 100 l 200 0 l 0 200',
            None, 
            None,
            None,
            None,
        ]
        
        positions = list(calculate_positions(positions))
        
        self.assertEqual(positions, [
            {'data-x': '0', 'data-y': '0'},
            {'data-x': '1600', 'data-y': '0'},
            {'data-x': '3300', 'data-y': '100'},
            {'data-x': '3400', 'data-y': '100'},
            {'data-x': '3500', 'data-y': '100'},
            {'data-x': '3500', 'data-y': '200'},
            {'data-x': '3500', 'data-y': '300'},
        ])


    def test_complex_path(self):
        positions = [
            None,
            None,
            'm 100 100 l 200 0 l 0 200',
            None, 
            None,
            {'data-x': '0', 'data-y': '0'},
            None,
            'm 100 100 l 200 0 l 0 200',
            None,
            None,
            {'data-x': '3000', 'data-y': '1000'},            
        ]
  
        positions = list(calculate_positions(positions))
        self.assertEqual(positions, [
            {'data-x': '0', 'data-y': '0'},
            {'data-x': '1600', 'data-y': '0'},
            {'data-x': '3300', 'data-y': '100'},
            {'data-x': '3500', 'data-y': '100'},
            {'data-x': '3500', 'data-y': '300'},
            {'data-x': '0', 'data-y': '0'},
            {'data-x': '-3500', 'data-y': '-300'},
            {'data-x': '-6900', 'data-y': '-500'},
            {'data-x': '-6700', 'data-y': '-500'},
            {'data-x': '-6700', 'data-y': '-300'},
            {'data-x': '3000', 'data-y': '1000'},
        ])


class PositionTest(unittest.TestCase):
    
    def test_complete(self):
        tree = make_tree('positioning.rst')
        # Position the slides:
        position_slides(tree)
        # Gather the positions (we cheat and use the function for that)
        positions = list(gather_positions(tree))
        
        self.assertEqual(positions, [
            {'data-x': '0', 'data-y': '0'},
            {'data-x': '1600', 'data-y': '0'},
            {'data-x': '3300', 'data-y': '100'},
            {'data-x': '3500', 'data-y': '100'},
            {'data-x': '3500', 'data-y': '300'},
            {'data-x': '0', 'data-y': '0'},
            {'data-x': '-3500', 'data-y': '-300'},
            {'data-x': '-6900', 'data-y': '-500'},
            {'data-x': '-6700', 'data-y': '-500'},
            {'data-x': '-6700', 'data-y': '-300'},
            {'data-x': '3000', 'data-y': '1000'},
        ])

        
        
if __name__ == '__main__':
    unittest.main()
    
    