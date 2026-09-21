function sols = PUMA560_IK(T)
%PUMA560_IK PUMA560 机械臂逆运动学（解析解，代数法）
%   输入：
%       T    —— 4x4 末端位姿矩阵（相对基坐标系 {0}）
%   输出：
%       sols —— Nx6 矩阵，每行一组关节角 [θ1..θ6]（rad），N ≤ 8；无解返回空矩阵
%
%   求解顺序：θ1 → θ3 → θ2 → θ5 → θ4 → θ6
%   每个正负号选择对应不同构型（肩部左/右、肘部上/下、腕部翻转），最多 8 组解。
%
%   说明：本函数为非奇异位形（θ5 ≠ 0）的完整解析解；腕部奇异位形（θ5 ≈ 0）
%   下 θ4、θ6 退化为同一自由度，本函数跳过该分支（如需处理可另加数值法）。

d2 = 145; d4 = 428; a2 = 425; a3 = 15;
alpha = [0, -pi/2, 0, -pi/2, pi/2, -pi/2];   % α_i
a     = [0, 0, a2, a3, 0, 0];                % a_i
d     = [0, d2, 0, d4, 0, 0];                % d_i

R  = T(1:3, 1:3);
px = T(1, 4); py = T(2, 4); pz = T(3, 4);

sols = [];   % 动态收集解

% ===== 第1步：求 θ1 =====
% 由方程 -px·sinθ1 + py·cosθ1 = d2 得到
r = sqrt(px^2 + py^2);
if r < 1e-10
    return;
end
phi = atan2(py, px);
for sgn1 = [1, -1]
    if abs(d2 / r) > 1
        continue;
    end
    theta1 = phi - atan2(d2, sgn1 * sqrt(r^2 - d2^2));
    s1 = sin(theta1); c1 = cos(theta1);
    K = px*c1 + py*s1;                    % = X·cosθ2 - Y·sinθ2

    % ===== 第2步：求 θ3 =====
    % 由 (px·c1+py·s1)^2 + pz^2 = X^2 + Y^2 消去 θ2
    num = (K^2 + pz^2 - a2^2 - a3^2 - d4^2) / (2*a2);
    den = sqrt(a3^2 + d4^2);
    ratio = num / den;
    if ratio > 1, ratio = 1; end
    if ratio < -1, ratio = -1; end
    for sgn3 = [1, -1]
        theta3 = sgn3*acos(ratio) - atan2(d4, a3);
        X = a2 + a3*cos(theta3) - d4*sin(theta3);
        Y = a3*sin(theta3) + d4*cos(theta3);

        % ===== 第3步：求 θ2 =====
        theta2 = atan2(-X*pz - K*Y, K*X - Y*pz);

        % ===== 第4步：求 R03，解出腕部 R36 =====
        R03 = eye(3);
        th13 = [theta1, theta2, theta3];
        for i = 1:3
            Ti = MDH_Transform(a(i), alpha(i), d(i), th13(i));
            R03 = R03 * Ti(1:3, 1:3);
        end
        R36 = R03' * R;

        r13 = R36(1,3); r23 = R36(2,3); r33 = R36(3,3);
        r21 = R36(2,1); r22 = R36(2,2);

        % ===== 第5步：求 θ5 =====
        s5 = sqrt(r13^2 + r33^2);
        if s5 < 1e-10
            continue;    % 腕部奇异位形（θ5≈0），此处略去
        end
        theta5 = atan2(s5, r23);
        for sgn5 = [1, -1]
            t5 = theta5;
            if sgn5 < 0
                t5 = -theta5;
            end
            % ===== 第6步：求 θ4、θ6 =====
            theta4 = atan2( sgn5*r33, -sgn5*r13);
            theta6 = atan2(-sgn5*r22,  sgn5*r21);
            sols = [sols; theta1, theta2, theta3, theta4, t5, theta6]; %#ok<AGROW>
        end
    end
end
end
