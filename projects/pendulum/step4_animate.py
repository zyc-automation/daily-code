# -*- coding: utf-8 -*-
"""
台阶 4 动画版：小车 + 倒立摆 PD 控制 —— 动态演示
==================================================
运行后你会看到：
  1. 一辆蓝色小车，上面立着一根红色摆杆；
  2. 摆杆一开始偏 10°，PD 控制让小车"追"摆杆，把它扶正；
  3. 摆杆立住了，但小车自己一路滑走（因为没有摩擦、也没有人管小车位置）。

⚠️ 注意：本文件包含台阶 4 的【完整答案】，建议先独立填完 step4_cart_pole_pd.py 再看。
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle, Circle

# ============ 第 1 部分：仿真（台阶 4 的完整答案） ============
M, m, l = 1.0, 0.2, 0.3
I = (1/3) * m * l**2
g = 9.81
Kp, Kd = 30.0, 6.0
dt = 0.001
t_end = 4.0

x, x_dot = 0.0, 0.0
theta, theta_dot = np.radians(10), 0.0
time_list, x_list, theta_list = [], [], []
t = 0.0
while t < t_end:
    s, c = np.sin(theta), np.cos(theta)
    F = Kp * theta + Kd * theta_dot
    A = np.array([[M + m, m * l * c],
                  [m * l * c, I + m * l**2]])
    b_vec = np.array([F + m * l * s * theta_dot**2,
                      m * g * l * s])
    x_ddot, theta_ddot = np.linalg.solve(A, b_vec)
    x_dot = x_dot + x_ddot * dt
    x = x + x_dot * dt
    theta_dot = theta_dot + theta_ddot * dt
    theta = theta + theta_dot * dt
    time_list.append(t); x_list.append(x); theta_list.append(theta)
    t += dt

# ============ 第 2 部分：动画 ============
pole_len = 2 * l     # 摆杆全长（l 是半长）
cart_w, cart_h = 0.4, 0.2

fig, ax = plt.subplots(figsize=(10, 5))
ax.set_xlim(-1.5, 4.5)
ax.set_ylim(-0.6, 1.2)
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)
ax.set_title('小车 + 倒立摆 PD 控制 —— 动态演示', fontsize=13)

# 轨道（小车在上面滑）
ax.axhline(y=0, color='gray', linewidth=2, alpha=0.5)

# 小车（矩形，左下角初始在原点附近）
cart = Rectangle((-cart_w/2, 0), cart_w, cart_h,
                 facecolor='steelblue', edgecolor='black', linewidth=1.5)
ax.add_patch(cart)

# 摆杆（线段，起点在小车顶部中心）
(pole,) = ax.plot([], [], color='darkred', lw=4, solid_capstyle='round')

# 摆杆末端的小球
ball = Circle((0, 0), 0.06, facecolor='crimson', edgecolor='black')
ax.add_patch(ball)

# 左上角信息
text = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=11,
               va='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))

def update(i):
    xi = x_list[i]          # 当前小车位置
    th = theta_list[i]      # 当前摆杆角度
    # 1) 移动小车矩形
    cart.set_xy((xi - cart_w / 2, 0))
    # 2) 摆杆起点 = 小车顶部中心，末端沿摆杆方向延伸
    pivot_y = cart_h
    tip_x = xi + pole_len * np.sin(th)
    tip_y = pivot_y + pole_len * np.cos(th)
    pole.set_data([xi, tip_x], [pivot_y, tip_y])
    ball.set_center((tip_x, tip_y))
    # 3) 更新信息
    text.set_text('t=%.2fs  θ=%.1f°  x=%.2fm' % (time_list[i], np.degrees(th), xi))
    return cart, pole, ball, text

frames = range(0, len(time_list), 20)
ani = FuncAnimation(fig, update, frames=frames, interval=30, blit=True)
plt.show()
