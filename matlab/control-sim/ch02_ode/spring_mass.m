% spring_mass.m
% 弹簧振子（无阻尼简谐运动）数值求解
% 核心技巧：把二阶 ODE 化成两个一阶 ODE（状态方程）
%
% 张宇诚 · 2026-09-09 · daily-code/matlab/control-sim/ch02_ode/
% 台阶1 第2课：二阶化一阶 —— 这是后面倒立摆反复复用的地基

clear; clc; close all;

%% 1. 物理模型
% 胡克定律 + 牛顿第二定律:
%   m * x'' = -k * x          (弹簧力 = -刚度 * 位移)
% 移项得:
%   x'' = -(k/m) * x = -omega^2 * x
% 其中 omega = sqrt(k/m) 是角频率 (rad/s)

m = 1;                 % 质量 (kg)
k = 4;                 % 弹簧刚度 (N/m)
omega = sqrt(k/m);     % 角频率 = 2 (rad/s)

%% 2. 关键技巧：二阶 ODE -> 一阶方程组（状态方程）
% 引入状态向量 z = [x; v]，其中 v = x' 是速度
% 则原来的二阶方程 x'' = -omega^2*x 等价于两个一阶方程：
%   z(1)' = x'  = v            = z(2)
%   z(2)' = x'' = -omega^2 * x = -omega^2 * z(1)
%
% 写成匿名函数（注意：ode45 要求返回"列向量"）：

spring_ode = @(t, z) [z(2); -omega^2 * z(1)];

%% 3. 用 ode45 求解
x0 = 1;      % 初始位移 (m)，把弹簧拉长 1 米后松手
v0 = 0;      % 初始速度 (m/s)，从静止释放
z0 = [x0; v0];

tspan = [0, 10];            % 仿真 0~10 秒
[t, z] = ode45(spring_ode, tspan, z0);

x = z(:, 1);   % 第1列 = 位移
v = z(:, 2);   % 第2列 = 速度

%% 4. 解析解对比（验证）
% 无阻尼简谐运动的解析解: x(t) = x0 * cos(omega*t)
% 周期 T = 2*pi/omega = pi ≈ 3.14 秒
x_exact = x0 * cos(omega * t);

error_max = max(abs(x - x_exact));
fprintf('弹簧振子数值解与解析解最大误差 = %.2e m\n', error_max);

%% 5. 画图：位移-时间曲线 + 相位图
figure('Position', [100 100 900 360]);

subplot(1, 2, 1);
plot(t, x, 'b-', 'LineWidth', 1.5); hold on;
plot(t, x_exact, 'r--', 'LineWidth', 1.5);
xlabel('时间 t (s)');
ylabel('位移 x (m)');
legend('ode45 数值解', '解析解 x_0 cos(\omegat)');
title('位移-时间曲线');
grid on;

subplot(1, 2, 2);
plot(x, v, 'k-', 'LineWidth', 1.5);
xlabel('位移 x (m)');
ylabel('速度 v (m/s)');
title('相位图 (x-v 平面，闭合圆 = 无阻尼振荡)');
axis equal;
grid on;
