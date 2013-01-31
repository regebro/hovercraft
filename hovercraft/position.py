
DEFAULT_MOVEMENT = 1600 # If no other movement is specified, go 1600px to the right.

def gather_positions(tree):
    """Makes a list of positions and position commands from the tree"""
    
    
def _coord_to_pos(coord):
    return {'data-x': str(int(coord.real)), 'data-y': str(int(coord.imag))}

def _val_to_int(val, cur):
    if val[0] == 'r':
        return cur + int(val[1:])
    return int(val)

def _pos_to_cord(coord, current_position):
    return _val_to_int(coord['data-x'], current_position.real) + _val_to_int(coord['data-y'], current_position.imag) * 1j
    
def calculate_positions(position_list):
    """Calculates position information"""
    current_position = -DEFAULT_MOVEMENT
    current_movement = DEFAULT_MOVEMENT
    
    updated_positions = []
    for index, position in enumerate(position_list):
        if position is None:
            position = current_position + current_movement
            current_position = position
            updated_positions.append(_coord_to_pos(position))
        else:
            position = _pos_to_cord(position, current_position)
            # Calculate the movement from previous slide
            current_movement = position - current_position
            current_position = position
            updated_positions.append(_coord_to_pos(position))
        
    return updated_positions
    
    
def update_positions(tree, position_list):
    """Updates the tree with new positions"""

def position_slides(tree):
    """Position the slides in the tree"""
    
    # For now, just put them side by side
    for count, step in enumerate(tree.findall('step')):
        step.attrib['data-y'] = str(0)
        step.attrib['data-x'] = str(1600*count)
    return tree
        