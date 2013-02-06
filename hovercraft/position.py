import math

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
            yield step.attrib['hovercraft-path'], pos
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

    
def _path_angle(path, point):
    start = point - 0.01
    end = point + 0.01
    if start < 0:
        start = 0
        end += 0.01
    elif end > 1:
        end = 1
        start -= 0.01
        
    distance = path.point(end) - path.point(start)
    hyp = math.hypot(distance.real, distance.imag)
    result = math.degrees(math.asin(distance.imag/hyp))

    if distance.real < 0:
        result = -180-result

    if abs(result) < 0.1:
        result = 0

    return result

    
def calculate_positions(positions):
    """Calculates position information"""
    last_position = None
    current_movement = DEFAULT_MOVEMENT
    
    positer = iter(positions)
    position = next(positer)
    while True:
        
        # This is an SVG path specification
        if isinstance(position, tuple):
            position, newpos = position
                    
            if last_position is None:
                first_point = 0
            else:
                first_point = last_position + current_movement
            first_point = _pos_to_cord(newpos, first_point)
                
            # Paths that end in Z or z are closed.
            closed_path = position.strip()[-1].upper() == 'Z'
            
            # The the first point of the path is absolute,
            # first_point is ignored.
            path = parse_path(position)#, first_point)
            
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
        
            
            if closed_path:
                # This path closes in on itself. Skip the last part, so that
                # the first and last step doesn't overlap.
                endcount = count + 1
            else:
                endcount = count
            
            multiplier = (endcount * DEFAULT_MOVEMENT) / path.length()
            offset = path.point(0)
            
            for x in range(count):
                point = path.point(x/(endcount-1))
                point = ((point - offset) * multiplier) + first_point
                if last_position is not None:
                    current_movement = point - last_position
                last_position = point

                result = _coord_to_pos(point)
                
                if not 'data-rotate' in result:
                    rotation = _path_angle(path, x/(endcount-1))
                    result['data-rotate'] = rotation
                    yield result
            
            if last:
                break
            
        # Calculate path from linear movements.
        elif position is None:
            if last_position is None:
                pos = 0
            else:
                pos = last_position + current_movement
            last_position = pos
            position = _coord_to_pos(pos)
            yield position
            position = next(positer)
            
        # Absolute position specified
        else:
            if last_position is None:
                start = 0
            else:
                start = last_position
            pos = _pos_to_cord(position, start)
            # Calculate the movement from previous slide, but not on the first slide.
            if last_position is not None:
                current_movement = pos - last_position
            last_position = pos
            position.update(_coord_to_pos(pos))
            yield position
            position = next(positer)
    
    
def update_positions(tree, positions):
    """Updates the tree with new positions"""
    for step, pos in zip(tree.findall('step'), positions):
        step.attrib['data-x'] = str(pos['data-x'])
        step.attrib['data-y'] = str(pos['data-y'])
        if 'data-rotate' in pos:
            step.attrib['data-rotate'] = str(pos['data-rotate'])
        if 'hovercraft-path' in step.attrib:
            del step.attrib['hovercraft-path']
        

def position_slides(tree):
    """Position the slides in the tree"""
    
    positions = gather_positions(tree)
    positions = calculate_positions(positions)
    update_positions(tree, positions)