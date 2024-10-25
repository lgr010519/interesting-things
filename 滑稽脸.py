from time import sleep
from turtle import *

setup(width=740, height=900, startx=700, starty=200);
pensize(8); speed(9);

def face():
    color("black", "yellow");
    begin_fill(); circle(150); end_fill();
    color("black", "black");
def mouse():
    pencolor("red"); pensize(5);
    up(); circle(120,80); rt(180); down();
    circle(-120,160);
    pencolor("black"); pensize(8);
def eye():
    lt(46);
    fillcolor("white");
    begin_fill();
    circle(-50,30); circle(-130,43); circle(-15,172); circle(130,38); circle(-17,150);
    end_fill();
    fillcolor("black");
    begin_fill(); circle(-16); end_fill();

up(); rt(90); fd(120); lt(90); down();
face();
up(); lt(90); fd(30); rt(90); down();
mouse();
up();circle(-120, 100);rt(90);fd(70);lt(90);fd(20);down();
eye();
up(); setheading(180); fd(180); rt(180); down();
eye();
done();
