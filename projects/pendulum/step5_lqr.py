# -*- coding: utf-8 -*-
"""
台阶 5：小车 + 倒立摆 + LQR 最优控制
=====================================
目标：用 LQR(线性二次型调节器)一次性反馈全部 4 个状态，
     把摆杆和小车【同时】稳住、拉回原点——彻底解决台阶 4"小车跑偏"的问题。

【回忆台阶 4 的局限】
    PD 控制只反馈了摆杆角度 θ，没管小车位置 x，所以摆杆立住了、小车却滑走了。
    LQR 会反馈 [x, x_dot, θ, θ_dot] 全部 4 个状态，把小车也拉回原点。

【LQR 的核心思想（三步）】
    1. 把系统在平衡点(θ=0)附近线性化，写成状态空间形式：
           dx/dt = A·x + B·u
       （x 是 4 维状态向量，u 是控制力 F）
    2. 定义代价函数 J = ∫(xᵀQx + uᵀRu)dt：
           Q 惩罚"状态偏离目标"（摆杆歪、小车跑），R 惩罚"用力太大"。
    3. 解一个 Riccati 方程，得到最优反馈增益 K，控制律就是：
           u = -K · x
       这就是 LQR 的最终结果——一个"算得最优"的全状态 PD。

【你需要完成 9 个填空】
    TODO 1：线性化 A 矩阵(4×4)
    TODO 2：线性化 B 矩阵(4×1)
    TODO 3：解 Riccati 方程得到 P
    TODO 4：计算最优增益 K
    TODO 5：控制力 u = -K·x（全状态反馈）
    TODO 6~9：欧拉积分更新 4 个状态

【填完后的预期】
    上图 θ：从 10° 收敛到 0（摆杆立住）。
    下图 x：先跑出去一点，然后被拉回原点(x→0)——小车不再滑走！

【提示：线性化结果（已在 θ=0 附近把 sinθ≈θ、cosθ≈1 代入）】
    记 den = (M+m)·I + M·m·l²，则：
    A = [[0, 1, 0, 0],
         [0, 0, -(m²·g·l²)/den, 0],
         [0, 0, 0, 1],
         [0, 0, (M+m)·m·g·l/den, 0]]
    B = [[0], [(I+m·l²)/den], [0], [-m·l/den]]
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import solve_continuous_are

# ---------- 1. 物理参数 ----------
M = 1.0
m = 0.2
l = 0.3
I = (1/3) * m * l**2
g = 9.81

# ---------- 2. 线性化：计算 A、B 矩阵 ----------
den = (M + m) * I + M * m * l**2

# 【TODO 1】构造 A 矩阵(4×4)，按上面的公式填
A = np.array([
    [0, 1, 0, 0],
    [0, 0, -(m**2*g*l**2)/den, 0],
    [0, 0, 0, 1],
    [0, 0, (M+m)*m*g*l/den, 0]
])

# 【TODO 2】构造 B 矩阵(4×1)
B = np.array([
    [0],
    [(I+m*l**2)/den],
    [0],
    [-m*l/den]
])

# ---------- 3. LQR 权重 ----------
# Q：惩罚状态偏离。数字越大 = 越在乎那个状态。
#    顺序 [x, x_dot, theta, theta_dot]：最在乎摆杆角度(100)，其次小车位置(10)。
Q = np.diag([10.0, 1.0, 100.0, 1.0])
R = np.array([[1.0]])   # 惩罚控制力：越大越"省力"

# ---------- 4. 解 Riccati 方程 + 计算增益 K ----------
# 【TODO 3】解连续时间代数 Riccati 方程，得到 P
# 提示：用 solve_continuous_are(A, B, Q, R)，它返回的就是 P
P = solve_continuous_are(A, B, Q, R)

# 【TODO 4】计算最优反馈增益 K
# 公式：K = R⁻¹ · Bᵀ · P
K = np.linalg.inv(R) @ B.T @ P

print("最优反馈增益 K =", K.round(3))

# ---------- 5. 模拟参数与初始状态 ----------
dt = 0.001
t_end = 6.0
x = 0.0
x_dot = 0.0
theta = np.radians(10)
theta_dot = 0.0

time_list, x_list, theta_list = [], [], []

t = 0.0
while t < t_end:
    # 组装状态向量(4×1)
    state = np.array([[x], [x_dot], [theta], [theta_dot]])

    # 【TODO 5】LQR 控制力：u = -K · x（全状态反馈）
    u = -K @ state

    # ---- 非线性动力学（和台阶 4 一样，用真实非线性方程更新）----
    s, c = np.sin(theta), np.cos(theta)
    A_mat = np.array([[M + m, m * l * c],
                      [m * l * c, I + m * l**2]])
    b_vec = np.array([u[0, 0] + m * l * s * theta_dot**2,
                      m * g * l * s])
    x_ddot, theta_ddot = np.linalg.solve(A_mat, b_vec)

    # 【TODO 6~9】欧拉积分更新 4 个状态
    x_dot = x_dot + x_ddot * dt
    x = x + x_dot * dt
    theta_dot = theta_dot + theta_ddot * dt
    theta = theta + theta_dot * dt

    time_list.append(t)
    x_list.append(x)
    theta_list.append(theta)
    t += dt

# ---------- 6. 画图 ----------
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))

ax1.plot(time_list, theta_list, color='crimson')
ax1.axhline(y=0, color='k', linewidth=0.5, linestyle='--')
ax1.set_ylabel('摆杆角度 θ (弧度)')
ax1.set_title('LQR：摆杆角度应收敛到 0')
ax1.grid(True, alpha=0.3)

ax2.plot(time_list, x_list, color='steelblue')
ax2.axhline(y=0, color='k', linewidth=0.5, linestyle='--')
ax2.set_xlabel('时间 (s)')
ax2.set_ylabel('小车位置 x (m)')
ax2.set_title('LQR：小车应先跑出去、再被拉回原点')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
