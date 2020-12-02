import turtle, random


def onDraw(number):
    draw = painter[number]

    def _draw():
        draw.begin_fill()
        if number == 0:
            draw.right(30)
            for i in range(3):
                draw.forward(60)
                draw.right(120)
            draw.left(30)
        elif number == 1 or number == 2:
            for i in range(2):
                draw.right(90)
                draw.forward(60)
                draw.right(90)
                draw.forward(100)
        elif number == 3:
            pos = draw.position()
            draw.right(180)
            draw.forward(100)
            draw.right(90)
            draw.forward(60)
            draw.right(90)
            draw.goto(pos)
        else:
            pos = draw.position()
            draw.left(180)
            draw.forward(100)
            draw.left(90)
            draw.forward(60)
            draw.left(90)
            draw.goto(pos)
        draw.end_fill()

    return _draw


rise = []
fall = []
painter = []
func = {}

screen = turtle.Screen()
screen.bgcolor('deepskyblue')
screen.tracer(0)
screen.colormode(255)

colors = ['red', 'orangered', 'orange', 'darkorange', 'darkorange']
pos = [(0, 0), (0, 0), (0, -100), (0, -100), (60, -100)]
for i in range(5):
    tmp = turtle.Turtle()
    tmp.penup()
    tmp.hideturtle()
    tmp.left(90)
    tmp.color(colors[i])
    tmp.goto(pos[i])
    painter.append(tmp)
    rise.append(tmp)
    func[tmp] = onDraw(i)
    func[tmp]()

stage = 0
speed = 20
separation = False
while True:
    for i in painter:
        i.clear()

    if rise[-1].ycor() > 300 + 100:
        # 切换场景，清理下落零件

        stage += 1
        if stage >= 5:
            break

        screen.bgcolor((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

        separation = False
        fall = []

        dist = -2 * rise[-1].ycor()
        for i in rise:
            i.sety(i.ycor() + dist)

    for up in rise:
        up.forward(5 / speed)
        func[up]()
    for down in fall:
        down.backward(5 / speed)
        func[down]()

    if not separation and rise[-1].ycor() >= 0:
        if stage == 1:
            separation = True
            fall.append(rise.pop())
            fall.append(rise.pop())
        elif stage == 2:
            separation = True
            fall.append(rise.pop())
        elif stage == 3:
            separation = True
            fall.append(rise.pop())

    screen.update()