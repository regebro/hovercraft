# This is not a generic SVG parser. It just looks for the first path it can
# find and makes a Path object out of it.
from string import digits
from hovercraft import svgpath 

COMMANDS = 'MmZzLlHhVvCcSsQqTtAa'
UPPERCASE = 'MZLHVCSQTA'

def find_path(svgdata):
    pass

def tokenize_path(pathdef):
    # Commas are separators, just like spaces.
    pathdef = pathdef.replace(',', ' ')
    
    # Commands are allowed without spaces around. Let's insert spaces so it's
    # easier to split later.
    for c in COMMANDS:
        pathdef = pathdef.replace(c, ' %s ' % c)
        
    # Split the path into elements and reverse, for easy use of .pop()
    return pathdef.split()
    
    
def parse_path(pathdef, current_pos=0j):
    # In the SVG specs, initial movetos are absolute, even if
    # specified as 'm'. This is the default behavior here as well.
    # But if you pass in a current_pos variable, the initial moveto
    # will be relative to that current_pos. This is useful.
    
    elements = tokenize_path(pathdef)
    elements.reverse()
    
    segments = svgpath.Path()
    start_pos = None
    command = None
    
    while elements:
        
        if elements[-1] in COMMANDS:
            # New command.
            last_command = command # Used by S and T
            command = elements.pop()
            absolute = command in UPPERCASE
            command = command.upper()
        else:
            # If this element starts with numbers, it is an implicit command
            # and we don't change the command. Check that it's allowed:
            if command is None:
                raise ValueError("Unallowed implicit command in %s, position %s" % (
                    pathdef, len(pathdef.split()) - len(elements)))
        
        if command == 'M':
            # Moveto command.
            x = elements.pop()
            y = elements.pop()
            pos = float(x) + float(y) * 1j
            if absolute:
                current_pos = pos
            else:
                current_pos += pos
            
            if start_pos is None:
                start_pos = current_pos
            
            # Implicit moveto commands are treated as lineto commands.
            # So we set command to lineto here, in case there are
            # further implicit commands after this moveto.
            command = 'L'
                
        elif command == 'Z':
            # Close path
            segments.append(svgpath.Line(current_pos, start_pos))
            
        elif command == 'L':
            x = elements.pop()
            y = elements.pop()
            pos = float(x) + float(y) * 1j
            if not absolute:
                pos += current_pos
            segments.append(svgpath.Line(current_pos, pos))
            current_pos = pos
            
        elif command == 'H':
            x = elements.pop()
            pos = float(x) + current_pos.imag * 1j
            if not absolute:
                pos += current_pos.real
            segments.append(svgpath.Line(current_pos, pos))
            current_pos = pos
            
        elif command == 'V':
            y = elements.pop()
            pos = current_pos.real + float(y) * 1j
            if not absolute:
                pos += current_pos.imag * 1j
            segments.append(svgpath.Line(current_pos, pos))
            current_pos = pos
        
        elif command == 'C':
            control1 = float(elements.pop()) + float(elements.pop()) * 1j
            control2 = float(elements.pop()) + float(elements.pop()) * 1j
            end = float(elements.pop()) + float(elements.pop()) * 1j
            
            if not absolute:
                control1 += current_pos
                control2 += current_pos
                end += current_pos
                
            segments.append(svgpath.CubicBezier(current_pos, control1, control2, end))
            current_pos = end

        elif command == 'S':
            # Smooth curve. First control point is the "reflection" of
            # the second control point in the previous path.
            
            if last_command not in 'CS':
                # If there is no previous command or if the previous command
                # was not an C, c, S or s, assume the first control point is
                # coincident with the current point.
                control1 = current_pos
            else:
                # The first control point is assumed to be the reflection of
                # the second control point on the previous command relative
                # to the current point.
                control1 = current_pos + current_pos - segments[-1].control2
                
            control2 = float(elements.pop()) + float(elements.pop()) * 1j
            end = float(elements.pop()) + float(elements.pop()) * 1j
            
            if not absolute:
                control2 += current_pos
                end += current_pos
                
            segments.append(svgpath.CubicBezier(current_pos, control1, control2, end))
            current_pos = end

        elif command == 'Q':
            control = float(elements.pop()) + float(elements.pop()) * 1j
            end = float(elements.pop()) + float(elements.pop()) * 1j
            
            if not absolute:
                control += current_pos
                end += current_pos
                
            segments.append(svgpath.QuadraticBezier(current_pos, control, end))
            current_pos = end

        elif command == 'T':
            # Smooth curve. Control point is the "reflection" of
            # the second control point in the previous path.
            
            if last_command not in 'QT':
                # If there is no previous command or if the previous command
                # was not an Q, q, T or t, assume the first control point is
                # coincident with the current point.
                control = current_pos
            else:
                # The control point is assumed to be the reflection of
                # the control point on the previous command relative
                # to the current point.
                control = current_pos + current_pos - segments[-1].control2
                
            end = float(elements.pop()) + float(elements.pop()) * 1j
            
            if not absolute:
                control += current_pos
                end += current_pos
                
            segments.append(svgpath.QuadraticBezier(current_pos, control, end))
            current_pos = end

        elif command == 'A':
            radius = float(elements.pop()) + float(elements.pop()) * 1j
            rotation = float(elements.pop())
            arc = float(elements.pop())
            sweep = float(elements.pop())            
            end = float(elements.pop()) + float(elements.pop()) * 1j
            
            if not absolute:
                end += current_pos
                
            segments.append(svgpath.Arc(current_pos, radius, rotation, arc, sweep, end))
            current_pos = end
            
    return segments
    
    
def get_path(filename):
    with open(filename, 'rb') as svgfile:
        path = find_path(svgfile.read())
        return parse_path(path)
    