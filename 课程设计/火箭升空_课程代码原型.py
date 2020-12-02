import turtle
import random

rise = []
fall = []

screen = turtle.Screen()
screen.bgpic('天空1.gif')
screen.tracer(0)

# 遍历图片文件列表，切换形象
rocket_shapes = ['火箭碎片1.gif', '火箭碎片2.gif', '火箭碎片3.gif', '火箭碎片4.gif', '火箭碎片5.gif']
for shapes in rocket_shapes:
    component = turtle.Turtle()
    component.penup()
    component.left(90)
    screen.register_shape(shapes)
    component.shape(shapes)
    rise.append(component)
rise[0].goto(60 , -100)
rise[1].goto(0 , -100)
rise[2].goto(0 , -100)

# 场景编号
stage = 0
stage_pics = ['天空1.gif' , '天空2.gif' , '天空1.gif' , '天空2.gif' , '天空1.gif' , '天空2.gif' , '天空1.gif']

while True:
    for up in rise:
        up.forward(1)
    for down in fall:
        down.backward(10)

    if rise[0].ycor() > 300 + 100:
        stage = stage + 1
        if stage >= 7:
            break
        screen.bgpic(stage_pics[stage])
        for each in rise:
            each.sety(each.ycor() - 650)

    if stage == 1 and rise[0].ycor() == 0:
        fall.append(rise[0])
        rise.pop(0)
        fall.append(rise[0])
        rise.pop(0)
    if stage == 3 and rise[0].ycor() == 0:
        fall.append(rise[0])
        rise.pop(0)
    if stage == 5 and rise[0].ycor() == 0:
        fall.append(rise[0])
        rise.pop(0)

    screen.update()