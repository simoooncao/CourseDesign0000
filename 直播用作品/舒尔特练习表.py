import turtle
import random
import time

N = 5
SIDE_COLOR = 'black'  # 边框颜色
SIDE_SIZE = 5  # 边框粗度
FILL_COLOR = 'yellow'  # 选中后填充颜色
NUMBER_COLOR = 'black'  # 数字颜色
TIME_COLOR = 'black'  # 计时器颜色
TIME_FONT_SIZE = 40  # 计时器字体大小
SQUARE_DY = -30  # 整体y方向偏移量

if N < 4:
    N = 4
if N > 15:
    N = 15
SQUARE = 500 / N

FONT_FACTOR = 0.7
MAX_TEXT = 2 if N < 10 else 3
NUMBER_FONT_SIZE = int(SQUARE / 2 / MAX_TEXT / FONT_FACTOR)

screen = turtle.Screen()
screen.tracer(0)

t_number = turtle.Turtle()
t_number.pencolor(SIDE_COLOR)
t_number.fillcolor(FILL_COLOR)
t_number.pensize(SIDE_SIZE)
t_number.penup()
t_number.hideturtle()

t_time = turtle.Turtle()
t_time.hideturtle()
t_time.penup()
t_time.fillcolor(TIME_COLOR)
t_time.goto(0, -250 + SQUARE_DY - TIME_FONT_SIZE * FONT_FACTOR)


def init():
    global numbers
    global x1, y1, x2, y2

    numbers = random.sample(range(1, N * N + 1), N * N)
    x1 = -N / 2 * SQUARE
    x2 = N / 2 * SQUARE
    y1 = 50 + SQUARE_DY - N / 2 * SQUARE
    y2 = 50 + SQUARE_DY + N / 2 * SQUARE

    for i in range(N + 1):
        t_number.goto(x1, y2 - i * SQUARE)
        t_number.pendown()
        t_number.forward(N * SQUARE)
        t_number.penup()

    t_number.right(90)
    for i in range(N + 1):
        t_number.goto(x1 + i * SQUARE, y2)
        t_number.pendown()
        t_number.forward(N * SQUARE)
        t_number.penup()
    t_number.left(90)

    t_number.fillcolor(NUMBER_COLOR)
    for i in range(N):
        for j in range(N):
            t_number.goto(x1 + (j + 0.5) * SQUARE, y2 - (i + 0.5) * SQUARE - NUMBER_FONT_SIZE * FONT_FACTOR)
            t_number.write(numbers[i * N + j], align='center', font=('Arial', NUMBER_FONT_SIZE, 'bold'))


def click(x, y):
    global next, end_time

    # print(x , y)

    if not x1 <= x <= x2 and y1 <= y <= y2:
        return
    if next > N * N:
        return

    j = int((x - x1) / SQUARE)
    i = int((y2 - y) / SQUARE)

    # print(i , j)
    # print(next , numbers[i * N + j])

    if numbers[i * N + j] != next:
        return

    t_number.fillcolor(FILL_COLOR)
    t_number.goto(x1 + j * SQUARE, y2 - i * SQUARE)

    t_number.begin_fill()
    for k in range(4):
        t_number.forward(SQUARE)
        t_number.right(90)
    t_number.end_fill()
    t_number.pendown()
    for k in range(4):
        t_number.forward(SQUARE)
        t_number.right(90)
    t_number.penup()

    t_number.goto(x1 + (j + 0.5) * SQUARE, y2 - (i + 0.5) * SQUARE - NUMBER_FONT_SIZE * FONT_FACTOR)
    t_number.fillcolor(NUMBER_COLOR)
    t_number.write(numbers[i * N + j], align='center', font=('Arial', NUMBER_FONT_SIZE, 'bold'))

    next += 1
    if next > N * N:
        end_time = time.time()
    screen.update()


def my_timer():
    global start_time

    if start_time == 0:
        start_time = time.time()
    if end_time == 0:
        now = time.time()
    else:
        now = end_time

    t_time.clear()
    dt = now - start_time
    m, s, ms = int(dt / 60), int(dt % 60), round((dt - int(dt)) * 1000)

    # t_time.write("{0:02d}:{1:02d}:{2:03d}".format(m , s , ms) , align = 'center' , font = ('Arial' , TIME_FONT_SIZE))
    def to_str(x, figure):
        x = str(x)
        if len(x) < figure:
            x = '0' * (figure - len(x)) + x
        return x

    m, s, ms = to_str(m, 2), to_str(s, 2), to_str(ms, 3)
    t_time.write(m + ':' + s + ':' + ms, align='center', font=('Arial', TIME_FONT_SIZE))
    screen.update()

    if end_time == 0:
        screen.ontimer(my_timer, 31)


next = 1
start_time = 0
end_time = 0

screen.onclick(click)
init()
# print(numbers)
# print(x1 , x2 , y1 , y2)
my_timer()

turtle.done()