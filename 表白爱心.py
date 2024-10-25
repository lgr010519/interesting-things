 
# 开发时间： 2023/11/20 23:12
import math
 
import random
import threading
import time
from math import sin, cos, pi, log
from tkinter import *
import re
 
Fireworks = []
maxFireworks = 8
CANVAS_WIDTH = 1080  # 画布的宽
CANVAS_HEIGHT = 600  # 画布的高
CANVAS_CENTER_X = CANVAS_WIDTH / 2  # 画布中心的X轴坐标
CANVAS_CENTER_Y = CANVAS_HEIGHT / 2  # 画布中心的Y轴坐标
 
IMAGE_ENLARGE = 12  # 放大比例
HEART_COLOR = "pink"  # 心的颜色
 
 
# 烟花类
class firework(object):
    def __init__(self, color, speed, width, height):
        # uid=uuid.uuid1()
        self.radius = random.randint(2,3)  # 粒子半径为2~3像素
        self.color = color  # 粒子颜色
        self.speed = speed  # speed是1.5-3.5秒
        self.status = 0  # 在烟花未爆炸的情况下，status=0；爆炸后，status>=1；当status>100时，烟花的生命期终止
        self.nParticle = random.randint(80, 100)  # 粒子数量
        self.center = [random.randint(0, width - 15), random.randint(0, height - 15)]  # 烟花随机中心坐标
        self.oneParticle = []  # 原始粒子坐标（100%状态时）
        self.rotTheta = random.uniform(-1, 2 * math.pi)  # 椭圆平面旋转角
 
        # 椭圆参数方程：x=a*cos(theta),y=b*sin(theta)
        # ellipsePara=[a,b]
 
        self.ellipsePara = [random.randint(30, 40), random.randint(20, 30)]
        theta = 2 * math.pi / self.nParticle
        for i in range(self.nParticle):
            t = random.uniform(-1.0 / 16, 1.0 / 16)  # 产生一个 [-1/16,1/16) 的随机数
            x, y = self.ellipsePara[0] * math.cos(theta * i + t), self.ellipsePara[1] * math.sin(
                theta * i + t)  # 椭圆参数方程
            xx, yy = x * math.cos(self.rotTheta) - y * math.sin(self.rotTheta), y * math.cos(
                self.rotTheta) + x * math.sin(self.rotTheta)  # 平面旋转方程
            self.oneParticle.append([xx, yy])
 
        self.curParticle = self.oneParticle[0:]  # 当前粒子坐标
        self.thread = threading.Thread(target=self.extend)  # 建立线程对象
 
    def extend(self):  # 粒子群状态变化函数线程
        for i in range(100):
            self.status += 1  # 更新状态标识
            self.curParticle = [[one[0] * self.status / 100, one[1] * self.status / 100] for one in
                                self.oneParticle]  # 更新粒子群坐标
            time.sleep(self.speed / 50)
 
    def explode(self):
        self.thread.setDaemon(True)  # 把现程设为守护线程
        self.thread.start()  # 启动线程
 
    def __repr__(self):
        return ('color:{color}'
                ''
                'speed:{speed}'
                ''
                'number of particle: {np}'
                ''
                'center:[{cx} , {cy}]'
                ''
                'ellipse:a={ea} , b={eb}'
                ''
                'particle:'
                '{p}'
                ''
                ).format(color=self.color, speed=self.speed, np=self.nParticle, cx=self.center[0], cy=self.center[1],
                         p=str(self.oneParticle), ea=self.ellipsePara[0], eb=self.ellipsePara[1])
 
 
def colorChange(fire):
    rgb = re.findall(r'(.{2})', fire.color[1:])
    cs = fire.status
 
    f = lambda x, c: hex(int(int(x, 16) * (100 - c) / 30))[2:]  # 当粒子寿命到70%时，颜色开始线性衰减
    if cs > 70:
        ccr, ccg, ccb = f(rgb[0], cs), f(rgb[1], cs), f(rgb[2], cs)
    else:
        ccr, ccg, ccb = rgb[0], rgb[1], rgb[2]
 
    return '#{0:0>2}{1:0>2}{2:0>2}'.format(ccr, ccg, ccb)
 
 
def appendFirework(n=1):  # 递归生成烟花对象
    if n > maxFireworks or len(Fireworks) > maxFireworks:
        pass
    elif n == 1:
        cl = '#{0:0>6}'.format(hex(int(random.randint(0, 16777215)))[2:])  # 产生一个0~16777215（0xFFFFFF）的随机数，作为随机颜色
        a = firework(cl, random.uniform(1.5, 3.5), CANVAS_WIDTH, CANVAS_HEIGHT)
        Fireworks.append({'particle': a, 'points': []})  # 建立粒子显示列表，‘particle’为一个烟花对象，‘points’为每一个粒子显示时的对象变量集
        a.explode()
    else:
        appendFirework()
        appendFirework(n - 1)
 
 
def show(c):
    for p in Fireworks:  # 每次刷新显示，先把已有的所以粒子全部删除
        for pp in p['points']:
            c.delete(pp)
 
    for p in Fireworks:  # 根据每个烟花对象，计算其中每个粒子的显示对象
        oneP = p['particle']
        if oneP.status == 100:  # 状态标识为100，说明烟花寿命结束
            Fireworks.remove(p)  # 移出当前烟花
            appendFirework()  # 新增一个烟花
            continue
        else:
            li = [[int(cp[0] * 2) + oneP.center[0], int(cp[1] * 2) + oneP.center[1]] for cp in
                  oneP.curParticle]  # 把中心为原点的椭圆平移到随机圆心坐标上
            color = colorChange(oneP)  # 根据烟花当前状态计算当前颜色
            for pp in li:
                p['points'].append(
                    c.create_oval(pp[0] - oneP.radius, pp[1] - oneP.radius, pp[0] + oneP.radius, pp[1] + oneP.radius,
                                  fill=color))  # 绘制烟花每个粒子
 
    root.after(10, show, c)  # 回调，每10ms刷新一次
 
 
