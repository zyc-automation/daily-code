function T = MDH_Transform(a, alpha, d, theta)
%MDH_Transform 修正D-H（改进D-H）变换矩阵
%   T = Rx(alpha) * Dx(a) * Rz(theta) * Dz(d)
%
%   输入：
%       a      —— 连杆长度 a_i（沿 x_i 轴，单位 mm）
%       alpha  —— 连杆扭角 alpha_i（绕 x_i 轴，单位 rad）
%       d      —— 关节偏置 d_i（沿 z_i 轴，单位 mm）
%       theta  —— 关节转角 theta_i（绕 z_i 轴，单位 rad）
%   输出：
%       T      —— 4x4 齐次变换矩阵
%
%   展开式：
%       [  cos(theta)              -sin(theta)            0        a         ]
%       [  sin(theta)*cos(alpha)   cos(theta)*cos(alpha)  -sin(alpha) -sin(alpha)*d ]
%       [  sin(theta)*sin(alpha)   cos(theta)*sin(alpha)   cos(alpha)  cos(alpha)*d ]
%       [  0                       0                       0        1         ]

T = [cos(theta),               -sin(theta),             0,            a;
     sin(theta)*cos(alpha),     cos(theta)*cos(alpha),  -sin(alpha),  -sin(alpha)*d;
     sin(theta)*sin(alpha),     cos(theta)*sin(alpha),   cos(alpha),   cos(alpha)*d;
     0,                         0,                      0,            1];
end
