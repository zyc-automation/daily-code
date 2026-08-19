# -*- coding: utf-8 -*-
"""
台阶 3 动画版：倒立摆 PD 控制 —— 动态演示
==========================================
运行这个文件，你会看到一根摆杆：
  1. 一开始从 15° 倒向一侧；
  2. 被 PD 控制"扶正"；
  3. 最终稳稳立在竖直向上，不再晃动。

⚠️ 注意：这个文件里包含台阶 3 的【完整答案】。
   建议你先独立填完 step3_inverted_pendulum_pd.py，再来运行这个动画对照看效果。

【动画代码在干什么】
   动画部分用的是 matplotlib 的 FuncAnimation：
   - 每一帧，根据当前角度 θ 算出摆杆末端的位置；
   - 摆杆末端坐标 = (L·sinθ, L·cosθ)，θ=0 时就是竖直向上 (0, L)；
   - 不断更新这条线段的端点，摆杆就"动起来"了。
   动画是可视化工具，不用你手写，看懂"它在更新摆杆端点"即可。
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ============ 第 1 部分：仿真（台阶 3 的完整答案） ============
g = 9.81
L = 1.0
m = 0.5
I = m * L**2

Kp = 20.0
Kd = 5.0

dt = 0.001
t_end = 5.0

theta = np.radians(15)
theta_dot = 0.0

time_list = []
theta_list = []

t = 0.0
while t < t_end:
    tau = -Kp * theta - Kd * theta_dot              # PD 控制
    theta_ddot = (g / L) * np.sin(theta) + tau / I  # 角加速度
    theta_dot = theta_dot + theta_ddot * dt         # 更新角速度
    theta = theta + theta_dot * dt                  # 更新角度
    time_list.append(t)
    theta_list.append(theta)
    t += dt

# ============ 第 2 部分：动画 ============
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)
ax.set_title('倒立摆 PD 控制 —— 动态演示', fontsize=13)

# 灰色虚线：目标位置（竖直向上 θ=0）
ax.plot([0, 0], [0, 1.3], '--', color='gray', alpha=0.6)

# 转轴点（原点）
ax.plot(0, 0, 'ko', markersize=8, zorder=3)

# 摆杆：先画一条空线段，之后每一帧更新它的端点
(line,) = ax.plot([], [], 'o-', lw=4, color='crimson', markersize=9, zorder=2)

# 左上角显示当前时间和角度
text = ax.text(0.02, 0.97, '', transform=ax.transAxes, fontsize=11,
               va='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))

def update(frame_idx):
    """画第 frame_idx 帧：根据当前角度，更新摆杆端点位置。"""
    th = theta_list[frame_idx]
    tip_x = L * np.sin(th)   # 末端水平偏移
    tip_y = L * np.cos(th)   # 末端竖直高度
    line.set_data([0, tip_x], [0, tip_y])
    text.set_text('t = %.2f s\nθ = %.1f°' % (time_list[frame_idx], np.degrees(th)))
    return line, text

# 每 25 个数据点取一帧（共约 200 帧），interval 控制播放速度(毫秒)
frames = range(0, len(time_list), 25)
ani = FuncAnimation(fig, update, frames=frames, interval=40, blit=True)

plt.show()
