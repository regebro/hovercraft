from __future__ import division
import unittest
from math import sqrt, pi

from hovercraft.svgpath import CubicBezier, QuadraticBezier, Line, Arc, Path

# Most of these test points are not calculated serparately, as that would
# take too long and be too error prone. Instead the curves have been verified
# to be correct visually, by drawing them with the turtle module, with code
# like this:
#
#        import turtle
#        t = turtle.Turtle()
#        t.penup()
#        
#        for arc in (path1, path2):
#            p = arc.point(0)
#            t.goto(p.real-500, -p.imag+300)
#            t.dot(3, 'black')
#            t.pendown()
#            for x in range(1,101):
#                p = arc.point(x*0.01)
#                t.goto(p.real-500, -p.imag+300)
#            t.penup()
#            t.dot(3, 'black')
#                
#        raw_input()
#
# After the paths have been verified to be correct this way, the testing of
# points along the paths has been added as regression tests, to make sure
# nobody changes the way curves are drawn by mistake. Therefore, do not take
# these points religiously. They might be subtly wrong, unless otherwise
# noted.

class LineTest(unittest.TestCase):
    
    def test_lines(self):
        # These points are calculated, and not just regression tests.
        
        line1 = Line(0j, 400+0j)
        self.assertAlmostEqual(line1.point(0), (0j))
        self.assertAlmostEqual(line1.point(0.3), (120+0j))
        self.assertAlmostEqual(line1.point(0.5), (200+0j))
        self.assertAlmostEqual(line1.point(0.9), (360+0j))
        self.assertAlmostEqual(line1.point(1), (400+0j))
        self.assertAlmostEqual(line1.length(), 400)

        line2 = Line(400+0j, 400+300j)
        self.assertAlmostEqual(line2.point(0), (400+0j))
        self.assertAlmostEqual(line2.point(0.3), (400+90j))
        self.assertAlmostEqual(line2.point(0.5), (400+150j))
        self.assertAlmostEqual(line2.point(0.9), (400+270j))
        self.assertAlmostEqual(line2.point(1), (400+300j))
        self.assertAlmostEqual(line2.length(), 300)

        line3 = Line(400+300j, 0j)
        self.assertAlmostEqual(line3.point(0), (400+300j))
        self.assertAlmostEqual(line3.point(0.3), (280+210j))
        self.assertAlmostEqual(line3.point(0.5), (200+150j))
        self.assertAlmostEqual(line3.point(0.9), (40+30j))
        self.assertAlmostEqual(line3.point(1), (0j))
        self.assertAlmostEqual(line3.length(), 500)


