A = rand(4,4)
B = rand(4,4)
A_plus_B = A + B
A_minus_B = A - B
A_mul_B = A * B
A_leftdiv_B = A\B    %A左除B
B_rightdiv_A = B/A   %B右除A

%a)首项0，公差0.5，末项10
v1 = 0:0.5:10
%b)首项1，公差1，末项19
v2 = 1:1:19

%a) [8,20]均匀分布1×20向量
vec_uniform = 8 + (20-8)*rand(1,20)
%b) [-10,10]高斯分布4×4矩阵
vec_gauss = 10 * randn(4,4)

%a 创建5×8矩阵A
A = rand(5,8)
%b 第2行第7列元素
ele = A(2,7)
%c 第1列所有元素
col1 = A(:,1)
%d 第3行所有元素
row3 = A(3,:)
%e 2‑4行，4‑7列子矩阵
subA = A(2:4,4:7)

%自定义4×4矩阵
A = [1 2 3 4;
     5 6 7 8;
     9 10 11 12;
     13 14 15 16];

%a 行列式，特征值特征向量，秩
det_A = det(A)
[V,D] = eig(A)
rank_A = rank(A)

%b LU三角分解、奇异值分解
[L,U] = lu(A)
[U_svd,S_svd,V_svd] = svd(A)

%c 各列最大最小、均值、标准差、方差
max_col = max(A)
min_col = min(A)
mean_col = mean(A)
std_col = std(A)
var_col = var(A)


clear;clc;
x = 0:0.1:2*pi;
figure;
%1行3列第1个子图
subplot(1,3,1);
y1 = sin(x);
plot(x,y1,'-','LineWidth',3);
xlabel('x');ylabel('y');
title('y=sin(x)');

%第2个子图
subplot(1,3,2);
y_sin = sin(x);
y_cos = cos(x);
plot(x,y_sin,'--','LineWidth',5);hold on;
plot(x,y_cos,'-.','LineWidth',5);
xlabel('x');ylabel('y');
title('sin与cos曲线');
legend('sin(x)','cos(x)');
hold off;

%第3个子图，分段函数
subplot(1,3,3);
xx = -2:0.1:3;
yy = zeros(size(xx));
for i = 1:length(xx)
    if xx(i)<1
        yy(i)=xx(i);
    else
        yy(i)=xx(i)^2;
    end
end
plot(xx,yy);
xlabel('x');ylabel('y');
title('分段函数曲线');


clear;clc;
t = 0:0.1:10*pi;
x = cos(t);
y = sin(t);
z = t;
plot3(x,y,z,'-o');
xlabel('x');ylabel('y');zlabel('z');
grid on;
title('绘制螺旋线');
axis equal;


[X,Y] = meshgrid(-3:0.2:3,-3:0.2:3);
Z = X.^2 + Y.^2;
figure;
surf(X,Y,Z);
xlabel('x');ylabel('y');zlabel('z');
axis equal;
grid on;
title('三维曲面图像');



scores = [78, 92, 48, 69, 88, 59, 100, 77, 81, 95, 52, 66];
n_excellent = 0;
n_good = 0;
n_medium = 0;
n_pass = 0;
n_fail = 0;
fail_index = [];
fail_score = [];
sum_score = 0;

for i = 1:length(scores)
    s = scores(i);
    sum_score = sum_score + s;
    if s>=90 && s<=100
        n_excellent = n_excellent +1;
    elseif s>=80 && s<=89
        n_good = n_good +1;
    elseif s>=70 && s<=79
        n_medium = n_medium +1;
    elseif s>=60 && s<=69
        n_pass = n_pass +1;
    else
        n_fail = n_fail +1;
        fail_index = [fail_index,i];
        fail_score = [fail_score,s];
    end
end

avg_score = sum_score / length(scores);

fprintf('优秀人数：%d\n',n_excellent);
fprintf('良好人数：%d\n',n_good);
fprintf('中等人数：%d\n',n_medium);
fprintf('及格人数：%d\n',n_pass);
fprintf('不及格人数：%d\n',n_fail);
fprintf('平均分=%.2f\n',avg_score);

if n_fail>0
    fprintf('不及格索引：%s\n',num2str(fail_index));
    fprintf('不及格分数：%s\n',num2str(fail_score));
else
    disp('全部及格');
end


