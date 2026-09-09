% ode1_first_order.m
% 一阶微分方程数值求解入门
% 方程: dy/dt = -y,  初值 y(0) = 1
% 解析解(理论答案): y(t) = e^{-t}
%
% 张宇诚 · 2026-09-09 · daily-code/matlab/control-sim/ch02_ode/
% 台阶1 第1课：认识 ode45 的基本用法

clear; clc; close all;

%% 1. 定义微分方程
% ode45 需要"一阶"方程，形式：dy/dt = f(t, y)
% 匿名函数语法：@(自变量, 因变量) 导数表达式
% 注意：参数顺序固定是 (t, y)，t 在前、y 在后！
dydt = @(t, y) -y;

%% 2. ode45 求解
% ode45 的四个输入：
%   @函数句柄 : 微分方程
%   tspan     : 时间范围 [t_start, t_end]
%   y0        : 初值
% 输出：
%   t : 求解器自己选的采样时间点（不均匀）
%   y : 对应每个 t 的数值解

y0 = 1;              % 初值 y(0) = 1
tspan = [0, 5];      % 从 t=0 到 t=5 秒
[t, y] = ode45(dydt, tspan, y0);

%% 3. 解析解对比（验证数值解对不对）
% 这是关键习惯：数值解一定要用"已知答案"验证一次
y_exact = exp(-t);

error_max = max(abs(y - y_exact));
fprintf('一阶方程数值解与解析解最大误差 = %.2e\n', error_max);

%% 4. 画图
figure;
plot(t, y, 'b-o', 'LineWidth', 1.5); hold on;
plot(t, y_exact, 'r--', 'LineWidth', 1.5);
xlabel('时间 t (s)');
ylabel('y(t)');
legend('ode45 数值解', '解析解 e^{-t}');
title('一阶方程 dy/dt = -y 的求解');
grid on;
