g = 9.8; L = 1;         
 A = [0,1; -(g/L),0] ;
 x0 = [deg2rad(30); 0] ; 

 x_elevator = expm(A*1) * x0


 pendulum_ode = @(t, z) [z(2); -(g/L)*z(1)];
 [t, z] = ode45(pendulum_ode, [0 1], x0);
 x_stairs = z(end,:)'
