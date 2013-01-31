import os
import unittest
from lxml import etree

from hovercraft.position import gather_positions, calculate_positions, update_positions

TEST_DATA = os.path.join(os.path.split(__file__)[0], 'test_data')

class PositionTests(unittest.TestCase):
    """Tests that template information is correctly parsed"""
    
    maxDiff = None
    
    def test_no_position(self):
        # Ten slides, none have any position information:
        position_list = [None] * 10
        
        position_list = calculate_positions(position_list)
        
        self.assertEqual(position_list, [
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
        position_list = [
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
        
        position_list = calculate_positions(position_list)
        
        self.assertEqual(position_list, [
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
        position_list = [
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

        position_list = calculate_positions(position_list)
        
        self.assertEqual(position_list, [
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


if __name__ == '__main__':
    unittest.main()
    
    