%% ==========第7题 三维绘图（严格按题目重写）==========
close all;clear;clc;

%(1) 螺旋线：x∈[0,3π]，y=cos(2x)，z=sin(2x)
% "点连接圆圈"：标记o，实线相连
x = linspace(0,3*pi,300);
y = cos(2*x);
z = sin(2*x);

figure;
plot3(x,y,z,'o-');
xlabel('x');
ylabel('cos(2x)');
zlabel('sin(2x)');
title('绘制螺旋线');
grid on;   %开启坐标栅格

%(2) 第二问三维参数曲线
% x(t)=(5+cos(sqrt(15)*t))*cos(t)
% y(t)=sin(sqrt(15)*t)
% z(t)=(5+cos(sqrt(15)*t))*sin(t)
% 注意：数组运算 .*
t = linspace(0, 8*pi, 3000);
sqrt15 = sqrt(15);
xt = (5 + cos(sqrt15 .* t)) .* cos(t);
yt = sin(sqrt15 .* t);
zt = (5 + cos(sqrt15 .* t)) .* sin(t);

figure;
plot3(xt,yt,zt);
axis equal;   %每个坐标轴的数据单元都相同！题目硬性要求
xlabel('x(t)');
ylabel('y(t)');
zlabel('z(t)');
grid on;
title('三维参数曲线');