class CubicBezierTest(unittest.TestCase):
    def test_approx_circle(self):
        """This is a approximate circle drawn in Inkscape"""
        
        arc1 = CubicBezier(
            complex(0,0),
            complex(0,109.66797),
            complex(-88.90345,198.57142),
            complex(-198.57142,198.57142)
        )
        
        self.assertAlmostEqual(arc1.point(0), (0j))
        self.assertAlmostEqual(arc1.point(0.1), (-2.59896457+32.20931647j))
        self.assertAlmostEqual(arc1.point(0.2), (-10.12330256+62.76392816j))
        self.assertAlmostEqual(arc1.point(0.3), (-22.16418039+91.25500149j))
        self.assertAlmostEqual(arc1.point(0.4), (-38.31276448+117.27370288j))
        self.assertAlmostEqual(arc1.point(0.5), (-58.16022125+140.41119875j))
        self.assertAlmostEqual(arc1.point(0.6), (-81.29771712+160.25865552j))
        self.assertAlmostEqual(arc1.point(0.7), (-107.31641851+176.40723961j))
        self.assertAlmostEqual(arc1.point(0.8), (-135.80749184+188.44811744j))
        self.assertAlmostEqual(arc1.point(0.9), (-166.36210353+195.97245543j))
        self.assertAlmostEqual(arc1.point(1), (-198.57142+198.57142j))
        
        arc2 = CubicBezier(
            complex(-198.57142,198.57142),
            complex(-109.66797-198.57142,0+198.57142),
            complex(-198.57143-198.57142,-88.90345+198.57142),
            complex(-198.57143-198.57142,0),
        )
        
        self.assertAlmostEqual(arc2.point(0), (-198.57142+198.57142j))
        self.assertAlmostEqual(arc2.point(0.1), (-230.78073675+195.97245543j))
        self.assertAlmostEqual(arc2.point(0.2), (-261.3353492+188.44811744j))
        self.assertAlmostEqual(arc2.point(0.3), (-289.82642365+176.40723961j))
        self.assertAlmostEqual(arc2.point(0.4), (-315.8451264+160.25865552j))
        self.assertAlmostEqual(arc2.point(0.5), (-338.98262375+140.41119875j))
        self.assertAlmostEqual(arc2.point(0.6), (-358.830082+117.27370288j))
        self.assertAlmostEqual(arc2.point(0.7), (-374.97866745+91.25500149j))
        self.assertAlmostEqual(arc2.point(0.8), (-387.0195464+62.76392816j))
        self.assertAlmostEqual(arc2.point(0.9), (-394.54388515+32.20931647j))
        self.assertAlmostEqual(arc2.point(1), (-397.14285+0j))

        arc3 = CubicBezier(
            complex(-198.57143-198.57142,0),
            complex(0-198.57143-198.57142,-109.66797 ),
            complex(88.90346-198.57143-198.57142,-198.57143),
            complex(-198.57142,-198.57143)
        )

        self.assertAlmostEqual(arc3.point(0), (-397.14285+0j))
        self.assertAlmostEqual(arc3.point(0.1), (-394.54388515-32.20931675j))
        self.assertAlmostEqual(arc3.point(0.2), (-387.0195464-62.7639292j))
        self.assertAlmostEqual(arc3.point(0.3), (-374.97866745-91.25500365j))
        self.assertAlmostEqual(arc3.point(0.4), (-358.830082-117.2737064j))
        self.assertAlmostEqual(arc3.point(0.5), (-338.98262375-140.41120375j))
        self.assertAlmostEqual(arc3.point(0.6), (-315.8451264-160.258662j))
        self.assertAlmostEqual(arc3.point(0.7), (-289.82642365-176.40724745j))
        self.assertAlmostEqual(arc3.point(0.8), (-261.3353492-188.4481264j))
        self.assertAlmostEqual(arc3.point(0.9), (-230.78073675-195.97246515j))
        self.assertAlmostEqual(arc3.point(1), (-198.57142-198.57143j))
        
        arc4 = CubicBezier(
            complex(-198.57142,-198.57143),
            complex(109.66797-198.57142,0-198.57143),
            complex(0,88.90346-198.57143),
            complex(0,0),
        )
        
        self.assertAlmostEqual(arc4.point(0), (-198.57142-198.57143j))
        self.assertAlmostEqual(arc4.point(0.1), (-166.36210353-195.97246515j))
        self.assertAlmostEqual(arc4.point(0.2), (-135.80749184-188.4481264j))
        self.assertAlmostEqual(arc4.point(0.3), (-107.31641851-176.40724745j))
        self.assertAlmostEqual(arc4.point(0.4), (-81.29771712-160.258662j))
        self.assertAlmostEqual(arc4.point(0.5), (-58.16022125-140.41120375j))
        self.assertAlmostEqual(arc4.point(0.6), (-38.31276448-117.2737064j))
        self.assertAlmostEqual(arc4.point(0.7), (-22.16418039-91.25500365j))
        self.assertAlmostEqual(arc4.point(0.8), (-10.12330256-62.7639292j))
        self.assertAlmostEqual(arc4.point(0.9), (-2.59896457-32.20931675j))
        self.assertAlmostEqual(arc4.point(1), (0j))

    def test_svg_examples(self):
        
        # M100,200 C100,100 250,100 250,200
        path1 = CubicBezier(100+200j, 100+100j, 250+100j, 250+200j)
        self.assertAlmostEqual(path1.point(0), (100+200j))
        self.assertAlmostEqual(path1.point(0.3), (132.4+137j))
        self.assertAlmostEqual(path1.point(0.5), (175+125j))
        self.assertAlmostEqual(path1.point(0.9), (245.8+173j))
        self.assertAlmostEqual(path1.point(1), (250+200j))
        
        # S400,300 400,200
        path2 = CubicBezier(250+200j, 250+300j, 400+300j, 400+200j)
        self.assertAlmostEqual(path2.point(0), (250+200j))
        self.assertAlmostEqual(path2.point(0.3), (282.4+263j))
        self.assertAlmostEqual(path2.point(0.5), (325+275j))
        self.assertAlmostEqual(path2.point(0.9), (395.8+227j))
        self.assertAlmostEqual(path2.point(1), (400+200j))

        # M100,200 C100,100 400,100 400,200
        path3 = CubicBezier(100+200j, 100+100j, 400+100j, 400+200j)
        self.assertAlmostEqual(path3.point(0), (100+200j))
        self.assertAlmostEqual(path3.point(0.3), (164.8+137j))
        self.assertAlmostEqual(path3.point(0.5), (250+125j))
        self.assertAlmostEqual(path3.point(0.9), (391.6+173j))
        self.assertAlmostEqual(path3.point(1), (400+200j))

        # M100,500 C25,400 475,400 400,500
        path4 = CubicBezier(100+500j,  25+400j, 475+400j, 400+500j)
        self.assertAlmostEqual(path4.point(0), (100+500j))
        self.assertAlmostEqual(path4.point(0.3), (145.9+437j))
        self.assertAlmostEqual(path4.point(0.5), (250+425j))
        self.assertAlmostEqual(path4.point(0.9), (407.8+473j))
        self.assertAlmostEqual(path4.point(1), (400+500j))

        # M100,800 C175,700 325,700 400,800
        path5 = CubicBezier(100+800j, 175+700j, 325+700j, 400+800j)
        self.assertAlmostEqual(path5.point(0), (100+800j))
        self.assertAlmostEqual(path5.point(0.3), (183.7+737j))
        self.assertAlmostEqual(path5.point(0.5), (250+725j))
        self.assertAlmostEqual(path5.point(0.9), (375.4+773j))
        self.assertAlmostEqual(path5.point(1), (400+800j))

        # M600,200 C675,100 975,100 900,200
        path6 = CubicBezier(600+200j, 675+100j, 975+100j, 900+200j)
        self.assertAlmostEqual(path6.point(0), (600+200j))
        self.assertAlmostEqual(path6.point(0.3), (712.05+137j))
        self.assertAlmostEqual(path6.point(0.5), (806.25+125j))
        self.assertAlmostEqual(path6.point(0.9), (911.85+173j))
        self.assertAlmostEqual(path6.point(1), (900+200j))

        # M600,500 C600,350 900,650 900,500
        path7 = CubicBezier(600+500j, 600+350j, 900+650j, 900+500j)
        self.assertAlmostEqual(path7.point(0), (600+500j))
        self.assertAlmostEqual(path7.point(0.3), (664.8+462.2j))
        self.assertAlmostEqual(path7.point(0.5), (750+500j))
        self.assertAlmostEqual(path7.point(0.9), (891.6+532.4j))
        self.assertAlmostEqual(path7.point(1), (900+500j))

        # M600,800 C625,700 725,700 750,800
        path8 = CubicBezier(600+800j, 625+700j, 725+700j, 750+800j)
        self.assertAlmostEqual(path8.point(0), (600+800j))
        self.assertAlmostEqual(path8.point(0.3), (638.7+737j))
        self.assertAlmostEqual(path8.point(0.5), (675+725j))
        self.assertAlmostEqual(path8.point(0.9), (740.4+773j))
        self.assertAlmostEqual(path8.point(1), (750+800j))

        # S875,900 900,800
        inversion = (750+800j) + (750+800j) - (725+700j)
        path9 = CubicBezier(750+800j, inversion, 875+900j, 900+800j)
        self.assertAlmostEqual(path9.point(0), (750+800j))
        self.assertAlmostEqual(path9.point(0.3), (788.7+863j))
        self.assertAlmostEqual(path9.point(0.5), (825+875j))
        self.assertAlmostEqual(path9.point(0.9), (890.4+827j))
        self.assertAlmostEqual(path9.point(1), (900+800j))
        
            
    def test_length(self):
        
        # A straight line:
        arc = CubicBezier(
            complex(0,0),
            complex(0,0),
            complex(0,100),
            complex(0,100)
        )
        
        self.assertAlmostEqual(arc.length(), 100)
        
        # A diagonal line:
        arc = CubicBezier(
            complex(0,0),
            complex(0,0),
            complex(100,100),
            complex(100,100)
        )
        
        self.assertAlmostEqual(arc.length(), sqrt(2*100*100))
        
        # A quarter circle arc with radius 100:
        kappa = 4*(sqrt(2)-1)/3 # http://www.whizkidtech.redprince.net/bezier/circle/
        
        arc = CubicBezier(
            complex(0,0),
            complex(0,kappa*100),
            complex(100-kappa*100,100),
            complex(100,100)
        )

        # We can't compare with pi*50 here, because this is just an
        # approximation of a circle arc. pi*50 is 157.079632679
        # So this is just yet another "warn if this changes" test.
        # This value is not to be seens as verified as correct.
        self.assertAlmostEqual(arc.length(), 157.1016698)
        
