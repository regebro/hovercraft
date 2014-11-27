import math

from svg.path import parse_path

DEFAULT_MOVEMENT = 1600
POSITION_ATTRIBS = ['data-x', 'data-y', 'data-z', 'data-rotate-x',
                    'data-rotate-y', 'data-rotate-z', 'data-scale']


def gather_positions(tree):
    """Makes a list of positions and position commands from the tree"""
    pos = {'data-x': 'r0',
           'data-y': 'r0',
           'data-z': 'r0',
           'data-rotate-x': 'r0',
           'data-rotate-y': 'r0',
           'data-rotate-z': 'r0',
           'data-scale': 'r0',
           'is_path': False
           }

    steps = 0
    default_movement = True

    for step in tree.findall('step'):
        steps += 1

        for key in POSITION_ATTRIBS:
            value = step.get(key)

            if value is not None:
                # We have a new value
                default_movement = False  # No longer use the default movement
                pos[key] = value
            elif pos[key] and not pos[key].startswith('r'):
                # The old value was absolute and no new value, so stop
                pos[key] = 'r0'
            # We had no new value, and the old value was a relative
            # movement, so we just keep moving.

        if default_movement and steps != 1:
            # No positioning has been given, use default:
            pos['data-x'] = 'r%s' % DEFAULT_MOVEMENT

        if 'data-rotate' in step.attrib:
            # data-rotate is an alias for data-rotate-z
            pos['data-rotate-z'] = step.get('data-rotate')
            del step.attrib['data-rotate']

        if 'hovercraft-path' in step.attrib:
            # Path given x and y will be calculated from the path
            default_movement = False  # No longer use the default movement
            pos['is_path'] = True
            # Add the path spec
            pos['path'] = step.attrib['hovercraft-path']
            yield pos.copy()
            # And get rid of it for the next step
            del pos['path']
        else:
            if 'data-x' in step.attrib or 'data-y' in step.attrib:
                # No longer using a path
                pos['is_path'] = False
            yield pos.copy()


def _coord_to_pos(coord):
    return {'data-x': int(coord.real), 'data-y': int(coord.imag)}


def _pos_to_cord(coord):
    return coord['data-x'] + coord['data-y'] * 1j


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
    last_position = {'data-x': 0,
                     'data-y': 0,
                     'data-z': 0,
                     'data-rotate-x': 0,
                     'data-rotate-y': 0,
                     'data-rotate-z': 0,
                     'data-scale': 0,
                     }

    positer = iter(positions)
    position = next(positer)

    while True:
        for key in POSITION_ATTRIBS:
            val = position.get(key)
            if val:
                if val[0] == 'r':
                    # Relative movement
                    print(last_position)
                    newval = last_position[key] + int(val[1:])
                else:
                    newval = int(val)
                last_position[key] = newval

        if 'path' in position:
            import pdb;pdb.set_trace()
            # Start of a new path!
            path = position['path']
            # Follow the path specification
            first_point = _pos_to_cord(last_position)

            # Paths that end in Z or z are closed.
            closed_path = path.strip()[-1].upper() == 'Z'
            path = parse_path(path)

            # Find out how many positions should be calculated:
            count = 1
            last = False
            while True:
                try:
                    position = next(positer)
                except StopIteration:
                    last = True  # This path goes to the end
                    break
                if not position.get('is_path') or 'path' in position:
                    # The end of the path, or the start of a new one
                    break
                count += 1

            if count < 2:
                raise AssertionError("The path specification is only used for "
                                     "one slide, which makes it pointless.")

            if closed_path:
                # This path closes in on itself. Skip the last part, so that
                # the first and last step doesn't overlap.
                endcount = count + 1
            else:
                endcount = count

            multiplier = ((endcount - 1 ) * DEFAULT_MOVEMENT) / path.length()
            offset = path.point(0)

            for x in range(count):
                point = path.point(x/(endcount-1))
                point = ((point - offset) * multiplier) + first_point

                last_position.update(_coord_to_pos(point))

                rotation = _path_angle(path, x/(endcount-1))
                last_position['data-rotate-z'] = rotation
                yield last_position.copy()

            if last:
                break

            continue

        yield last_position.copy()
        position = next(positer)


def update_positions(tree, positions):
    """Updates the tree with new positions"""

    for step, pos in zip(tree.findall('step'), positions):
        for key in pos:
            step.attrib[key] = str(pos[key])

        #if 'hovercraft-path' in step.attrib:
            #del step.attrib['hovercraft-path']

        #for key in persistent:
            #if key in step.attrib:
                #persistent[key] = step.attrib[key]
            #elif persistent[key] != '0': # Skip if zero.
                #step.attrib[key] = persistent[key]


def position_slides(tree):
    """Position the slides in the tree"""

    positions = gather_positions(tree)
    positions = calculate_positions(positions)
    update_positions(tree, positions)
