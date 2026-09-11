 g = 9.8; L = 1;         
 A = [0,1; -(g/L),0] ;
 x = [deg2rad(30); 0] ;
 a=A*x  ; 
 pendulum_ode = @(t, z) [z(2); -(g/L)*z(1)];
 pendulum_ode(0, x)