class QuadraticBezierTest(unittest.TestCase):
        
    def test_svg_examples(self):
        """These is the path in the SVG specs"""
        # M200,300 Q400,50 600,300 T1000,300
        path1 = QuadraticBezier(200+300j, 400+50j, 600+300j)
        self.assertAlmostEqual(path1.point(0), (200+300j))
        self.assertAlmostEqual(path1.point(0.3), (336.8+142.5j))
        self.assertAlmostEqual(path1.point(0.5), (400+112.5j))
        self.assertAlmostEqual(path1.point(0.9), (545.6+232.5j))
        self.assertAlmostEqual(path1.point(1), (600+300j))

        # T1000, 300
        inversion = (600+300j) + (600+300j) - (400+50j)
        path2 = QuadraticBezier(600+300j, inversion, 1000+300j)
        self.assertAlmostEqual(path2.point(0), (600+300j))
        self.assertAlmostEqual(path2.point(0.3), (736.8+457.5j))
        self.assertAlmostEqual(path2.point(0.5), (800+487.5j))
        self.assertAlmostEqual(path2.point(0.9), (945.6+367.5j))
        self.assertAlmostEqual(path2.point(1), (1000+300j))

        
class ArcTest(unittest.TestCase):
    
    def test_points(self):
        arc1 = Arc(0j, 100+50j, 0, 0, 0, 100+50j)
        self.assertAlmostEqual(arc1.center, 100+0j)
        self.assertAlmostEqual(arc1.theta, 180.0)
        self.assertAlmostEqual(arc1.delta, -90.0)
        
        self.assertAlmostEqual(arc1.point(0.0), (0j))
        self.assertAlmostEqual(arc1.point(0.1), (1.23116594049+7.82172325201j))
        self.assertAlmostEqual(arc1.point(0.2), (4.89434837048+15.4508497187j))
        self.assertAlmostEqual(arc1.point(0.3), (10.8993475812+22.699524987j))
        self.assertAlmostEqual(arc1.point(0.4), (19.0983005625+29.3892626146j))
        self.assertAlmostEqual(arc1.point(0.5), (29.2893218813+35.3553390593j))
        self.assertAlmostEqual(arc1.point(0.6), (41.2214747708+40.4508497187j))
        self.assertAlmostEqual(arc1.point(0.7), (54.6009500260+44.5503262094j))
        self.assertAlmostEqual(arc1.point(0.8), (69.0983005625+47.5528258148j))
        self.assertAlmostEqual(arc1.point(0.9), (84.3565534960+49.3844170298j))
        self.assertAlmostEqual(arc1.point(1.0), (100+50j))
        
        arc2 = Arc(0j, 100+50j, 0, 1, 0, 100+50j)
        self.assertAlmostEqual(arc2.center, 50j)
        self.assertAlmostEqual(arc2.theta, 270.0)
        self.assertAlmostEqual(arc2.delta, -270.0)
        
        self.assertAlmostEqual(arc2.point(0.0), (0j))
        self.assertAlmostEqual(arc2.point(0.1), (-45.399049974+5.44967379058j))
        self.assertAlmostEqual(arc2.point(0.2), (-80.9016994375+20.6107373854j))
        self.assertAlmostEqual(arc2.point(0.3), (-98.7688340595+42.178276748j))
        self.assertAlmostEqual(arc2.point(0.4), (-95.1056516295+65.4508497187j))
        self.assertAlmostEqual(arc2.point(0.5), (-70.7106781187+85.3553390593j))
        self.assertAlmostEqual(arc2.point(0.6), (-30.9016994375+97.5528258148j))
        self.assertAlmostEqual(arc2.point(0.7), (15.643446504+99.3844170298j))
        self.assertAlmostEqual(arc2.point(0.8), (58.7785252292+90.4508497187j))
        self.assertAlmostEqual(arc2.point(0.9), (89.1006524188+72.699524987j))
        self.assertAlmostEqual(arc2.point(1.0), (100+50j))

        arc3 = Arc(0j, 100+50j, 0, 0, 1, 100+50j)
        self.assertAlmostEqual(arc3.center, 50j)
        self.assertAlmostEqual(arc3.theta, 270.0)
        self.assertAlmostEqual(arc3.delta, 90.0)
        
        self.assertAlmostEqual(arc3.point(0.0), (0j))
        self.assertAlmostEqual(arc3.point(0.1), (15.643446504+0.615582970243j))
        self.assertAlmostEqual(arc3.point(0.2), (30.9016994375+2.44717418524j))
        self.assertAlmostEqual(arc3.point(0.3), (45.399049974+5.44967379058j))
        self.assertAlmostEqual(arc3.point(0.4), (58.7785252292+9.54915028125j))
        self.assertAlmostEqual(arc3.point(0.5), (70.7106781187+14.6446609407j))
        self.assertAlmostEqual(arc3.point(0.6), (80.9016994375+20.6107373854j))
        self.assertAlmostEqual(arc3.point(0.7), (89.1006524188+27.300475013j))
        self.assertAlmostEqual(arc3.point(0.8), (95.1056516295+34.5491502813j))
        self.assertAlmostEqual(arc3.point(0.9), (98.7688340595+42.178276748j))
        self.assertAlmostEqual(arc3.point(1.0), (100+50j))

        arc4 = Arc(0j, 100+50j, 0, 1, 1, 100+50j)
        self.assertAlmostEqual(arc4.center, 100+0j)
        self.assertAlmostEqual(arc4.theta, 180.0)
        self.assertAlmostEqual(arc4.delta, 270.0)

        self.assertAlmostEqual(arc4.point(0.0), (0j))
        self.assertAlmostEqual(arc4.point(0.1), (10.8993475812-22.699524987j))
        self.assertAlmostEqual(arc4.point(0.2), (41.2214747708-40.4508497187j))
        self.assertAlmostEqual(arc4.point(0.3), (84.3565534960-49.3844170298j))
        self.assertAlmostEqual(arc4.point(0.4), (130.901699437-47.5528258148j))
        self.assertAlmostEqual(arc4.point(0.5), (170.710678119-35.3553390593j))
        self.assertAlmostEqual(arc4.point(0.6), (195.105651630-15.4508497187j))
        self.assertAlmostEqual(arc4.point(0.7), (198.768834060+7.82172325201j))
        self.assertAlmostEqual(arc4.point(0.8), (180.901699437+29.3892626146j))
        self.assertAlmostEqual(arc4.point(0.9), (145.399049974+44.5503262094j))
        self.assertAlmostEqual(arc4.point(1.0), (100+50j))

    def test_lenght(self):
        # I'll test the length calculations by making a circle, in two parts.
        arc1 = Arc(0j, 100+100j, 0, 0, 0, 200+0j)
        arc2 = Arc(200+0j, 100+100j, 0, 0, 0, 0j)
        self.assertAlmostEqual(arc1.length(), pi*100)
        self.assertAlmostEqual(arc2.length(), pi*100)
        
        
