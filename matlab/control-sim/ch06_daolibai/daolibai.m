M = 1; m = 0.1; L = 1; g = 9.8;
A = [0 1 0 0;
     0 0 -m*g/M 0;
     0 0 0 1;
     0 0 (M+m)*g/(M*L) 0];
B = [0; 1/M; 0; -1/(M*L)];
Q(3,3) = 100000;
R = 1;
K = lqr(A, B, Q, R);
Acl = A - B*K;

X0 = [0; 0; deg2rad(5); 0];
tspan = [0, 10];
[t, X] = ode45(@(t,X) Acl*X, [0 5], X0);

plot(t, rad2deg(X(:,3)), 'b-', 'LineWidth', 1.5);
xlabel('时间 t (s)'); ylabel('摆角 \theta (度)');
title('倒立摆 LQR 控制'); grid on;
% plot(t, X(:,1))

