from __future__ import division
import unittest
from hovercraft.svgpath import CubicBezier, QuadraticBezier, Line, Arc, Path
from hovercraft.svgparser import parse_path, get_path, find_path

class TestParser(unittest.TestCase):
    
    def test_svg_examples(self):
        """Examples from the SVG spec"""
        path1 = parse_path('M 100 100 L 300 100 L 200 300 z')
        self.assertEqual(path1, Path(Line(100+100j, 300+100j), 
                                     Line(300+100j, 200+300j),
                                     Line(200+300j, 100+100j)))
        
        path1 = parse_path('M 100 100 L 200 200')
        path2 = parse_path('M100 100L200 200')
        self.assertEqual(path1, path2)
                
        path1 = parse_path('M 100 200 L 200 100 L -100 -200')
        path2 = parse_path('M 100 200 L 200 100 -100 -200')
        self.assertEqual(path1, path2)
        
        
        path1 = parse_path("""M100,200 C100,100 250,100 250,200
                              S400,300 400,200""")
        self.assertEqual(path1, 
            Path(CubicBezier(100+200j, 100+100j, 250+100j, 250+200j),
                 CubicBezier(250+200j, 250+300j, 400+300j, 400+200j)))

        path1 = parse_path('M100,200 C100,100 400,100 400,200')
        self.assertEqual(path1, 
            Path(CubicBezier(100+200j, 100+100j, 400+100j, 400+200j)))

        path1 = parse_path('M100,500 C25,400 475,400 400,500')
        self.assertEqual(path1, 
            Path(CubicBezier(100+500j,  25+400j, 475+400j, 400+500j)))

        path1 = parse_path('M100,800 C175,700 325,700 400,800')
        self.assertEqual(path1, 
            Path(CubicBezier(100+800j, 175+700j, 325+700j, 400+800j)))

        path1 = parse_path('M600,200 C675,100 975,100 900,200')
        self.assertEqual(path1, 
            Path(CubicBezier(600+200j, 675+100j, 975+100j, 900+200j)))

        path1 = parse_path('M600,500 C600,350 900,650 900,500')
        self.assertEqual(path1, 
            Path(CubicBezier(600+500j, 600+350j, 900+650j, 900+500j)))

        path1 = parse_path("""M600,800 C625,700 725,700 750,800
                              S875,900 900,800""")
        self.assertEqual(path1, 
            Path(CubicBezier(600+800j, 625+700j, 725+700j, 750+800j),
                 CubicBezier(750+800j, 775+900j, 875+900j, 900+800j)))

        path1 = parse_path('M200,300 Q400,50 600,300 T1000,300')
        self.assertEqual(path1, 
            Path(QuadraticBezier(200+300j, 400+50j, 600+300j),
                 QuadraticBezier(600+300j, 800+550j, 1000+300j)))

        path1 = parse_path('M300,200 h-150 a150,150 0 1,0 150,-150 z')
        self.assertEqual(path1, 
            Path(Line(300+200j, 150+200j), 
                 Arc(150+200j, 150+150j, 0, 1, 0, 300+50j), 
                 Line(300+50j, 300+200j)))
        
        path1 = parse_path('M275,175 v-150 a150,150 0 0,0 -150,150 z')
        self.assertEqual(path1, 
            Path(Line(275+175j, 275+25j), 
                 Arc(275+25j, 150+150j, 0, 0, 0, 125+175j), 
                 Line(125+175j, 275+175j)))

        path1 = parse_path("""M600,350 l 50,-25 
                              a25,25 -30 0,1 50,-25 l 50,-25 
                              a25,50 -30 0,1 50,-25 l 50,-25 
                              a25,75 -30 0,1 50,-25 l 50,-25 
                              a25,100 -30 0,1 50,-25 l 50,-25""")
        self.assertEqual(path1, 
            Path(Line(600+350j, 650+325j),
                 Arc(650+325j, 25+25j, -30, 0, 1, 700+300j),
                 Line(700+300j, 750+275j),
                 Arc(750+275j, 25+50j, -30, 0, 1, 800+250j),
                 Line(800+250j, 850+225j),
                 Arc(850+225j, 25+75j, -30, 0, 1, 900+200j),
                 Line(900+200j, 950+175j),
                 Arc(950+175j, 25+100j, -30, 0, 1, 1000+150j),
                 Line(1000+150j, 1050+125j)))
        
        
if __name__ == '__main__':
    unittest.main()