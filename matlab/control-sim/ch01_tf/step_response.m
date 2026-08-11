% step_response.m
% 二阶系统阶跃响应
% 张宇诚 · 2026-08-12 · daily-code/matlab/control-sim/ch01_tf/

clear; clc; close all;

%% 二阶系统定义
% 传递函数: G(s) = ωn² / (s² + 2ζωn·s + ωn²)

omega_n = 2;        % 自然频率 (rad/s)
zeta = 0.3;         % 阻尼比 (0~1 欠阻尼, 1 临界阻尼, >1 过阻尼)

num = omega_n^2;                % 分子: ωn²
den = [1, 2*zeta*omega_n, omega_n^2];  % 分母: s² + 2ζωn·s + ωn²

sys = tf(num, den)

%% 阶跃响应
figure;
step(sys);
title(sprintf('二阶系统阶跃响应 (\\zeta = %.1f, \\omega_n = %.1f)', zeta, omega_n));
grid on;

%% 不同阻尼比对比
zeta_values = [0.1, 0.3, 0.7, 1.0, 1.5];
figure;
hold on;
for i = 1:length(zeta_values)
    z = zeta_values(i);
    den = [1, 2*z*omega_n, omega_n^2];
    sys = tf(omega_n^2, den);
    step(sys);
end
hold off;
legend(arrayfun(@(z) sprintf('\\zeta = %.1f', z), zeta_values, 'UniformOutput', false));
title(sprintf('不同阻尼比下的阶跃响应 (\\omega_n = %.1f)', omega_n));
grid on;
