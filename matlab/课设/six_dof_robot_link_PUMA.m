%% ========== 六自由度机械臂动力学建模与力矩求解 ==========
clear; clc; close all;

%% ---------- 步骤1：建立机器人模型（改进DH参数） ----------
% 连杆参数: [theta, d, a, alpha, offset]
L(1) = Link('d', 0.670, 'a', 0,     'alpha', -pi/2, 'modified');
L(2) = Link('d', 0,     'a', 0.431, 'alpha', 0,     'modified');
L(3) = Link('d', 0.150, 'a', 0.020, 'alpha', pi/2,  'modified');
L(4) = Link('d', 0.432, 'a', 0,     'alpha', -pi/2, 'modified');
L(5) = Link('d', 0,     'a', 0,     'alpha', pi/2,  'modified');
L(6) = Link('d', 0.056, 'a', 0,     'alpha', 0,     'modified');

robot = SerialLink(L, 'name', 'SixDOF_Arm');

% ---------- 设置各连杆动力学参数 ----------
% 连杆1
L(1).m = 3.70;
L(1).r = [0, 0.02561, 0.00193];
L(1).I = diag([0.0108, 0.0108, 0.00463]);
L(1).Jm = 0.004898;   % 电机惯量
L(1).B  = 0.00148;    % 粘性摩擦
L(1).Tc = [0.005, -0.005]; % 库仑摩擦

% 连杆2
L(2).m = 9.00;
L(2).r = [0, 0.1119, 0];
L(2).I = diag([0.2264, 0.2264, 0.0151]);
L(2).Jm = 0.00352;
L(2).B  = 0.00148;
L(2).Tc = [0.005, -0.005];

% 连杆3
L(3).m = 2.275;
L(3).r = [0, 0, 0.01634];
L(3).I = diag([0.0485, 0.0485, 0.0028]);
L(3).Jm = 0.001518;
L(3).B  = 0.00148;
L(3).Tc = [0.005, -0.005];

% 连杆4
L(4).m = 1.61;
L(4).r = [0, 0, 0.001159];
L(4).I = diag([0.0034, 0.0034, 0.009]);
L(4).Jm = 0.0008;
L(4).B  = 0.001;
L(4).Tc = [0.003, -0.003];

% 连杆5
L(5).m = 0.50;
L(5).r = [0, 0, 0.008];
L(5).I = diag([0.0008, 0.0008, 0.0005]);
L(5).Jm = 0.0003;
L(5).B  = 0.0005;
L(5).Tc = [0.002, -0.002];

% 连杆6
L(6).m = 0.30;
L(6).r = [0, 0, 0.005];
L(6).I = diag([0.0003, 0.0003, 0.0002]);
L(6).Jm = 0.0002;
L(6).B  = 0.0003;
L(6).Tc = [0.001, -0.001];

% 设置重力方向
robot.gravity = [0, 0, -9.81];

fprintf('机器人模型建立完成\n');
robot.display();

%% ---------- 步骤2：定义初始位置和目标位置 ----------
% 初始关节角度（零位附近）
q_start = [0, 0, 0, 0, 0, 0];

% 目标关节角度（通过逆运动学求解得到）
% 目标末端位置: [0.5, 0.3, 0.4]，姿态: RPY = [pi/3, pi/4, pi/5]
T_target = transl(0.5, 0.3, 0.4) * trotz(pi/3) * troty(pi/4) * trotx(pi/5);
% q_target = robot.ikine(T_target, 'q0', q_start, 'ilimit', 50);
% q_target = robot.ikine6s(T_target);

q_target = [pi/6, pi/4, -pi/3, pi/6, pi/4, pi/3];

fprintf('初始关节角度: [%s]\n', num2str(q_start, '%.3f '));
fprintf('目标关节角度: [%s]\n', num2str(q_target, '%.3f '));

%% ---------- 步骤3：五次多项式轨迹规划 ----------
N = 100;              % 轨迹点数
T_total = 2.0;        % 运动总时间 (秒)
t = linspace(0, T_total, N);

% 使用jtraj生成五次多项式轨迹
% q: 关节角度, qd: 关节角速度, qdd: 关节角加速度
size(q_start)
size(q_target)
[q, qd, qdd] = jtraj(q_start, q_target, N);

fprintf('轨迹规划完成，共 %d 个轨迹点，总时长 %.1f 秒\n', N, T_total);

%% ---------- 步骤4：逆动力学求解各关节力矩 ----------
% 方法A：使用rne函数（Recursive Newton-Euler）
tau = zeros(N, 6);
for i = 1:N
    tau(i, :) = robot.rne(q(i,:), qd(i,:), qdd(i,:));
end

% 方法B：使用inverseDynamics（等价实现）
% tau2 = zeros(N, 6);
% for i = 1:N
%     tau2(i,:) = inverseDynamics(robot, q(i,:), qd(i,:), qdd(i,:));
% end

fprintf('逆动力学求解完成\n');

%% ---------- 步骤5：结果可视化 ----------
figure('Position', [100, 100, 1200, 800]);

% 绘制各关节力矩随时间变化曲线
joint_names = {'关节1', '关节2', '关节3', '关节4', '关节5', '关节6'};
colors = lines(6);

for j = 1:6
    subplot(2, 3, j);
    plot(t, tau(:, j), 'Color', colors(j,:), 'LineWidth', 1.5);
    xlabel('时间 (s)');
    ylabel('力矩 (N·m)');
    title([joint_names{j} ' 驱动力矩']);
    grid on;
end
sgtitle('六自由度机械臂各关节驱动力矩随时间变化');

% 绘制关节角度轨迹
figure('Position', [100, 100, 1200, 400]);
for j = 1:6
    subplot(1, 6, j);
    plot(t, q(:, j), 'Color', colors(j,:), 'LineWidth', 1.5);
    xlabel('时间 (s)');
    ylabel('角度 (rad)');
    title(joint_names{j});
    grid on;
end
sgtitle('各关节角度轨迹');

%% ---------- 步骤6：输出关键结果 ----------
fprintf('\n===== 逆动力学求解结果 =====\n');
fprintf('%-8s %12s %12s %12s %12s\n', '关节', '最大力矩', '最小力矩', '平均力矩', '单位');
for j = 1:6
    fprintf('%-8s %12.4f %12.4f %12.4f %12s\n', ...
        joint_names{j}, max(tau(:,j)), min(tau(:,j)), mean(tau(:,j)), 'N·m');
end

%% ---------- 步骤7：机械臂运动动画（可选） ----------
% figure('Name', '机械臂运动动画');
% robot.plot(q, 'fps', 30, 'trail', 'r-');
% title('六自由度机械臂运动轨迹动画');
%% ---------- 步骤7：机械臂运动动画 ----------
figure('Name', '机械臂运动动画', 'NumberTitle', 'off');
robot.plot(q, 'fps', 30, 'trail', 'r-', 'workspace', [-1 1 -1 1 -0.5 1.5]);
title('六自由度机械臂运动轨迹动画');