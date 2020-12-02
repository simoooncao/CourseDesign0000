import random
import turtle
import math


def hard_mode_init():
    global N, inf
    global points, start, end, dist, path

    def pt_dist2(a, b):
        x1, y1 = a
        x2, y2 = b
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def circumscribed_circle(triangle):
        a, b, c = triangle
        x1, y1 = a
        x2, y2 = b
        x3, y3 = c

        d = 4 * (x2 - x1) * (y3 - y2) - 4 * (y2 - y1) * (x3 - x2)
        d1 = 2 * (y3 - y1) * (y3 - y2) - 2 * (x1 - x3) * (x3 - x2)
        beta = d1 / d

        cx = (x1 + x2) / 2 - beta * (y2 - y1)
        cy = (y1 + y2) / 2 + beta * (x2 - x1)
        r = pt_dist2((x1, y1), (cx, cy))

        return (cx, cy), r

    def buffer_push(edge_set, pt1, pt2):
        if pt1[0] > pt2[0] or pt1[0] == pt2[0] and pt1[1] > pt2[1]:
            pt1, pt2 = pt2, pt1
        if (pt1, pt2) not in edge_set:
            edge_set.add((pt1, pt2))
        else:
            edge_set.remove((pt1, pt2))

    graph_init()
    N = random.randint(14, 18)
    for i in range(N):
        while True:
            x = random.uniform(-265, 265)
            y = random.uniform(-265, 265)
            if 125 <= x <= 300 and -300 <= y <= -240:
                continue
            for px, py in points:
                if (x - px) ** 2 + (y - py) ** 2 <= 100 ** 2:
                    break
            else:
                points.append((x, y))
                break

    point_number = {}
    for i, pt in enumerate(points):
        point_number[pt] = i
    vertics = sorted(points, key=lambda x: x[0])
    super_triangle = ((930, -310), (-930, -310), (0, 620))
    triangles = [super_triangle]
    temp_triangles = [super_triangle]
    for pt in vertics:
        edge_buffer = set()
        new_tmp_triangles = []
        for tg in temp_triangles:
            center, radius2 = circumscribed_circle(tg)
            if pt_dist2(center, pt) > radius2:
                if (pt[0] - center[0]) ** 2 > radius2:
                    triangles.append(tg)
                else:
                    new_tmp_triangles.append(tg)
            else:
                buffer_push(edge_buffer, tg[0], tg[1])
                buffer_push(edge_buffer, tg[1], tg[2])
                buffer_push(edge_buffer, tg[2], tg[0])

        for edge in edge_buffer:
            new_tmp_triangles.append((edge[0], edge[1], pt))
        temp_triangles = new_tmp_triangles

    triangles.extend(temp_triangles)
    triangles = [_ for _ in triangles if not (set(_) & set(super_triangle))]

    for x, y, z in triangles:
        # 去除钝角过大的三角形，防止挤在一起

        d = sorted([pt_dist2(x, y), pt_dist2(y, z), pt_dist2(z, x)])
        if (d[0] + d[1] - d[2]) / (2 * (d[0] * d[1]) ** 0.5) < math.cos(140 / 180 * math.pi):
            continue
        x = point_number[x]
        y = point_number[y]
        z = point_number[z]

        add_edge(dist, x, y)
        add_edge(dist, y, z)
        add_edge(dist, z, x)

    start = point_number[sorted(vertics[:N // 4], key=lambda x: x[1])[-1]]
    end = point_number[sorted(vertics[-(N // 4):], key=lambda x: x[1])[0]]
    draw_marks()

    floyed(dist)
    path = get_path(start, end)


def normal_mode_init():
    global N, inf
    global points, start, end, dist, path

    graph_init()
    column, row = random.randint(2, 3), random.randint(3, 4)
    column_pts = [1] + [row] * column + [1]
    N = sum(column_pts)
    start, end = 0, N - 1

    for i in range(column + 2):
        xs = 600 / (column + 2)
        ys = 600 / (column_pts[i] + 1)
        for j in range(column_pts[i]):
            points.append((-300 + xs / 2 + xs * i, 300 - (j + 1) * ys))

    # 起点终点的边
    for i in range(row):
        add_edge(dist, 0, i + 1)
        add_edge(dist, N - 1, N - i - 2)

    # 纵向边
    for i in range(column - 1):
        s1 = sum(column_pts[:i + 1])
        s2 = s1 + row
        for j in range(row):
            add_edge(dist, s1 + j, s2 + j)

    # 纵向边
    for i in range(column):
        s = sum(column_pts[:i + 1])
        for j in range(row - 1):
            add_edge(dist, s + j, s + j + 1)

    # 斜向边
    for i in range(column - 1):
        s1 = sum(column_pts[:i + 1])
        s2 = s1 + row
        for j in range(row - 1):
            if random.uniform(-10, 10) > 0:
                add_edge(dist, s1 + j, s2 + j + 1)
            else:
                add_edge(dist, s1 + j + 1, s2 + j)

    draw_marks()
    floyed(dist)
    path = get_path(start, end)


def easy_mode_init():
    global pic_number
    # pic_number = random.randint(3)
    # screen.bgpic('simple_{}.gif'.format(pic_number))
    draw_show_answer_zone()
    screen.update()


def graph_init():
    global inf, dist, points, path
    path = []
    points = []
    inf = 123456789
    dist = [[inf] * 24 for _ in range(24)]


def add_edge(array, x, y):
    if array[x][y] != inf:
        return

    if mode == 'hard':
        d = random.randint(20, 80)
    else:
        d = random.randint(6, 15)
    array[x][y] = array[y][x] = d


def floyed(array):
    for k in range(N):
        for i in range(N):
            for j in range(N):
                if i != j and j != k and k != i:
                    array[i][j] = min(array[i][j], array[i][k] + array[k][j])


def get_path(now, target):
    for i in range(N):
        if dist[now][i] + dist[i][target] == dist[now][target]:
            return get_path(now, i) + get_path(i, target)
    return [target]


def show_answer():
    if mode == 'easy':
        screen.bgcolor('gold')
        # screen.bgpic('simple_{}_answer.gif'.format(pic_number))
        screen.update()
        return

    Bob.penup()
    Bob.goto(points[start])
    Bob.pendown()
    Bob.pensize(4)

    last_pt = start
    for pt in path:
        Bob.color('lightskyblue')
        Bob.penup()
        Bob.goto(points[last_pt])
        Bob.pendown()
        Bob.goto(points[pt])
        Bob.color('orange')
        Bob.penup()
        Bob.goto((points[last_pt][0] + points[pt][0]) / 2, (points[last_pt][1] + points[pt][1]) / 2 - 5)
        Bob.pendown()
        Bob.write(dist[last_pt][pt], align='center', font=('Arial', 16, 'bold'))
        last_pt = pt

    screen.update()


def draw_show_answer_zone():
    Bob.penup()
    Bob.goto(130, -290)
    Bob.write('查看答案', font=('微软雅黑', 32))


def draw_marks():
    for i in range(N):
        for j in range(i + 1, N):
            if dist[i][j] != inf:
                Bob.color('darkgrey')
                Bob.penup()
                Bob.goto(points[i])
                Bob.pendown()
                Bob.goto(points[j])
                Bob.penup()
                Bob.goto((points[i][0] + points[j][0]) / 2, (points[i][1] + points[j][1]) / 2 - 5)
                Bob.pendown()
                Bob.color('orange')
                Bob.write(dist[i][j], align='center', font=('Arial', 16, 'bold'))

    Bob.color('black')
    for i in range(N):
        if i == start or i == end:
            continue
        Bob.penup()
        Bob.goto(points[i])
        Bob.pendown()
        Bob.dot(60)

    Bob.color('blue')
    Bob.penup()
    Bob.goto(points[start])
    Bob.dot(60)
    Bob.goto(points[start][0], points[start][1] - 8)
    Bob.color('white')
    Bob.write('起点', align='center', font=('Arial', 20, 'bold'))

    Bob.color('red')
    Bob.goto(points[end])
    Bob.dot(60)
    Bob.color('black')
    Bob.goto(points[end][0], points[end][1] - 10)
    Bob.write('终点', align='center', font=('Arial', 20, 'bold'))

    draw_show_answer_zone()
    screen.update()


def click(x, y):
    global status, mode
    # print(x , y)

    if status == 2:
        return

    if status == 0:
        if -175 <= y <= -75:
            if -250 <= x <= -150 and -150 <= y <= 50:
                mode = 'easy'
                Bob.clear()
                easy_mode_init()
                status = 1
            if -50 <= x <= 50 and -150 <= y <= 50:
                mode = 'normal'
                Bob.clear()
                normal_mode_init()
                status = 1
            if 150 <= x <= 250 and -150 <= y <= 50:
                mode = 'hard'
                Bob.clear()
                status = 1
                hard_mode_init()

    if status == 1:
        if 125 <= x <= 300 and -300 <= y <= -240:
            show_answer()
            status = 2


def _background():
    Bob.goto(0, 100)
    Bob.write('寻找最短路径', align='center', font=('微软雅黑', 48))

    btn = [(-250, -100), (-50, -100), (150, -100)]
    text = ['easy', 'normal', 'hard']
    width, height = 100, 75

    Bob.pensize(5)
    for i in range(3):
        Bob.penup()
        Bob.goto(btn[i])
        Bob.pendown()

        for j in range(2):
            Bob.forward(width)
            Bob.right(90)
            Bob.forward(height)
            Bob.right(90)

        Bob.penup()
        Bob.goto(btn[i][0] + width / 2, btn[i][1] - height / 2 - 10)
        Bob.pendown()
        Bob.write(text[i], align='center', font=('Arial', 20))
    Bob.pensize(1)
    screen.update()


Bob = turtle.Turtle()
Bob.penup()
Bob.speed(0)
Bob.hideturtle()

screen = turtle.Screen()
screen.tracer(0)
screen.onclick(click)

status = 0
_background()
turtle.done()
