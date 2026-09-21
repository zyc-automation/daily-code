% ============================================================
% 实验报告1《机器人建模与仿真实验A》第七题
% MATLAB 三维绘图 plot3 / mesh / surf
% ============================================================
clear; clc; close all;

% ---------- (1) 螺旋线：x ∈ [0, 3π]，y = cos(2x)，z = sin(2x) ----------
figure;
x = 0 : 0.1 : 3*pi;
y = cos(2*x);
z = sin(2*x);
plot3(x, y, z, '-o');      % 圆圈标记数据点，并用线连接
grid on;                   % 开启坐标栅格
xlabel('x');
ylabel('cos(2x)');
zlabel('sin(2x)');
title('绘制螺旋线');

% ---------- (2) 参数曲线（环面螺旋线） ----------
%   x(t) = (5 + cos(15t)) * cos(t)
%   y(t) = sin(15t)
%   z(t) = (5 + cos(15t)) * sin(t)
figure;
t = 0 : 0.01 : 2*pi;
x = (5 + cos(15*t)) .* cos(t);
y = sin(15*t);
z = (5 + cos(15*t)) .* sin(t);
plot3(x, y, z);
axis equal;                % 使每个坐标轴的数据单元相同
grid on;
xlabel('x(t)');
ylabel('y(t)');
zlabel('z(t)');
