# -*- coding: utf-8 -*-
"""
台阶 3：倒立摆 + PD 控制(比例-微分)
=====================================
目标：在 P 控制的基础上加入 D(微分)项，让摆杆不仅能立住，还能"稳住不晃"。

【回忆台阶 2 的问题】
    台阶 2 只有 P 控制，摆杆虽然不倒，但会一直来回振荡。
    原因：P 控制只根据"歪了多少"用力，没有"刹车"，摆杆回正后会冲过头。

【D 项(微分)的作用：给系统"加阻尼/刹车"】
    P 项：看"歪了多少"（角度 θ），歪得多 → 用力多。
    D 项：看"歪得多快"（角速度 θ_dot），倒得快 → 加反向力矩"刹车"。

    PD 控制律：  τ = -Kp · θ - Kd · θ_dot

【你需要完成 4 个填空(这次公式要你自己想，不直接给了)】
    TODO 1：写出 PD 控制力矩（把 P 项和 D 项合起来）
    TODO 2：写出角加速度（重力项 + 力矩项，结构同台阶 2）
    TODO 3：欧拉积分更新角速度
    TODO 4：欧拉积分更新角度

【填完后的预期】
    摆杆从 15° 被扶正，振荡越来越小，最终稳稳立在竖直向上(θ → 0)。
    对比台阶 2 的"一直晃"，这就是 D 项的功劳。

【试玩】
    把 Kd 改成 0，会退化成台阶 2(一直晃)；
    把 Kd 调很大，会"刹车过头"变慢——体会"阻尼"的手感。
"""

import numpy as np
import matplotlib.pyplot as plt

g = 9.81      # 重力加速度
L = 1.0       # 摆长
m = 0.5       # 摆杆质量
I = m * L**2  # 转动惯量

# 控制增益：Kp 负责"扶正"，Kd 负责"阻尼"
Kp = 20.0
Kd = 30.0      # 微分增益(阻尼)——自己调调看

dt = 0.001
t_end = 5.0

theta = np.radians(15)   # 初始角度 15°
theta_dot = 0.0          # 初始角速度 0

time_list = []
theta_list = []

t = 0.0
while t < t_end:
    # 【TODO 1】PD 控制力矩
    # 提示：
    #   P 项你已经会了：-Kp * theta（扶正）
    #   D 项是新的：和"角速度 theta_dot 成正比、方向相反"的阻尼
    # 把 P 项和 D 项加起来，写出完整的 tau：
    tau = -Kp * theta + theta_dot * (-Kd)

    # 【TODO 2】角加速度（结构同台阶 2，自己写对）
    # 重力项(想让摆倒) + 力矩项(想扶正)
    theta_ddot = (g / L) * np.sin(theta) + tau / I

    # 【TODO 3】更新角速度
    theta_dot = theta_ddot * dt + theta_dot

    # 【TODO 4】更新角度
    theta = theta + theta_dot *dt

    time_list.append(t)
    theta_list.append(theta)
    t += dt

plt.plot(time_list, theta_list)
plt.xlabel('时间 (s)')
plt.ylabel('角度 (弧度)')
plt.title('倒立摆 PD 控制：角度随时间变化(应收敛到 0)')
plt.grid(True)
plt.show()
