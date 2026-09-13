M = 1; m = 0.1; L = 1; g = 9.8;
A = [0 1 0 0;
     0 0 -m*g/M 0;
     0 0 0 1;
     0 0 (M+m)*g/(M*L) 0];
B = [0; 1/M; 0; -1/(M*L)];
Q = diag([100, 1, 100, 0.1]);
R = 1;
K = lqr(A, B, Q, R)
Acl = A - B*K;

X0 = [0; 0; deg2rad(20); 0];
tspan = [0, 10];
[t, X] = ode45(@(t,X) Acl*X, [0 10], X0);

% plot(t, rad2deg(X(:,3)), 'b-', 'LineWidth', 1.5);
% xlabel('时间 t (s)'); ylabel('摆角 \theta (度)');
% title('倒立摆开环（无控制）'); grid on;

figure;
for i = 1:5:length(t)% 每5帧取1帧（降采样，动画更流畅）
    x_cart = X(i, 1);% 这一帧：小车位置
    theta  = X(i, 3);% 这一帧：摆角
    cla; hold on;% 擦掉上一帧
    % 画小车（一个蓝色矩形）
    rectangle('Position', [x_cart-0.15, -0.05, 0.3, 0.1], 'FaceColor', 'b');
    % 画摆杆（一条线段：支点 → 摆杆顶端）
    px = x_cart + L*sin(theta);% 顶端横坐标
    py = L*cos(theta);% 顶端纵坐标
    plot([x_cart, px], [0, py], 'r-', 'LineWidth', 3);

    % 固定画面范围，防止镜头乱跳
    xlim([-1.5, 1.5]); ylim([-0.3, 1.5]); axis equal;

    title(sprintf('倒立摆  t = %.2f s', t(i)));
    drawnow;% 刷新这一帧（关键！）
    pause(0.05);% 停 0.01 秒（控制速度）  
end