class TestPath(unittest.TestCase):
    
    def test_circle(self):
        arc1 = Arc(0j, 100+100j, 0, 0, 0, 200+0j)
        arc2 = Arc(200+0j, 100+100j, 0, 0, 0, 0j)
        path = Path(arc1, arc2)
        self.assertAlmostEqual(path.point(0.0), (0j))
        self.assertAlmostEqual(path.point(0.25), (100+100j))
        self.assertAlmostEqual(path.point(0.5), (200+0j))
        self.assertAlmostEqual(path.point(0.75), (100-100j))
        self.assertAlmostEqual(path.point(1.0), (0j))
        self.assertAlmostEqual(path.length(), pi*200)

    def test_svg_specs(self):
        """The paths that are in the SVG specs"""
        
        # Big pie: M300,200 h-150 a150,150 0 1,0 150,-150 z
        path = Path(Line(300+200j, 150+200j), Arc(150+200j, 150+150j, 0, 1, 0, 300+50j), Line(300+50j, 300+200j))
        # The points and length for this path are calculated and not regression tests.
        self.assertAlmostEqual(path.point(0.0), (300+200j))
        self.assertAlmostEqual(path.point(0.14897825542), (150+200j))
        self.assertAlmostEqual(path.point(0.5), (406.066017177+306.066017177j))
        self.assertAlmostEqual(path.point(1-0.14897825542), (300+50j))
        self.assertAlmostEqual(path.point(1.0), (300+200j))
        # The errors seem to accumulate. Still 6 decimal places is more than good enough.
        self.assertAlmostEqual(path.length(), pi*225+300, places=6) 
        
        # Little pie: M275,175 v-150 a150,150 0 0,0 -150,150 z
        path = Path(Line(275+175j, 275+25j), Arc(275+25j, 150+150j, 0, 0, 0, 125+175j), Line(125+175j, 275+175j))
        # The points and length for this path are calculated and not regression tests.
        self.assertAlmostEqual(path.point(0.0), (275+175j))
        self.assertAlmostEqual(path.point(0.2800495767557787), (275+25j))
        self.assertAlmostEqual(path.point(0.5), (168.93398282201787+68.93398282201787j))
        self.assertAlmostEqual(path.point(1-0.2800495767557787), (125+175j))
        self.assertAlmostEqual(path.point(1.0), (275+175j))
        # The errors seem to accumulate. Still 6 decimal places is more than good enough.
        self.assertAlmostEqual(path.length(), pi*75+300, places=6) 

        
        # Bumpy path: M600,350 l 50,-25 
        #             a25,25 -30 0,1 50,-25 l 50,-25
        #             a25,50 -30 0,1 50,-25 l 50,-25
        #             a25,75 -30 0,1 50,-25 l 50,-25 
        #             a25,100 -30 0,1 50,-25 l 50,-25
        path = Path(Line(600+350j, 650+325j),
                    Arc(650+325j, 25+25j, -30, 0, 1, 700+300j),
                    Line(700+300j, 750+275j),
                    Arc(750+275j, 25+50j, -30, 0, 1, 800+250j),
                    Line(800+250j, 850+225j),
                    Arc(850+225j, 25+75j, -30, 0, 1, 900+200j),
                    Line(900+200j, 950+175j),
                    Arc(950+175j, 25+100j, -30, 0, 1, 1000+150j),
                    Line(1000+150j, 1050+125j),
                    )
        # These are *not* calculated, but just regression tests. Be skeptical.
        self.assertAlmostEqual(path.point(0.0), (600+350j))
        self.assertAlmostEqual(path.point(0.3), (755.31526434+217.51578768j))
        self.assertAlmostEqual(path.point(0.5), (832.23324151+156.33454892j))
        self.assertAlmostEqual(path.point(0.9), (974.00559321+115.26473532j))
        self.assertAlmostEqual(path.point(1.0), (1050+125j))
        # The errors seem to accumulate. Still 6 decimal places is more than good enough.
        self.assertAlmostEqual(path.length(), 860.6756221710) 
            

if __name__ == "__main__":
    unittest.main()