def heart_function(t, shrink_ratio: float = IMAGE_ENLARGE):
    """
    “爱心函数生成器”
    :param shrink_ratio: 放大比例
    :param t: 参数
    :return: 坐标
    """
    # 基础函数
    x = 16 * (sin(t) ** 3)
    y = -(13 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(4 * t))
 
    # 放大
    x *= shrink_ratio
    y *= shrink_ratio
 
    # 移到画布中央
    x += CANVAS_CENTER_X
    y += CANVAS_CENTER_Y
 
    return int(x), int(y)
 
 
def scatter_inside(x, y, beta=0.15):
    """
    随机内部扩散
    :param x: 原x
    :param y: 原y
    :param beta: 强度
    :return: 新坐标
    """
    ratio_x = - beta * log(random.random())
    ratio_y = - beta * log(random.random())
 
    dx = ratio_x * (x - CANVAS_CENTER_X)
    dy = ratio_y * (y - CANVAS_CENTER_Y)
 
    return x - dx, y - dy
 
 
def shrink(x, y, ratio):
    """
    抖动
    :param x: 原x
    :param y: 原y
    :param ratio: 比例
    :return: 新坐标
    """
    force = -1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.6)  # 这个参数...
    dx = ratio * force * (x - CANVAS_CENTER_X)
    dy = ratio * force * (y - CANVAS_CENTER_Y)
    return x - dx, y - dy
 
 
def curve(p):
    """
    自定义曲线函数，调整跳动周期
    :param p: 参数
    :return: 正弦
    """
    return 4 * (2 * sin(4 * p)) / (2 * pi)
 
 
class Heart:
    """
    爱心类
    """
 
    def __init__(self, generate_frame=20):
        self._points = set()  # 原始爱心坐标集合
        self._edge_diffusion_points = set()  # 边缘扩散效果点坐标集合
        self._center_diffusion_points = set()  # 中心扩散效果点坐标集合
        self.all_points = {}  # 每帧动态点坐标
        self.build(2000)
 
        self.random_halo = 1000
 
        self.generate_frame = generate_frame
        for frame in range(generate_frame):
            self.calc(frame)
 
    def build(self, number):
        # 爱心
        for _ in range(number):
            t = random.uniform(0, 2 * pi)  # 随机不到的地方造成爱心有缺口
            x, y = heart_function(t)
            self._points.add((x, y))
 
        # 爱心内扩散
        for _x, _y in list(self._points):
            for _ in range(3):
                x, y = scatter_inside(_x, _y, 0.05)
                self._edge_diffusion_points.add((x, y))
 
        # 爱心内再次扩散
        point_list = list(self._points)
        for _ in range(4000):
            x, y = random.choice(point_list)
            x, y = scatter_inside(x, y, 0.17)
            self._center_diffusion_points.add((x, y))
 
    @staticmethod
    def calc_position(x, y, ratio):
        # 调整缩放比例
        force = 1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.520)
 
        dx = ratio * force * (x - CANVAS_CENTER_X) + random.randint(-1, 1)
        dy = ratio * force * (y - CANVAS_CENTER_Y) + random.randint(-1, 1)
 
        return x - dx, y - dy
 
    def calc(self, generate_frame):
        ratio = 10 * curve(generate_frame / 10 * pi)  # 圆滑的周期的缩放比例
 
        halo_radius = int(4 + 6 * (1 + curve(generate_frame / 10 * pi)))
        halo_number = int(3000 + 4000 * abs(curve(generate_frame / 10 * pi) ** 2))
 
        all_points = []
 
        # 光环
        heart_halo_point = set()  # 光环的点坐标集合
        for _ in range(halo_number):
            t = random.uniform(0, 2 * pi)  # 随机不到的地方造成爱心有缺口
            x, y = heart_function(t, shrink_ratio=11)
            x, y = shrink(x, y, halo_radius)
            if (x, y) not in heart_halo_point:
                # 处理新的点
                heart_halo_point.add((x, y))
                x += random.randint(-11, 11)
                y += random.randint(-11, 11)
                size = random.choice((1, 2, 2))  # 控制外围粒子的大小
                all_points.append((x, y, size))
 
        # 轮廓
        for x, y in self._points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 3)
            all_points.append((x, y, size))
 
        # 内容
        for x, y in self._center_diffusion_points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))
 
        self.all_points[generate_frame] = all_points
 
    def render(self, render_canvas, render_frame):
        for x, y, size in self.all_points[render_frame % self.generate_frame]:
            render_canvas.create_rectangle(x, y, x + size, y + size, width=0, fill=HEART_COLOR)
 
 
def draw(main: Tk, render_canvas: Canvas, render_heart: Heart, render_frame=0):
    render_canvas.delete('all')
    render_heart.render(render_canvas, render_frame)
    main.after(160, draw, main, render_canvas, render_heart, render_frame + 1)
 
 
 
 
if __name__ == '__main__':
    appendFirework(maxFireworks)
 
    root = Tk()  # 一个Tk
    canvas = Canvas(root, bg='black', height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
    canvas.create_rectangle(0, 0, CANVAS_HEIGHT, CANVAS_WIDTH, fill="black")
    canvas.pack()
    root.after(10, show, canvas)
    heart = Heart()  # 心
    draw(root, canvas, heart)  # 开始画画~
 
    root.mainloop()
