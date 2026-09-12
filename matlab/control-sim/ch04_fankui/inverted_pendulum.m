clear;clc;close all;
g=9.8;
L=1;
Kp=20;Kd=5;

pendulum_ode = @(t, z) [z(2); (g/L)*sin(z(1)) - Kp*z(1) - Kd*z(2)];
theta0=deg2rad(5);
z0=[theta0; 0];
tspan=[0,5];
[t,z]=ode45(pendulum_ode,tspan,z0);
theta=z(:,1);


figure;
plot(t,rad2deg(theta),'b-','LineWidth',1.5);
xlabel('时间t（s）');
ylabel('角度\theta(度)');
title('倒立单摆曲线（PD控制）');
grid on;