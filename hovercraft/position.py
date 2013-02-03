from lxml import etree

from svg.path import parse_path

DEFAULT_MOVEMENT = 1600 # If no other movement is specified, go 1600px to the right.

def gather_positions(tree):
    """Makes a list of positions and position commands from the tree"""
    for step in tree.findall('step'):
        pos = {'data-x': 'r0', 'data-y': 'r0'}
        explicit_position = False
        
        for key in ('data-x', 'data-y'):
            value = step.get(key)
            if value is not None:
                explicit_position = True
                pos[key] = value
                
        if 'hovercraft-path' in step.attrib:
            # Path given
            if explicit_position:
                raise ValueError("You can't specify both a path and a position on a step: %s" % etree.tostring(step))
            yield step.attrib['hovercraft-path']
        elif explicit_position:
            # Position given
            yield pos
        else:
            # No position given
            yield None
        
    
def _coord_to_pos(coord):
    return {'data-x': str(int(coord.real)), 'data-y': str(int(coord.imag))}

def _val_to_int(val, cur):
    if val[0] == 'r':
        return cur + int(val[1:])
    return int(val)

def _pos_to_cord(coord, current_position):
    return _val_to_int(coord['data-x'], current_position.real) + _val_to_int(coord['data-y'], current_position.imag) * 1j
    
def calculate_positions(positions):
    """Calculates position information"""
    last_position = None
    current_movement = DEFAULT_MOVEMENT
    
    positer = iter(positions)
    while True:
        position = next(positer)
        
        # This is an SVG path specification
        if isinstance(position, str):
            if last_position is None:
                first_point = 0
            else:
                first_point = last_position + current_movement
            # The the first point of the path is absolute,
            # first_point is ignored.
            path = parse_path(position, first_point)
            
            # Find out how many positions should be calculated:
            count = 1
            last = False
            while True:
                try:
                    position = next(positer)
                except StopIteration:
                    last = True
                    break
                if position is not None:
                    break
                count += 1
        
            for x in range(count):
                point = path.point(x/(count-1))
                yield _coord_to_pos(point)
                if last_position is not None:
                    current_movement = point - last_position
                last_position = point
                
            if last:
                break
        
        # Calculate path from linear movements.
        if position is None:
            if last_position is None:
                position = 0
            else:
                position = last_position + current_movement
            last_position = position 
            yield _coord_to_pos(position)
            
        # Absolute position specified
        else:
            if last_position is None:
                start = 0
            else:
                start = last_position
            position = _pos_to_cord(position, start)
            # Calculate the mo.vement from previous slide, but not on the first slide.
            if last_position is not None:
                current_movement = position - last_position
            last_position = position
            yield _coord_to_pos(position)

    
    
def update_positions(tree, positions):
    """Updates the tree with new positions"""
    for step, pos in zip(tree.findall('step'), positions):
        step.attrib['data-x'] = str(pos['data-x'])
        step.attrib['data-y'] = str(pos['data-y'])
        if 'hovercraft-path' in step.attrib:
            del step.attrib['hovercraft-path']
        

def position_slides(tree):
    """Position the slides in the tree"""
    
    positions = gather_positions(tree)
    positions = calculate_positions(positions)
    update_positions(tree, positions)