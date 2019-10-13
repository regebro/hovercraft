import math

from svg.path import parse_path

DEFAULT_MOVEMENT = 1600  # If no other movement is specified, go 1600px to the right.
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

    step_number = 0
    default_movement = True

    steps = tree.findall('step')
    for step in steps:
        step_number += 1

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

        if step_number == 1 and pos['data-scale'] == 'r0':
            # No scale given for first slide, it needs to start at 1
            pos['data-scale'] = '1'

        if default_movement and step_number != 1:
            # No positioning has been given, use default:
            pos['data-x'] = 'r%s' % DEFAULT_MOVEMENT

        if 'data-rotate' in step.attrib:
            # data-rotate is an alias for data-rotate-z
            pos['data-rotate-z'] = step.get('data-rotate')
            del step.attrib['data-rotate']


        # multiply data-x, data-y, data-z with the scale if we use "r". Otherwise all the relative positions would not look the same anymore if we change the scale somewhere
        ATTRIBUTES_TO_FIX = ['data-x', 'data-y', 'data-z']

        if pos['data-scale'] == 'r0':
            # make sure every step has a scale value and is not "r0". This works as the first slide always has a value.
            pos['data-scale'] = steps[step_number-2].get('data-scale')

        for attribute_to_fix in ATTRIBUTES_TO_FIX:

            value = pos[attribute_to_fix]
            
            if value.startswith('r'):
                number_only = int(value.replace('r',''))
                scale_factor = float(pos['data-scale'])
                pos[attribute_to_fix] = 'r' + str( int( number_only * scale_factor) )



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
    result = math.degrees(math.asin(distance.imag / hyp))

    if distance.real < 0:
        result = -180 - result

    if abs(result) < 0.1:
        result = 0

    return result


def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)


def _update_position(pos1, pos2):

    for key in POSITION_ATTRIBS:
        val = pos2.get(key)
        if val is not None:
            plus = val.find("+")
            minus = val.find("-")
            if plus > -1:
                newval = num(val[plus+1:])
                pos1[key + "-rel"] = val[0:plus]
            elif minus > -1 and not val.startswith("r-"):
                newval = num(val[minus:])
                pos1[key + "-rel"] = val[0:minus]
            else:
                if val[0] == 'r':
                # Relative movement
                    newval = pos1[key] + num(val[1:])
                else:
                    newval = num(val)
                    pos1.pop(key+"-rel",  None)
            pos1[key] = newval


def calculate_positions(positions):
    """Calculates position information"""
    current_position = {'data-x': 0,
                        'data-y': 0,
                        'data-z': 0,
                        'data-rotate-x': 0,
                        'data-rotate-y': 0,
                        'data-rotate-z': 0,
                        'data-scale': 1,
                        }

    positer = iter(positions)
    position = next(positer)
    _update_position(current_position, position)

    while True:

        if 'path' in position:
            # Start of a new path!
            path = position['path']
            # Follow the path specification
            first_point = _pos_to_cord(current_position)

            # Paths that end in Z or z are closed.
            closed_path = path.strip()[-1].upper() == 'Z'
            path = parse_path(path)

            # Find out how many positions should be calculated:
            count = 1
            last = False
            deferred_positions = []
            while True:
                try:
                    position = next(positer)
                    deferred_positions.append(position)
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

            multiplier = (endcount * DEFAULT_MOVEMENT) / path.length()
            offset = path.point(0)

            path_iter = iter(deferred_positions)
            for x in range(count):

                point = path.point(x / (endcount - 1))
                point = ((point - offset) * multiplier) + first_point

                current_position.update(_coord_to_pos(point))

                rotation = _path_angle(path, x / (endcount - 1))
                current_position['data-rotate-z'] = rotation
                yield current_position.copy()
                try:
                    position = next(path_iter)
                except StopIteration:
                    last = True
                    break
                _update_position(current_position, position)

            if last:
                break

            continue

        yield current_position.copy()
        try:
            position = next(positer)
        except StopIteration:
            break
        _update_position(current_position, position)


def update_positions(tree, positions):
    """Updates the tree with new positions"""

    for step, pos in zip(tree.findall('step'), positions):
        for key in sorted(pos):
            value = pos.get(key)
            if key.endswith("-rel"):
                abs_key = key[:key.index("-rel")]
                if value is not None:
                    els = tree.findall(".//*[@id='" + value + "']")
                    for el in els :
                        pos[abs_key] = num(el.get(abs_key)) + pos.get(abs_key)
                        step.attrib[abs_key] = str(pos.get(abs_key))
            else:
                step.attrib[key] = str(pos[key])

        if 'hovercraft-path' in step.attrib:
            del step.attrib['hovercraft-path']


def position_slides(tree):
    """Position the slides in the tree"""

    positions = gather_positions(tree)
    positions = calculate_positions(positions)
    update_positions(tree, positions)
