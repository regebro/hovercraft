from __future__ import division
from math import sqrt, cos, sin, acos, degrees, radians
from collections import MutableSequence

# This file contains classes for the different types of SVG path segments as
# well as a Path object that contains a sequence of path segments.

class Line(object):

    def __init__(self, start, end):
        self.start = start
        self.end = end
    
    def __repr__(self):
        return '<Line start=%s end=%s>' % (self.start, self.end)

    def __eq__(self, other):
        if not isinstance(other, Line):
            return NotImplemented
        return self.start == other.start and self.end == other.end

    def __ne__(self, other):
        if not isinstance(other, Line):
            return NotImplemented
        return not self == other
    
    def point(self, pos):
        distance = self.end - self.start
        return self.start + distance * pos
        
    def length(self):
        distance = (self.end - self.start)
        return sqrt(distance.real**2+distance.imag**2)


class CubicBezier(object):
    def __init__(self, start, control1, control2, end):
        self.start = start
        self.control1 = control1
        self.control2 = control2
        self.end = end
    
    def __repr__(self):
        return '<CubicBezier start=%s control1=%s control2=%s end=%s>' % (
               self.start, self.control1, self.control2, self.end)
        
    def __eq__(self, other):
        if not isinstance(other, CubicBezier):
            return NotImplemented
        return self.start == other.start and self.end == other.end and \
               self.control1 == other.control1 and self.control2 == other.control2

    def __ne__(self, other):
        if not isinstance(other, CubicBezier):
            return NotImplemented
        return not self == other

    def point(self, pos):
        """Calculate the x,y position at a certain position of the path"""
        return ((1-pos) ** 3 * self.start) + \
               (3 * (1-pos) ** 2 * pos * self.control1) + \
               (3 * (1-pos) * pos ** 2 * self.control2) + \
               (pos ** 3 * self.end)
    
    def length(self):
        """Calculate the length of the path up to a certain position"""
        # Apparently it's impossible to integrate a Cubic Bezier, so
        # this is a geometric approximation instead.
        
        current_point = self.point(0)
        # I needed 100,000 subdivisions to satisfy assertAlmostEqual on the
        # Arc segment, so I go for the same here. Over 1,000,000 subdivisions
        # makes no difference in accuracy at all.
        subdivisions = 100000
        lenght = 0
        delta = 1/subdivisions
        
        for x in range(1, subdivisions+1):
            next_point = self.point(delta*x)
            distance = sqrt((next_point.real - current_point.real)**2 + (next_point.imag - current_point.imag)**2)
            lenght += distance
            current_point = next_point
            
        return lenght
    
class QuadraticBezier(CubicBezier):
    # For Quadratic Bezier we simply subclass the Cubic. This is less efficient
    # and gives more complex calculations, but reuse means less bugs.
    # It is possible to calculate the length of a quadratic bezier so a TODO is to
    # replace the geometric approximation here.

    def __init__(self, start, control, end):
        self.start = start
        self.control1 = self.control2 = control
        self.end = end

    def __repr__(self):
        return '<QuadradicBezier start=%s control=%s end=%s>' % (
               self.start, self.control1, self.end)
        

