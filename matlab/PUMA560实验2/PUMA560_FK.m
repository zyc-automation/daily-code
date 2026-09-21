function [T, A] = PUMA560_FK(theta)
%PUMA560_FK PUMA560 机械臂正运动学（修正D-H）
%   输入：
%       theta —— 6x1 关节角向量（单位 rad）
%   输出：
%       T     —— 4x4 末端坐标系 {6} 相对基坐标系 {0} 的齐次变换矩阵
%       A     —— (可选) 1x6 cell，A{i} 为第 i 个相邻变换 T(i-1,i)
%
%   修正D-H 参数表（单位 mm；α、a、d、θ 下标统一用 i）：
%     i   α_i(°)   a_i(mm)   d_i(mm)   θ_i
%     1   0        0         0         θ1
%     2   -90      0         145       θ2
%     3   0        425       0         θ3
%     4   -90      15        428       θ4
%     5   90       0         0         θ5
%     6   -90      0         0         θ6

d2 = 145; d4 = 428; a2 = 425; a3 = 15;
alpha = [0, -pi/2, 0, -pi/2, pi/2, -pi/2];   % α_i
a     = [0, 0, a2, a3, 0, 0];                % a_i
d     = [0, d2, 0, d4, 0, 0];                % d_i

if nargout > 1
    A = cell(1, 6);
end

T = eye(4);
for i = 1:6
    Ti = MDH_Transform(a(i), alpha(i), d(i), theta(i));
    if nargout > 1
        A{i} = Ti;
    end
    T = T * Ti;
end
end
