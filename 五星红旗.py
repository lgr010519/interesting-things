#五星红旗
import turtle as t
 
t.setup(600,400,200,200)
 
t.speed(1)
 
t.penup()
t.goto(-100,-50)
t.pendown()
t.color("red","red")
t.pensize(2)
t.begin_fill()
for i in range(2):
    t.forward(240)
    t.left(90)
    t.forward(160)
    t.left(90)
t.end_fill()
 
t.color("yellow","yellow")
t.penup()
t.goto(-80,80)
t.pendown()
t.begin_fill()
for i in range(5):
    t.forward(30)
    t.right(144)
t.end_fill()
 
 
t.penup()
t.goto(-40,95)
t.pendown()
t.seth(-30)
t.begin_fill()
for i in range(5):
    t.forward(10)
    t.right(144)
t.end_fill()
 
t.penup()
t.goto(-40,55)
t.pendown()
t.begin_fill()
for i in range(5):
    t.forward(10)
    t.right(144)
t.end_fill()
 
t.penup()
t.goto(-25,62)
t.pendown()
t.seth(10)
t.begin_fill()
for i in range(5):
    t.forward(10)
    t.right(144)
t.end_fill()
 
t.penup()
t.goto(-25,78)
t.pendown()
t.seth(20)
t.begin_fill()
for i in range(5):
    t.forward(10)
    t.right(144)
t.end_fill()
 
t.penup()
t.goto(-130,-150)
t.pendown()
t.color("red","red")
t.write("祝祖国妈妈生日快乐", font=('Arial', 40, 'normal'))
 
t.done()
