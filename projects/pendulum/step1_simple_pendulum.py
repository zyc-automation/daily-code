# -*- coding: utf-8 -*-
"""
台阶 1：自由单摆（无控制）
============================
目标：用高中物理 + 欧拉积分，让一根摆杆在重力下自然摆动。

你需要完成 3 个填空（标了 TODO），填完后运行，就能看到单摆角度随时间的变化曲线。

【物理知识，高中就够】
    单摆的角加速度公式：  θ'' = -(g / L) · sin(θ)
    - g：重力加速度 9.81 m/s²
    - L：摆长
    - θ：摆杆与竖直方向的夹角（弧度）
    - 负号表示：摆杆偏离竖直方向时，重力会把它"往回拉"

【数学工具：欧拉积分——用"现在"算"下一步"】
    新角速度 = 旧角速度 + 角加速度 × 时间步长
    新角度   = 旧角度   + 角速度   × 时间步长

【运行方式】
    在命令行执行：  python step1_simple_pendulum.py
    （或在你用的 IDE 里直接运行）

【填完后的预期】
    你会看到一条"波浪线"（正弦曲线），说明摆杆在来回摆动。
"""

import numpy as np
import matplotlib.pyplot as plt

# ---------- 1. 物理参数 ----------
g = 9.81      # 重力加速度 (m/s²)
L = 1.0       # 摆长 (m)

# ---------- 2. 模拟参数 ----------
dt = 0.01     # 时间步长 (s)
t_end = 5.0   # 模拟总时长 (s)

# ---------- 3. 初始状态 ----------
theta = np.radians(45)   # 初始角度 45°（转成弧度）
theta_dot = 0.0          # 初始角速度 0（静止释放）

# ---------- 4. 模拟循环 ----------
time_list = []    # 记录每个时刻
theta_list = []   # 记录每个时刻的角度

t = 0.0
while t < t_end:
    # 【TODO 1】写出单摆的角加速度
    # 公式：theta_ddot = -(g / L) * sin(theta)
    # 提示：用 np.sin() 算正弦
    theta_ddot = -(g / L) * np.sin(theta)

    # 【TODO 2】欧拉积分：更新角速度
    # 新角速度 = 旧角速度 + 角加速度 * dt
    theta_dot = theta_dot + theta_ddot * dt

    # 【TODO 3】欧拉积分：更新角度
    # 新角度 = 旧角度 + 角速度 * dt
    theta = theta + theta_dot *dt

    # 记录数据（这行不用改）
    time_list.append(t)
    theta_list.append(theta)

    # 时间前进（这行不用改）
    t += dt

# ---------- 5. 画图 ----------
plt.plot(time_list, theta_list)
plt.xlabel('时间 (s)')
plt.ylabel('角度 (弧度)')
plt.title('自由单摆：角度随时间变化')
plt.grid(True)
plt.show()
