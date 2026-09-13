A = [0 1; 9.8 0];
B = [0; 1];
Q = [1 0; 0 1];
R = 1;
K = lqr(A,B,Q,R);

% Q = [10 0; 0 1];  R = 1;
% K_fast = lqr(A, B, Q, R);
% 
% Q = [1 0; 0 1];  R = 10;
% K_slow = lqr(A, B, Q, R)