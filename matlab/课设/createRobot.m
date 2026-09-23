function robot = createRobot()
% 创建六自由度机械臂 Robotics Toolbox 模型
    L(1) = Link('d', 0.670, 'a', 0,     'alpha', -pi/2, 'modified');
    L(2) = Link('d', 0,     'a', 0.431, 'alpha', 0,     'modified');
    L(3) = Link('d', 0.150, 'a', 0.020, 'alpha', pi/2,  'modified');
    L(4) = Link('d', 0.432, 'a', 0,     'alpha', -pi/2, 'modified');
    L(5) = Link('d', 0,     'a', 0,     'alpha', pi/2,  'modified');
    L(6) = Link('d', 0.056, 'a', 0,     'alpha', 0,     'modified');

    % 连杆动力学参数
    L(1).m = 3.70;  L(1).r = [0, 0.02561, 0.00193];  L(1).I = diag([0.0108, 0.0108, 0.00463]);
    L(2).m = 9.00;  L(2).r = [0, 0.1119,  0];        L(2).I = diag([0.2264, 0.2264, 0.0151]);
    L(3).m = 2.275; L(3).r = [0, 0, 0.01634];        L(3).I = diag([0.0485, 0.0485, 0.0028]);
    L(4).m = 1.61;  L(4).r = [0, 0, 0.001159];       L(4).I = diag([0.0034, 0.0034, 0.009]);
    L(5).m = 0.50;  L(5).r = [0, 0, 0.008];          L(5).I = diag([0.0008, 0.0008, 0.0005]);
    L(6).m = 0.30;  L(6).r = [0, 0, 0.005];          L(6).I = diag([0.0003, 0.0003, 0.0002]);

    robot = SerialLink(L, 'name', 'SixDOF');
    robot.gravity = [0, 0, -9.81];
end