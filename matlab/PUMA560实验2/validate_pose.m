function [pos_err, rot_err] = validate_pose(T_target, T_verify)
%validate_pose 末端位姿闭环校验：位置误差(mm)与姿态误差(deg)
%   输入：
%       T_target —— 目标位姿（4x4 齐次矩阵）
%       T_verify —— 待校验位姿（4x4 齐次矩阵）
%   输出：
%       pos_err  —— 位置误差（单位 mm，欧氏距离）
%       rot_err  —— 姿态误差（单位 deg，旋转矩阵间的等效转角）
%
%   判据：两者都小于容差（如 1e-6）即认为位姿一致。

p1 = T_target(1:3, 4);
p2 = T_verify(1:3, 4);
pos_err = norm(p1 - p2);

R1 = T_target(1:3, 1:3);
R2 = T_verify(1:3, 1:3);
R_delta = R1' * R2;                 % 姿态偏差旋转矩阵
c = (trace(R_delta) - 1) / 2;
c = max(-1, min(1, c));             % 防止浮点越界
rot_err = rad2deg(acos(c));
end
