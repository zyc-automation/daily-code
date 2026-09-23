function tau = computeTorque(q, qd, qdd)
% 使用 persistent 缓存机器人对象，避免重复创建
    persistent robot
    if isempty(robot)
        robot = createRobot();
    end
    tau = robot.rne(q, qd, qdd);
end