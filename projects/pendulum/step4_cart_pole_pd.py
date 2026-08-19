# -*- coding: utf-8 -*-
"""
台阶 4：小车 + 倒立摆(完整 cart-pole 模型)+ PD 控制
======================================================
目标：摆杆立在一辆能左右移动的小车上，通过给小车施加水平力 F，让摆杆保持竖直。

【和台阶 3 的本质区别】
    台阶 3：摆杆绕"固定转轴"转，你直接用"力矩 τ"掰摆杆。
    台阶 4：摆杆立在小车上，你只能给"小车"施加水平力 F——
            靠"移动小车"来间接扶正摆杆（就像手指顶筷子，手移动、筷子才立住）。

【系统的状态(4 个量)】
    x      ：小车位置
    x_dot  ：小车速度
    theta  ：摆杆与竖直向上方向的夹角
    theta_dot：摆杆角速度
    这 4 个量完全描述了小车和摆杆在任意时刻的样子。

【物理：两个耦合方程】
    小车和摆杆是"绑在一起"的，所以要联立两个方程才能解出加速度。
    这里先忽略摩擦(简化)，方程如下：

    方程①(小车水平方向)：
        (M+m)·x_ddot + m·l·cosθ·θ_ddot = F + m·l·sinθ·θ_dot²
    方程②(摆杆转动)：
        m·l·cosθ·x_ddot + (I+m·l²)·θ_ddot = m·g·l·sinθ

    两个方程、两个未知数(x_ddot 和 θ_ddot)，写成矩阵形式：
        A · [x_ddot, θ_ddot]^T = b_vec
    然后用 np.linalg.solve 一次解出来。

【⚠️ 关键：控制符号反了！】
    台阶 3 是"力矩直接掰摆杆"：θ>0(右偏) → 用逆时针力矩 → τ = -Kp·θ
    台阶 4 是"力作用在小车上"：θ>0(摆杆右偏) → 要让小车也往右开，
        摆杆才会因为"支点跑了"而往回倒 → F 和 θ 同号 → F = +Kp·θ + Kd·θ_dot
    所以 PD 公式里的符号和台阶 3 相反，这是台阶 4 最反直觉、也最关键的点。

【你需要完成 8 个填空】
    TODO 1：PD 控制力 F（注意符号！）
    TODO 2：构造 A 矩阵（两个方程的系数）
    TODO 3：构造 b_vec（两个方程的右边）
    TODO 4：联立求解 x_ddot 和 theta_ddot
    TODO 5~8：欧拉积分更新 4 个状态

【填完后的预期】
    上图(θ)：摆杆从 10° 被扶正，收敛到 0（摆杆立住了）。
    下图(x)：小车在扶正过程中"跑偏"了一段距离，然后停在那里——
            因为 PD 只反馈了摆杆角度，没管小车位置。这正是台阶 5(LQR)要解决的。
"""

import numpy as np
import matplotlib.pyplot as plt

# ---------- 1. 物理参数 ----------
M = 1.0              # 小车质量 (kg)
m = 0.2              # 摆杆质量 (kg)
l = 0.3              # 摆杆半长 (m)
I = (1/3) * m * l**2 # 摆杆绕质心的转动惯量（均匀细杆公式）
g = 9.81             # 重力加速度

# ---------- 2. 控制参数 ----------
Kp = 30.0            # 比例增益
Kd = 6.0             # 微分增益

# ---------- 3. 模拟参数 ----------
dt = 0.001
t_end = 6.0

# ---------- 4. 初始状态 ----------
x = 0.0                       # 小车初始位置
x_dot = 0.0                   # 小车初始速度
theta = np.radians(10)        # 摆杆初始角度 10°
theta_dot = 0.0               # 摆杆初始角速度

time_list = []
x_list = []
theta_list = []

t = 0.0
while t < t_end:
    # 预计算三角函数
    sin_theta = np.sin(theta)
    cos_theta = np.cos(theta)

    # 【TODO 1】PD 控制力 F
    # 力作用在"小车"上！摆杆右偏(θ>0)→小车往右开→摆杆往回倒
    # 所以 F 和 θ 同号（符号和台阶 3 的力矩相反）
    # 公式：F = Kp * theta + Kd * theta_dot
    F = Kp * theta + Kd * theta_dot
    # 【TODO 2】构造 A 矩阵
    # 方程①：(M+m)·x_ddot + m·l·cosθ·θ_ddot = F + m·l·sinθ·θ_dot²
    # 方程②：m·l·cosθ·x_ddot + (I+m·l²)·θ_ddot = m·g·l·sinθ
    # A = [[第一行 x_ddot 系数, 第一行 θ_ddot 系数],
    #      [第二行 x_ddot 系数, 第二行 θ_ddot 系数]]
    A = np.array([
        [(M+m), m*l*cos_theta],
        [m*l*cos_theta, (I+m*l**2)]
    ])

    # 【TODO 3】构造 b_vec（两个方程的右边）
    # 方程①右边 = F + m·l·sinθ·θ_dot²
    # 方程②右边 = m·g·l·sinθ
    b_vec = np.array([
        F + m*l*sin_theta*theta_dot**2,
        m*g*l*sin_theta
    ])

    # 【TODO 4】联立求解两个加速度
    x_ddot, theta_ddot = np.linalg.solve(A, b_vec)

    # 【TODO 5~8】欧拉积分更新 4 个状态（新值 = 旧值 + 变化率 × dt）
    x_dot = x_dot + x_ddot * dt
    x = x + x_dot * dt
    theta_dot =  theta_dot + theta_ddot * dt
    theta =  theta + theta_dot * dt

    # 记录数据（不用改）
    time_list.append(t)
    x_list.append(x)
    theta_list.append(theta)
    t += dt

# ---------- 5. 画图（两个子图：角度 + 小车位置） ----------
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))

ax1.plot(time_list, theta_list, color='crimson')
ax1.axhline(y=0, color='k', linewidth=0.5, linestyle='--')
ax1.set_ylabel('摆杆角度 θ (弧度)')
ax1.set_title('摆杆角度：应收敛到 0（摆杆立住）')
ax1.grid(True, alpha=0.3)

ax2.plot(time_list, x_list, color='steelblue')
ax2.axhline(y=0, color='k', linewidth=0.5, linestyle='--')
ax2.set_xlabel('时间 (s)')
ax2.set_ylabel('小车位置 x (m)')
ax2.set_title('小车位置：注意它会"跑偏"——PD 没管小车')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
