%% main_PUMA560.m —— PUMA560 机械臂正/逆运动学实验主脚本
% 《机器人建模与仿真实验A》实验2：机械臂运动学建模与仿真
%
% 运行前把本目录（含 MDH_Transform.m / PUMA560_FK.m / PUMA560_IK.m /
% validate_pose.m）加入 MATLAB 路径，或直接在本目录运行。
%
% 流程：建参数表 → 正运动学 → 逆运动学 → 8 组解闭环校验 → 结果汇总。
clc; clear; close all;

TOL_POS = 1e-6;   % 位置误差容差（mm）
TOL_ROT = 1e-6;   % 姿态误差容差（deg）

%% 1. 修正 D-H 参数表
fprintf('========== 1. 修正 D-H 参数表 ==========\n');
fprintf('  i   α_i(deg)   a_i(mm)   d_i(mm)   θ_i\n');
fprintf('  1       0         0         0      θ1\n');
fprintf('  2     -90         0       145      θ2\n');
fprintf('  3       0       425         0      θ3\n');
fprintf('  4     -90        15       428      θ4\n');
fprintf('  5      90         0         0      θ5\n');
fprintf('  6     -90         0         0      θ6\n');

%% 2. 正运动学：设定当前关节角 → 求末端位姿
fprintf('\n========== 2. 正运动学 ==========\n');
theta_true_deg = [30, -45, 60, 20, 30, 40];   % 当前关节角（deg）
theta_true     = deg2rad(theta_true_deg);      % 转为 rad

[T, A] = PUMA560_FK(theta_true);               % A{i} 为第 i 个相邻变换

fprintf('当前关节角 θ(deg) = [%g %g %g %g %g %g]\n', theta_true_deg);
fprintf('末端位姿矩阵 T06 =\n');
disp(T);
fprintf('末端位置 p(mm) = [%.3f, %.3f, %.3f]\n', T(1,4), T(2,4), T(3,4));
fprintf('末端姿态 R =\n'); disp(T(1:3,1:3));
fprintf('（中间变换矩阵 T01 示例见 A{1}，其余在 A{2}~A{6}）\n');

%% 3. 逆运动学：由末端位姿反解关节角
fprintf('\n========== 3. 逆运动学反解 ==========\n');
sols = PUMA560_IK(T);
n = size(sols, 1);
fprintf('共求得 %d 组逆解（角度已归一化到 [-180°, 180°]）：\n', n);

%% 4. 闭环校验：8 组解回代正运动学，与目标位姿比较
fprintf('\n========== 4. 闭环校验（位置 mm / 姿态 deg） ==========\n');
fprintf('容差：位置 %.0e mm，姿态 %.0e deg\n\n', TOL_POS, TOL_ROT);

n_pass = 0;
for k = 1:n
    Tk = PUMA560_FK(sols(k, :));
    [pos_err, rot_err] = validate_pose(T, Tk);
    pass = (pos_err < TOL_POS) && (rot_err < TOL_ROT);
    if pass
        n_pass = n_pass + 1;
        tag = '通过';
    else
        tag = '不通过';
    end
    q_deg = wrapTo180(rad2deg(sols(k, :)));   % 归一化显示
    fprintf('解 %d [%s]: θ(deg) = [%7.2f %7.2f %7.2f %7.2f %7.2f %7.2f]  位置误差=%.2e mm  姿态误差=%.2e deg\n', ...
        k, tag, q_deg, pos_err, rot_err);
    if max(abs(q_deg - theta_true_deg)) < 1e-4
        fprintf('        ^-- 与原"当前"关节角一致（逆解正确性的直接验证）\n');
    end
end

%% 5. 结果汇总
fprintf('\n========== 5. 汇总 ==========\n');
fprintf('逆解共 %d 组，其中 %d 组通过闭环校验（位姿恢复到目标）。\n', n, n_pass);
if n_pass == n
    fprintf('结论：全部解有效，正/逆运动学一致，误差均在容差以内。\n');
else
    fprintf('警告：存在未通过校验的解，请检查实现。\n');
end