class Arc(object):

    def __init__(self, start, radius, rotation, arc, sweep, end):
        """radius is complex, rotation is in degrees, 
           large and sweep are 1 or 0 (True/False also work)"""

        self.start = start
        self.radius = radius
        self.rotation = rotation
        self.arc = bool(arc)
        self.sweep = bool(sweep)
        self.end = end

        self._parameterize()

    def __repr__(self):
        return '<Arc start=%s radius=%s rotation=%s arc=%s sweep=%s end=%s>' % (
               self.start, self.radius, self.rotation, self.arc, self.sweep, self.end)

    def __eq__(self, other):
        if not isinstance(other, Arc):
            return NotImplemented
        return self.start == other.start and self.end == other.end and \
               self.radius == other.radius and self.rotation == other.rotation and\
               self.arc == other.arc and self.sweep == other.sweep

    def __ne__(self, other):
        if not isinstance(other, Arc):
            return NotImplemented
        return not self == other

    def _parameterize(self):
        # Conversion from endpoint to center parameterization
        # http://www.w3.org/TR/SVG/implnote.html#ArcImplementationNotes

        cosr = cos(radians(self.rotation))
        sinr = sin(radians(self.rotation))
        dx = (self.start.real - self.end.real) / 2
        dy = (self.start.imag - self.end.imag) / 2
        x1prim = cosr * dx + sinr * dy
        x1prim_sq = x1prim * x1prim
        y1prim = -sinr * dx + cosr * dy
        y1prim_sq = y1prim * y1prim

        rx = self.radius.real
        rx_sq = rx * rx
        ry = self.radius.imag        
        ry_sq = ry * ry

        # Correct out of range radii
        radius_check = (x1prim_sq / rx_sq) + (y1prim_sq / ry_sq)
        if radius_check > 1:
            rx *= sqrt(radius_check)
            ry *= sqrt(radius_check)
            rx_sq = rx * rx
            ry_sq = ry * ry

        t1 = rx_sq * y1prim_sq
        t2 = ry_sq * x1prim_sq
        c = sqrt(abs((rx_sq * ry_sq - t1 - t2) / (t1 + t2)))
        
        if self.arc == self.sweep:
            c = -c
        cxprim = c * rx * y1prim / ry
        cyprim = -c * ry * x1prim / rx

        self.center = complex((cosr * cxprim - sinr * cyprim) + 
                              ((self.start.real + self.end.real) / 2),
                              (sinr * cxprim + cosr * cyprim) + 
                              ((self.start.imag + self.end.imag) / 2))

        ux = (x1prim - cxprim) / rx
        uy = (y1prim - cyprim) / ry
        vx = (-x1prim - cxprim) / rx
        vy = (-y1prim - cyprim) / ry
        n = sqrt(ux * ux + uy * uy)
        p = ux
        theta = degrees(acos(p / n))
        if uy < 0:
            theta = -theta
        self.theta = theta % 360

        n = sqrt((ux * ux + uy * uy) * (vx * vx + vy * vy))
        p = ux * vx + uy * vy
        if p == 0:
            delta = degrees(acos(0))
        else:
            delta = degrees(acos(p / n))
        if (ux * vy - uy * vx) < 0:
            delta = -delta
        self.delta = delta % 360
        if not self.sweep:
            self.delta -= 360

    def point(self, pos):
        angle = radians(self.theta + (self.delta * pos))
        cosr = cos(radians(self.rotation))
        sinr = sin(radians(self.rotation))
    
        x = cosr * cos(angle) * self.radius.real - sinr * sin(angle) * self.radius.imag + self.center.real
        y = sinr * cos(angle) * self.radius.real + cosr * sin(angle) * self.radius.imag + self.center.imag
        return complex(x, y)
    
    def length(self):
        """The length of an elliptical arc segment requires numerical
        integration, and in that case it's simpler to just do a geometric
        approximation, as for cubic bezier curves.
        """
        
        current_point = self.point(0)
        # Here I need 100,000 subdivisions to satisfy assertAlmostEqual. It's
        # a bit slow, but I'm not in a hurry. Over 1,000,000 subdivisions
        # makes no difference in accuracy at all.
        subdivisions = 100000
        lenght = 0
        delta = 1/subdivisions
        
        for x in range(1, subdivisions+1):
            next_point = self.point(delta*x)
            distance = sqrt((next_point.real - current_point.real)**2 + (next_point.imag - current_point.imag)**2)
            lenght += distance
            current_point = next_point
            
        return lenght
    
class Path(MutableSequence):
    """A Path is a sequence of path segments"""
        
    def __init__(self, *segments):
        self._segments = list(segments)
        self._length = None
        self._lengths = None
                
    def __getitem__(self, index):
        return self._segments[index]

    def __setitem__(self, index, value):
        self._segments[index] = value

    def __delitem__(self, index):
        del self._segments[index]

    def insert(self, index, value):
        self._segments.insert(index, value)
    
    def __len__(self):
        return len(self._segments)
    
    def __repr__(self):
        return '<Path %s>' % ', '.join(repr(x) for x in self._segments)
    
    def __eq__(self, other):
        if not isinstance(other, Path):
            return NotImplemented
        if len(self) != len(other):
            return False
        for s, o in zip(self._segments, other._segments):
            if not s == o:
                return False
        return True

    def __ne__(self, other):
        if not isinstance(other, Path):
            return NotImplemented
        return not self == other
    
    def _calc_lengths(self):
        if self._length is not None:
            return
        
        lengths = [each.length() for each in self._segments]        
        self._length = sum(lengths)
        self._lengths = [each/self._length for each in lengths]
        
    def point(self, pos):
        self._calc_lengths()
        # Find which segment the point we search for is located on:
        segment_start = 0
        for index, segment in enumerate(self._segments):
            segment_end = segment_start + self._lengths[index]
            if segment_end >= pos:
                # This is the segment! How far in on the segment is the point?
                segment_pos = (pos - segment_start) / (segment_end - segment_start)
                break
            segment_start = segment_end
        else:
            # This happens when pos is 1.0, and accumulated errors
            # mean that segment_end of the last segment is not quite 1.0.
            segment_pos = 1.0

        return segment.point(segment_pos)
    
    def length(self):
        self._calc_lengths()
        return self._length
