"""
倒立摆（Inverted Pendulum on a Cart）LQR 控制仿真
======================================================
本代码实现了经典的小车-倒立摆系统的建模、LQR控制器设计与仿真动画。

🎯 学习目标：
    - 理解倒立摆的物理模型和动力学方程
    - 掌握 LQR（线性二次型调节器）控制器的设计方法
    - 学会用 Python 进行控制系统仿真与可视化

📖 阅读建议：
    如果你是第一次接触控制理论，建议按以下顺序阅读：
    1. 先看「物理模型」部分，理解小车和摆杆的运动关系
    2. 再看 InvertedPendulum 类的 dynamics() 方法，了解动力学方程的代码实现
    3. 然后看 LQRController 类，理解控制器是如何"决策"的
    4. 最后看 main() 函数，了解整个仿真流程是如何串联的

🔧 物理模型说明：
    - 一辆小车在水平轨道上左右移动
    - 一根摆杆通过铰链连接在小车上，可以自由旋转
    - 控制目标：通过施加水平力 F，使摆杆保持在竖直向上（不稳定平衡点）
      （就像用手指顶着一根筷子保持竖直不倒）
    - 状态变量 x = [小车位置, 小车速度, 摆杆角度, 摆杆角速度]
      这 4 个量完全描述了系统在任意时刻的"样子"

📐 坐标系约定：
    - x：小车水平位置，向右为正
    - θ：摆杆与竖直向上方向的夹角，顺时针为正
    - θ=0 即为摆杆竖直向上的平衡位置（我们的控制目标）

📚 参考文献：
    - 系统建模参考经典的 Cart-Pole 动力学方程

作者: CodeWhale
日期: 2026-08-04
"""

# ===========================================================================
# 导入依赖库 —— 这些是 Python 科学计算的"三件套"
# ===========================================================================

# sys：提供与 Python 解释器交互的功能（这里用来修复控制台编码问题）
import sys

# numpy：Python 科学计算的基石，提供多维数组（ndarray）和矩阵运算
# 简单理解：numpy 数组就像"超级加强版的 Python 列表"，能高效做向量/矩阵运算
import numpy as np

# scipy.linalg.solve_continuous_are：求解连续时间代数 Riccati 方程
# 这是 LQR 控制器的数学核心 —— 不用手算，一个函数调用搞定
from scipy.linalg import solve_continuous_are

# scipy.integrate.solve_ivp：求解常微分方程（ODE）初值问题
# "ivp" = Initial Value Problem（初值问题）
# 作用：给定初始状态和动力学方程，算出未来任意时刻的状态
from scipy.integrate import solve_ivp

# matplotlib：Python 最常用的绘图库，功能类似 MATLAB 的 plot
import matplotlib.pyplot as plt

# FuncAnimation：matplotlib 的动画模块，让图片"动起来"
from matplotlib.animation import FuncAnimation

# Rectangle, Circle：matplotlib 的图形元素，用来画小车（矩形）和摆杆末端球（圆形）
from matplotlib.patches import Rectangle, Circle

# ---- matplotlib 中文字体配置 ----
# 默认字体 DejaVu Sans 不包含中文字形，所以必须指定支持中文的字体
# 按优先级依次尝试：微软雅黑 → 黑体 → 楷体 → 文泉驿微米黑
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'KaiTi', 'WenQuanYi Micro Hei']

# unicode_minus=False：让 matplotlib 使用 ASCII 减号而非 Unicode 减号
# 否则负号可能因为字体不支持而显示为方块
plt.rcParams['axes.unicode_minus'] = False

# ---- Windows 控制台编码修复 ----
# Windows 命令行默认使用 GBK 编码，无法输出 ✓ ✗ × ² ° 等 Unicode 符号
# sys.stdout.reconfigure(encoding='utf-8') 把输出编码切换为 UTF-8
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass   # 如果切换失败（比如在某些旧版 Python 中），静默忽略

# ============================================================================
# 第1部分：系统参数定义
# ============================================================================

class InvertedPendulum:
    """
    倒立摆系统的物理参数与动力学模型。
    
    这个类就像一个"虚拟实验台"——它存储了小车和摆杆的所有物理参数，
    并根据牛顿力学（拉格朗日方程）计算系统在受力后的运动。

    ╔═══════════════════════╗
    ║   🏗️  物理参数说明    ║
    ╚═══════════════════════╝
        M  : 小车质量 (kg)              —— 小车越重，越难推动
        m  : 摆杆质量 (kg)              —— 摆杆越重，倒下越快
        l  : 摆杆质心到转轴的距离 (m)    —— 即半杆长，摆杆越长越难控制
        I  : 摆杆绕质心的转动惯量 (kg·m²)—— 衡量摆杆"抗拒旋转"的程度
        g  : 重力加速度 (m/s²)          —— 默认 9.81，正是它让摆杆往下掉
        b  : 小车与轨道的粘性摩擦系数     —— 小车移动时的"阻力"
        c  : 摆杆转轴的粘性摩擦系数       —— 摆杆旋转时的"阻力"
    
    这些参数可以自由修改来测试不同场景：
        想更难控制？→ 增大 m、l，或减小 M
        想更真实？  → 增大 b、c（加入更多阻尼）
    """

    def __init__(self):
        """
        构造函数 —— 初始化倒立摆的所有物理参数。
        
        Python 知识点：__init__ 是类的"初始化方法"，
        当你写 pendulum = InvertedPendulum() 时自动调用。
        self.xxx 定义的变量可以在类的其他方法中通过 self.xxx 访问。
        """
        # ---------- 物理参数 ----------
        # 你可以修改这些数值来测试不同的场景！
        self.M = 0.5      # 小车质量 0.5 kg（相当于一瓶矿泉水）
        self.m = 0.2      # 摆杆质量 0.2 kg
        self.l = 0.3      # 摆杆半长 0.3 m（全长 0.6 m，约一根筷子长度）
        self.g = 9.81     # 重力加速度（地球上约 9.8 m/s²）
        self.b = 0.1      # 小车摩擦系数（越大 → 小车运动阻力越大）
        self.c = 0.002    # 转轴摩擦系数（越大 → 摆杆旋转阻力越大）

        # 转动惯量：均匀细杆绕质心转动的公式
        # 对长度为 2l 的细杆绕质心：I = (1/12)*m*(2l)² = (1/3)*m*l²
        # 直观理解：摆杆越重越长，越"抗拒"被转动
        self.I = (1/3) * self.m * self.l**2

        # ---------- 预计算导出量 ----------
        # 把一些反复出现的组合项提前算好，避免在 dynamics() 中重复计算
        self._precompute()

    def _precompute(self):
        """
        预计算组合常数，提高后续计算效率。
        
        Python 知识点：函数名前的下划线 _ 表示这是"私有方法"，
        约定只在类内部使用，外部代码不应该直接调用它。
        """
        m, M, l, I, g = self.m, self.M, self.l, self.I, self.g
        # 这个分母在动力学方程中反复出现，提前算好避免每次重新计算
        # den = (M+m)(I+ml²) - (ml)²  —— 来源于联立求解二元一次方程组时的行列式
        self._den = (M + m) * I + M * m * l**2

    # ------------------------------------------------------------------------
    # 动力学方程（非线性，完整形式）
    # ------------------------------------------------------------------------
    def dynamics(self, t, state, u):
        """
        非线性动力学方程的右侧函数 —— 这是整个仿真的"物理引擎"。
        
        🎯 这个函数的作用：
            给定当前时刻的状态和控制力，计算状态的变化率（导数）。
            solve_ivp() 会反复调用这个函数来进行数值积分。

        📥 输入参数：
            t     : 当前时间（秒），虽然这里没用上 t，但 solve_ivp 要求这个参数
            state : 状态向量 [x, x_dot, theta, theta_dot] —— 系统当前"样子"
                   x         : 小车水平位置 (m)
                   x_dot     : 小车水平速度 (m/s)
                   theta     : 摆杆与竖直向上方向的夹角 (rad)，顺时针为正
                   theta_dot : 摆杆角速度 (rad/s)
            u     : 施加在小车上的水平力 (N)，正值 = 向右推

        📤 返回值：
            dstate = [x_dot, x_ddot, theta_dot, theta_ddot]
            即四个状态量各自的变化率（对时间的导数）
            
            举个例子方便理解：
            - 如果摆杆正在倒下（theta 越来越大），theta_ddot 会是正值
            - 如果控制器施加的力让小车加速，x_ddot 会是正值

        🔬 工作原理（简化版）：
            1. 从拉格朗日力学推导出两个耦合的二阶微分方程
            2. 把未知的加速度 x_ddot 和 θ_ddot 当成两个未知数
            3. 写成 A * [x_ddot, θ_ddot]^T = b_vec 的矩阵形式
            4. 用 np.linalg.solve 求解 —— 两个方程两个未知数，初中数学！
        """
        # ---- 步骤1：解包状态向量 ----
        # Python 技巧：一行代码把四个元素分别赋给四个变量
        x, x_dot, theta, theta_dot = state

        # ---- 步骤2：取出物理参数（提高可读性） ----
        m, M, l, I, g, b, c = self.m, self.M, self.l, self.I, self.g, self.b, self.c

        # ---- 步骤3：预计算三角函数（避免重复调用） ----
        sin_theta = np.sin(theta)
        cos_theta = np.cos(theta)

        # ---- 步骤4：构造矩阵方程 A * [x_ddot, θ_ddot]^T = b_vec ----
        # 这两个方程来源于拉格朗日力学（详见文件末尾的推导附录）
        #
        # 方程①（小车平动）：
        #   (M + m)·x_ddot + m·l·cosθ·θ_ddot = u - b·x_dot + m·l·sinθ·θ_dot²
        #   ↑           ↑                          ↑    ↑         ↑
        #   总质量×加速度  摆杆质量×切向加速度      外力  摩擦   离心力项
        #
        # 方程②（摆杆转动）：
        #   m·l·cosθ·x_ddot + (I + m·l²)·θ_ddot = m·g·l·sinθ - c·θ_dot
        #   ↑                      ↑                ↑              ↑
        #   小车加速度耦合项      转动惯性项       重力力矩      转轴摩擦

        A = np.array([
            [M + m,               m * l * cos_theta],   # 方程①的系数：[小车项, 摆杆项]
            [m * l * cos_theta,   I + m * l**2    ]     # 方程②的系数：[耦合项, 转动项]
        ])
        b_vec = np.array([
            u - b * x_dot + m * l * sin_theta * theta_dot**2,   # 方程①的右侧
            m * g * l * sin_theta - c * theta_dot                # 方程②的右侧
        ])

        # ---- 步骤5：求解加速度 ----
        # np.linalg.solve 解线性方程组，等价于手算的 Cramer 法则
        sol = np.linalg.solve(A, b_vec)
        x_ddot = sol[0]        # 小车加速度
        theta_ddot = sol[1]    # 摆杆角加速度

        # ---- 步骤6：组装并返回导数向量 ----
        # 注意：位置 x 的导数是速度 x_dot，角度 θ 的导数是角速度 θ_dot
        return np.array([x_dot, x_ddot, theta_dot, theta_ddot])

    # ------------------------------------------------------------------------
    # 线性化模型（在 theta=0, theta_dot=0 处线性化）
    # ------------------------------------------------------------------------
    def linearized_matrices(self):
        """
        计算在直立平衡点附近的线性化状态空间矩阵 A, B。
        
        🎯 为什么要线性化？
            LQR 控制器只能用于"线性系统"（即 A*x + B*u 这种形式），
            但倒立摆的真实动力学是非线性的（有 sinθ、cosθ、θ_dot²）。
            
            解决思路：在平衡点（θ≈0）附近，非线性方程可以近似为线性方程。
            这就像地球表面是球面，但在你脚下的小范围内可以当作平面。

        📐 线性化技巧（小角度近似，只适用于 θ 很小的情况）：
            sin(θ) ≈ θ          （当 θ→0 时，正弦 ≈ 角度本身）
            cos(θ) ≈ 1          （当 θ→0 时，余弦 ≈ 1）
            θ_dot² ≈ 0          （两个小量相乘是二阶小量，可以忽略）

        📊 状态空间表示：
            dx/dt = A * x + B * u
            其中 x = [x, x_dot, θ, θ_dot]^T  是 4×1 的状态向量
                  u = [F]                     是 1×1 的控制输入

        🔢 返回 (A, B)：
            A : (4×4) 系统矩阵 —— 描述系统自身的演化规律（没有外力时的运动）
            B : (4×1) 输入矩阵 —— 描述控制力如何影响系统（外力→加速度的"杠杆"）
        """
        m, M, l, I, g, b, c = self.m, self.M, self.l, self.I, self.g, self.b, self.c
        den = self._den

        # 经过线性化后（Cramer 法则严格推导）：
        # x_ddot = ( -(I+ml²)·b·x_dot - m²gl²·θ + mlc·θ_dot + (I+ml²)·u ) / den
        # θ_ddot = ( mlb·x_dot + (M+m)mgl·θ - (M+m)c·θ_dot - ml·u ) / den

        # 构造 A 矩阵（4×4）
        A = np.zeros((4, 4))
        A[0, 1] = 1.0  # dx/dt = x_dot

        # x_ddot 对 x_dot 的偏导
        A[1, 1] = -(I + m * l**2) * b / den
        # x_ddot 对 theta 的偏导
        A[1, 2] = -(m**2 * g * l**2) / den
        # x_ddot 对 theta_dot 的偏导
        A[1, 3] = m * l * c / den

        A[2, 3] = 1.0  # dtheta/dt = theta_dot

        # theta_ddot 对 x_dot 的偏导
        A[3, 1] = m * l * b / den
        # theta_ddot 对 theta 的偏导
        A[3, 2] = (M + m) * m * g * l / den
        # theta_ddot 对 theta_dot 的偏导
        A[3, 3] = -(M + m) * c / den

        # 构造 B 矩阵（4×1）
        B = np.zeros((4, 1))
        B[1, 0] = (I + m * l**2) / den
        B[3, 0] = -m * l / den

        return A, B


# ============================================================================
# 第2部分：LQR 控制器设计
# ============================================================================

class LQRController:
    """
    线性二次型调节器 (Linear Quadratic Regulator) —— 控制系统的"大脑"
    
    ╔══════════════════════════════════════════════════════════╗
    ║  🤔 LQR 通俗解释                                        ║
    ╚══════════════════════════════════════════════════════════╝
    
    想象你在用手指顶着一根筷子保持竖直：
    - 筷子往右歪了 → 你的手往右移（"跟上"筷子）
    - 筷子往左歪了 → 你的手往左移
    - 筷子歪得越厉害 → 你移动得越快
    - 但你也得控制手的力气，不能猛冲导致过冲
    
    LQR 做的事情一模一样：根据当前状态（筷子歪了多少、歪的速度多快），
    计算一个最优的控制力，同时兼顾"快速纠正"和"省力"。
    
    ╔══════════════════════════════════════════════════════════╗
    ║  📐 数学公式（了解即可，不用背）                        ║
    ╚══════════════════════════════════════════════════════════╝
    
    代价函数（LQR 要最小化的东西）：
        J = ∫ (x^T Q x + u^T R u) dt
         ↑   ↑               ↑
         │   └─ 惩罚状态偏离  └─ 惩罚用力太大
         └─ 积分（从 0 到 ∞）
    
    最优控制律（最终使用的简单公式）：
        u = -K @ x    ← 这就是整个 LQR 的核心结果！
        
        其中 K = R^{-1} B^T P，P 由 Riccati 方程解得。
        你不需要手动解 Riccati 方程，scipy 帮你搞定。
    
    ╔══════════════════════════════════════════════════════════╗
    ║  🎛️ Q 和 R 权重调参指南                                ║
    ╚══════════════════════════════════════════════════════════╝
    
    Q 矩阵（4×4 对角阵）—— 每个状态量偏离零的"罚款"：
        Q[0,0] = 小车位置权重     → 增大会限制小车移动范围
        Q[1,1] = 小车速度权重     → 增大会让小车的运动更"柔和"
        Q[2,2] = 摆杆角度权重 ⭐   → 最重要！决定控制器多"在意"角度偏差
        Q[3,3] = 摆杆角速度权重   → 增大可以抑制摆动
    
    R 矩阵（1×1）—— 用力太大的"罚款"：
        R 越小 → 控制器越大胆，允许更大的控制力（响应更快但可能超调）
        R 越大 → 控制器越保守，控制力更温和（响应较慢但省力）
    
    想自己调参试试？在 main() 函数中修改 Q 和 R 的值即可！
    """

    def __init__(self, A, B, Q=None, R=None):
        """
        LQR 控制器构造函数 —— 初始化并自动计算最优反馈增益 K。
        
        Python 知识点：Q=None, R=None 表示"默认参数"。
        调用方可以不传这两个参数，此时使用类内部预设的默认值。
        
        参数:
            A : 系统矩阵 (4×4) —— 从 pendulum.linearized_matrices() 获得
            B : 输入矩阵 (4×1) —— 同上
            Q : 状态权重矩阵 (4×4)，默认重点关注角度和角速度
            R : 输入权重矩阵 (1×1)，默认 0.1
        """
        self.A = A
        self.B = B

        # 默认 Q: 重点惩罚角度偏差和角速度
        # np.diag([a, b, c, d]) 创建一个对角矩阵，对角线元素依次为 a, b, c, d
        # 非对角线元素都为 0 —— 这意味着"交叉惩罚"为 0
        if Q is None:
            self.Q = np.diag([1.0,    # 小车位置权重（低 —— 小车跑到哪儿我们不太在乎）
                              1.0,    # 小车速度权重（低）
                              100.0,  # 摆杆角度权重（高 ⭐ —— 核心控制目标！）
                              10.0])  # 摆杆角速度权重（中高 —— 抑制快速摆动）
        else:
            self.Q = Q

        if R is None:
            self.R = np.array([[0.1]])  # 控制输入权重 —— 0.1 表示允许适度用力
        else:
            self.R = np.atleast_2d(R)   # np.atleast_2d 确保 R 至少是二维数组

        # 在构造时就计算好最优增益 K，之后每次 compute_control() 直接使用
        self.K = self._compute_gain()

    def _compute_gain(self):
        """
        求解连续时间代数 Riccati 方程并计算最优反馈增益 K。
        
        🧮 计算流程（scipy 帮你完成所有重活）：
            1. solve_continuous_are(A, B, Q, R) → 得到矩阵 P
            2. K = R^{-1} B^T P              → 得到增益矩阵 K
        
        这个 K 就是控制器的"配方"——它告诉你：
        "摆杆偏了 1 弧度 → 应该施加 K[2] 牛顿的力"
        "小车在移动      → 应该施加 K[1] 牛顿的力来抵消惯性"
        """
        A, B, Q, R = self.A, self.B, self.Q, self.R

        # solve_continuous_are 求解 Riccati 方程
        # 输入：系统的 A、B 和权重 Q、R
        # 输出：矩阵 P（4×4），二次型代价函数的最优解
        P = solve_continuous_are(A, B, Q, R)

        # 计算反馈增益 K = R^{-1} * B^T * P
        # 用 np.linalg.solve(R, B.T @ P) 而不是 R^{-1} @ ...，
        # 因为 solve 比直接求逆矩阵更数值稳定
        K = np.linalg.solve(R, B.T @ P)

        return K

    def compute_control(self, state):
        """
        根据当前状态计算控制力 —— 这就是控制器的"决策"函数。
        
        这个函数在仿真中每 0.01 秒被调用一次，相当于：
        "现在摆杆这个姿势，我该用多大力去推小车？"
        
        参数:
            state : 状态向量 [x, x_dot, theta, theta_dot]
        
        返回:
            u : 控制力 (N)，正值 = 向右推小车
        
        计算公式：u = -K @ state
            K @ state 是矩阵乘法（点积），得到一个数。
            负号表示"反馈"——状态偏离正值时施加负方向力来纠正。
            
        Python 知识点：
            - @ 是矩阵乘法运算符（Python 3.5+）
            - .item() 把 numpy 单元素数组转为 Python 标量 float
            - float() 确保返回值是普通浮点数
        """
        return float((-self.K @ state).item())


# ============================================================================
# 第3部分：仿真运行
# ============================================================================

def run_simulation(pendulum, controller, initial_state, t_span, dt_control=0.01):
    """
    运行闭环仿真 —— 模拟倒立摆在 LQR 控制器作用下的运动过程。
    
    ╔══════════════════════════════════════════════════════════╗
    ║  🔄 仿真循环 = "测量 → 决策 → 执行 → 前进一小步"    ║
    ╚══════════════════════════════════════════════════════════╝
    
    每 0.01 秒重复以下步骤：
        1. 📏 测量：控制器读取当前状态（摆杆歪了多少、小车在哪儿）
        2. 🧠 决策：controller.compute_control() 算出该用多大力
        3. ⚡ 执行：用 solve_ivp() 模拟物理系统在这个力作用下的运动
        4. ⏩ 前进：时间推进 0.01 秒，回到步骤 1
    
    Python 知识点：solve_ivp
        ivp = Initial Value Problem（初值问题）
        solve_ivp 是 scipy 的常微分方程求解器，它会在每个控制周期内
        自动选择合适的步长来保证精度，比手工写 Euler 法要精确得多。

    参数:
        pendulum      : InvertedPendulum 实例 —— 物理系统
        controller    : LQRController 实例    —— 控制器
        initial_state : 初始状态 [x0, x_dot0, theta0, theta_dot0]
        t_span        : (t_start, t_end) 仿真时间范围，单位秒
        dt_control    : 控制周期 (s) = 0.01，即每秒更新 100 次控制力

    返回:
        t_history     : 时间序列数组   (形状 N,)
        state_history : 状态轨迹数组   (形状 N × 4)
        u_history     : 控制输入序列   (形状 N,)
    """
    t_start, t_end = t_span

    # ---- 初始化：记录第 0 秒的数据 ----
    # Python 知识点：用列表 [] 存储历史，最后用 np.array() 一次性转换
    t_history = [t_start]                              # 时间列表
    state_history = [np.array(initial_state)]           # 状态列表
    u_history = [controller.compute_control(initial_state)]  # 控制力列表

    current_state = np.array(initial_state, dtype=float)
    t_current = t_start

    # ---- 主仿真循环 ----
    # while 循环：只要还没到截止时间，就一直推进仿真
    while t_current < t_end:
        # ---------- 步骤 1+2：测量 + 决策 ----------
        # controller.compute_control 根据当前状态计算最优控制力
        u = controller.compute_control(current_state)

        # ---------- 步骤 3：执行（ODE 数值积分）----------
        # solve_ivp 从 t_current 积分到 t_next（一个控制周期）
        # 在这 0.01 秒内，控制力 u 保持恒定
        t_next = min(t_current + dt_control, t_end)
        sol = solve_ivp(
            fun=lambda t, y: pendulum.dynamics(t, y, u),
            #    ↑ lambda 匿名函数：把控制力 u "冻结"在当前的动力学中
            t_span=(t_current, t_next),    # 积分时间区间
            y0=current_state,              # 初始状态
            method='RK45',                 # Runge-Kutta 4(5) 自适应方法
            max_step=dt_control / 10,      # 最大步长 = 0.001s（10 倍精度）
            rtol=1e-6,                     # 相对误差容限（0.0001%）
            atol=1e-8                      # 绝对误差容限
        )

        # ---------- 步骤 4：更新状态并记录 ----------
        # sol.y[:, -1] 取积分结果的最后一列 = 该周期结束时的状态
        current_state = sol.y[:, -1]
        t_current = t_next

        # 记录这一个时间步的结果
        t_history.append(t_current)
        state_history.append(current_state.copy())   # .copy() 防止后续修改影响历史
        u_history.append(u)

    # 最后把列表转成 numpy 数组，方便后续绘图和计算
    return (np.array(t_history),
            np.array(state_history),
            np.array(u_history))


# ============================================================================
# 第4部分：结果可视化
# ============================================================================

def plot_results(t, states, u, pendulum):
    """
    绘制仿真结果 —— 在一个 3×2 的画布上展示所有状态和控制力。
    
    ╔══════════════════════════════════════════════╗
    ║  📊 子图布局 (3 行 × 2 列 = 6 个面板)       ║
    ╚══════════════════════════════════════════════╝
    
    第 1 行：小车位置 x   | 小车速度 ẋ
    第 2 行：摆杆角度 θ   | 摆杆角速度 θ̇
    第 3 行：控制力 u     | 参数信息面板
    
    每条曲线中的水平虚线 (y=0) 表示目标平衡点。

    参数:
        t        : 时间序列 (N,)       —— 横轴
        states   : 状态轨迹 (N × 4)    —— 4 列分别是 [x, ẋ, θ, θ̇]
        u        : 控制输入序列 (N,)    —— LQR 输出的控制力
        pendulum : 系统实例 —— 用于获取参数信息
    """
    # plt.subplots(3, 2) 创建 3 行 2 列的网格，返回 Figure 和 Axes 数组
    # fig = 整个画布，axes[i,j] = 第 i 行第 j 列的子图
    fig, axes = plt.subplots(3, 2, figsize=(12, 10))
    fig.suptitle('倒立摆 LQR 控制仿真结果', fontsize=16, fontweight='bold')

    # 4 个状态变量的标签和颜色
    # Python 知识点：列表中的每个元素是 (标签, 颜色) 的元组 (tuple)
    labels = [
        ('小车位置 $x$ (m)', 'b'),                    # b = blue
        (r'小车速度 $\dot{x}$ (m/s)', 'g'),           # g = green
        ('摆杆角度 $\\theta$ (rad)', 'r'),             # r = red
        (r'摆杆角速度 $\dot{\theta}$ (rad/s)', 'orange'),  # orange = 橙色
    ]

    # ---- 前 4 个子图：4 个状态变量 ----
    # enumerate() 同时给出索引 i 和元素 (ylabel, color)
    # i//2 是行号，i%2 是列号（整数除法和取余）
    for i, (ylabel, color) in enumerate(labels):
        ax = axes[i // 2, i % 2]                     # 选中对应的子图
        ax.plot(t, states[:, i], color=color, linewidth=1.5)  # states[:,i] = 第 i 列
        ax.axhline(y=0, color='k', linewidth=0.5, linestyle='--')  # 目标线
        ax.set_xlabel('时间 (s)')
        ax.set_ylabel(ylabel)
        ax.set_title(ylabel)
        ax.grid(True, alpha=0.3)                      # 半透明网格

    # ---- 第 5 个子图：控制输入 u ----
    ax_u = axes[2, 0]
    ax_u.plot(t, u, color='purple', linewidth=1.5)    # 紫色曲线
    ax_u.axhline(y=0, color='k', linewidth=0.5, linestyle='--')
    ax_u.set_xlabel('时间 (s)')
    ax_u.set_ylabel('控制力 $u$ (N)')
    ax_u.set_title('控制输入（水平力）')
    ax_u.grid(True, alpha=0.3)

    # ---- 第 6 个子图：参数信息面板 ----
    ax_info = axes[2, 1]
    ax_info.axis('off')                               # 隐藏坐标轴
    # f-string 格式化字符串 —— f"..." 中的 {变量} 会被替换为实际值
    info_text = (
        f"系统参数：\n"
        f"  小车质量 M = {pendulum.M} kg\n"
        f"  摆杆质量 m = {pendulum.m} kg\n"
        f"  摆杆半长 l = {pendulum.l} m\n"
        f"  重力加速度 g = {pendulum.g} m/s²\n\n"
        f"LQR 权重：\n"
        f"  Q = diag(1, 1, 100, 10)\n"
        f"  R = [0.1]\n\n"
        f"绿色虚线 = 目标平衡点 (θ=0)"
    )
    # ax.text() 在子图指定位置放置文字
    # transform=ax.transAxes 表示坐标是相对于子图的 (0,0) 到 (1,1)
    ax_info.text(0.1, 0.5, info_text, transform=ax_info.transAxes,
                 fontsize=11, verticalalignment='center',
                 fontfamily='monospace',
                 bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()    # 自动调整子图间距，避免标签重叠
    # plt.show() 已移至 main() 末尾统一调用，避免阻塞后续动画显示


# ============================================================================
# 第5部分：动画可视化
# ============================================================================

def animate_pendulum(t, states, pendulum, save_gif=False, filename='inverted_pendulum.gif'):
    """
    创建倒立摆系统的实时动画 —— 用可视化的方式展示 LQR 控制器的工作过程。
    
    ╔══════════════════════════════════════════════════════════╗
    ║  🎬 动画组成元素                                        ║
    ╚══════════════════════════════════════════════════════════╝
    
    - 灰色水平线 = 轨道
    - 蓝色矩形 = 小车 (steelblue)
    - 红色粗线 = 摆杆 (darkred)
    - 红色圆球 = 摆杆末端质量 (crimson)
    - 金色小圆 = 转轴点 (gold)
    
    ╔══════════════════════════════════════════════════════════╗
    ║  🐍 Python 知识点：matplotlib 动画                      ║
    ╚══════════════════════════════════════════════════════════╝
    
    FuncAnimation 需要三个核心组件：
        1. init()    —— 初始化函数，设置所有元素的起始状态
        2. update(i) —— 更新函数，绘制第 i 帧（每帧改变图形元素位置）
        3. frames    —— 帧索引列表，决定 update() 被调用多少次

    参数:
        t         : 时间序列
        states    : 状态轨迹 (N × 4)
        pendulum  : 系统参数
        save_gif  : 是否保存为 GIF 文件（需要 pillow 库）
        filename  : 保存的文件名
    """
    l = pendulum.l  # 摆杆半长

    # ---- 步骤 1：设置图形 ----
    fig, ax = plt.subplots(figsize=(10, 5))    # 10×5 英寸的画布
    ax.set_xlim(-3, 3)          # 水平视野范围：-3m 到 +3m
    ax.set_ylim(-0.5, 2.0)      # 垂直视野范围：-0.5m 到 2.0m
    ax.set_aspect('equal')      # 等比例坐标轴（1m 在 x 和 y 方向长度相同）
    ax.grid(True, alpha=0.3)    # 半透明网格
    ax.set_title('倒立摆 LQR 控制 —— 动画演示', fontsize=14, fontweight='bold')
    ax.set_xlabel('水平位置 (m)')

    # 轨道线（小车在它上面移动）
    ax.axhline(y=0, color='gray', linewidth=2, linestyle='-', alpha=0.5)

    # ---- 步骤 2：创建绘图元素（此时位置都是临时的，之后由 update() 更新）----

    # 小车 —— 用蓝色矩形表示
    cart_width, cart_height = 0.4, 0.2
    cart = Rectangle((-cart_width / 2, -cart_height / 2),
                     cart_width, cart_height,
                     facecolor='steelblue', edgecolor='black', linewidth=1.5)
    ax.add_patch(cart)   # 把矩形加入画布

    # 摆杆 —— 用红色粗线段表示
    # 注意 pole_line, 后面的逗号 —— 这是 Python 的"解包"语法
    # ax.plot() 返回一个只有一个元素的列表，加逗号解包出那个元素
    pole_line, = ax.plot([], [], color='darkred', linewidth=4, solid_capstyle='round')

    # 摆杆末端的质量球 —— 用红色实心圆表示
    ball = Circle((0, 0), 0.06, facecolor='crimson', edgecolor='black', linewidth=1)
    ax.add_patch(ball)

    # 转轴点（小车顶部与摆杆的连接处）—— 用金色小圆表示
    pivot = Circle((0, 0), 0.05, facecolor='gold', edgecolor='black', linewidth=1)
    ax.add_patch(pivot)

    # 时间/角度显示文字
    # transform=ax.transAxes：坐标 (0.02, 0.95) 是相对于子图的百分比位置
    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes,
                        fontsize=12, verticalalignment='top',
                        bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))

    # ---- 步骤 3：定义 init() —— 动画第一帧的初始化 ----
    def init():
        """重置所有元素到初始位置。FuncAnimation 会在动画开始时调用一次。"""
        cart.set_xy((-cart_width / 2, -cart_height / 2))  # 小车回到原点
        pole_line.set_data([], [])                         # 摆杆消失
        ball.set_center((0, 0))                           # 球回到原点
        pivot.set_center((0, 0))                          # 转轴回到原点
        time_text.set_text('')                             # 文字清空
        # blit=True 模式下，必须返回所有会被修改的图形对象
        return cart, pole_line, ball, pivot, time_text

    # ---- 步骤 4：定义 update() —— 每一帧的绘制逻辑 ----
    def update(frame_idx):
        """
        绘制第 frame_idx 帧。
        
        参数 frame_idx：当前帧在 states 数组中的行索引。
        返回值：所有被修改的图形对象（blit=True 模式下必需）。
        """
        x = states[frame_idx, 0]       # 当前帧的小车位置
        theta = states[frame_idx, 2]   # 当前帧的摆杆角度 (rad)

        # 4a. 更新小车位置（移动矩形）
        cart.set_xy((x - cart_width / 2, -cart_height / 2))

        # 4b. 更新转轴点（小车顶部中心 = 摆杆底部支点）
        pivot_x = x
        pivot_y = cart_height / 2
        pivot.set_center((pivot_x, pivot_y))

        # 4c. 计算摆杆端点坐标（从转轴点沿摆杆方向延伸）
        # 摆杆全长 = 2*l（因为 l 是半长）
        # theta=0 时，cos(0)=1, sin(0)=0 → 摆杆竖直向上 ✓
        pole_tip_x = pivot_x + l * 2 * np.sin(theta)
        pole_tip_y = pivot_y + l * 2 * np.cos(theta)

        # 4d. 更新摆杆线段的位置
        pole_line.set_data([pivot_x, pole_tip_x],
                           [pivot_y, pole_tip_y])

        # 4e. 质量球在摆杆末端
        ball.set_center((pole_tip_x, pole_tip_y))

        # 4f. 更新时间/角度显示
        # np.degrees() 把弧度转成角度（人类更熟悉角度单位）
        time_text.set_text(f't = {t[frame_idx]:.2f} s\nθ = {np.degrees(theta):.1f}°')

        return cart, pole_line, ball, pivot, time_text

    # ---- 步骤 5：创建动画 ----
    # 每隔 skip 帧取一帧，把总帧数控制在 300 以内（避免动画太长或内存爆炸）
    skip = max(1, len(t) // 300)           # 比如 500 帧 ÷ 300 = 隔 1 帧取 1 帧
    frames = range(0, len(t), skip)         # [0, skip, 2*skip, ...]

    ani = FuncAnimation(fig, update, frames=frames,
                        init_func=init,      # 初始化函数
                        blit=True,           # 只重绘变化的元素（提升性能）
                        interval=30,         # 每帧间隔 30ms ≈ 33 FPS
                        repeat=True)         # 播放完循环重放

    if save_gif:
        print(f"正在保存动画到 {filename} ...")
        ani.save(filename, writer='pillow', fps=30, dpi=100)
        print("保存完成！")

    plt.show()    # 显示动画窗口（关闭窗口后继续执行）
    return ani    # 返回动画对象（防止被垃圾回收提前销毁）


# ============================================================================
# 第6部分：主程序入口
# ============================================================================

def main():
    """
    主函数 —— 把前面所有的"零件"组装起来，跑一遍完整的仿真流程。
    
    ╔══════════════════════════════════════════════════════════╗
    ║  🏭 仿真流水线（5 个步骤）                              ║
    ╚══════════════════════════════════════════════════════════╝
    
    [1/5] 创建物理模型     → pendulum = InvertedPendulum()
    [2/5] 线性化（准备 LQR）→ A, B = pendulum.linearized_matrices()
    [3/5] 设计控制器       → controller = LQRController(A, B, Q, R)
    [4/5] 运行仿真         → t, states, u = run_simulation(...)
    [5/5] 可视化结果       → plot_results() + animate_pendulum()
    
    ╔══════════════════════════════════════════════════════════╗
    ║  🎛️  想自己调参？修改下面这些变量：                     ║
    ╚══════════════════════════════════════════════════════════╝
    
    改初始角度 → 修改 initial_theta 的值（弧度，用 np.radians(角度)）
    改仿真时长 → 修改 t_end 的值
    改控制器   → 修改 Q 矩阵和 R 矩阵的值
    改物理参数 → 修改 InvertedPendulum.__init__() 中的 M, m, l 等
    """
    print("=" * 60)
    print("  倒立摆 LQR 控制仿真")
    print("=" * 60)

    # ===== [1/5] 创建物理模型 =====
    # 实例化倒立摆——就像在实验室里搭好了一个真实的装置
    print("\n[1/5] 初始化倒立摆系统模型...")
    pendulum = InvertedPendulum()
    print(f"  小车质量: {pendulum.M} kg, 摆杆质量: {pendulum.m} kg, 摆杆半长: {pendulum.l} m")

    # ===== [2/5] 线性化模型 =====
    # 计算 A 和 B 矩阵——LQR 控制器的"原材料"
    print("\n[2/5] 计算线性化状态空间矩阵 (A, B)...")
    A, B = pendulum.linearized_matrices()
    print(f"  A 矩阵 ({A.shape[0]}×{A.shape[1]}):\n{A}")
    print(f"\n  B 矩阵 ({B.shape[0]}×{B.shape[1]}):\n{B}")

    # ---- 可控性检查 ----
    # 为什么检查可控性？如果系统不可控，LQR 算出来的控制器是无效的
    # 可控性意味着：存在一种控制策略，能把系统从任意初始状态
    # 驱动到任意目标状态（这里是 θ=0 的直立平衡点）
    #
    # 可控性矩阵 C = [B, AB, A²B, A³B]（对于 4 维系统需要 4 列块）
    # 如果 C 的秩 = 4（满秩），说明系统完全可控 ✓
    n = A.shape[0]                                      # 4：状态空间维度
    controllability_matrix = B.copy()                   # 从 B 开始
    temp = B.copy()
    for _ in range(n - 1):                              # 再算 3 次：AB, A²B, A³B
        temp = A @ temp                                 # 每次左乘 A
        controllability_matrix = np.hstack([controllability_matrix, temp])  # 水平拼接
    rank = np.linalg.matrix_rank(controllability_matrix)
    print(f"\n  可控性矩阵秩 = {rank} / {n} {'✓ 系统可控' if rank == n else '✗ 系统不可控！'}")

    # ===== [3/5] 设计 LQR 控制器 =====
    print("\n[3/5] 设计 LQR 控制器...")
    # Q：状态权重 —— 决定了控制器"在乎"哪些状态量
    # 修改这里的值可以改变控制效果！试试把 100 改成 1000 或 10 看看区别
    Q = np.diag([1.0, 1.0, 100.0, 10.0])     # 状态权重：[x, x_dot, theta, theta_dot]
    R = np.array([[0.1]])                     # 控制权重：越大越"省力"
    controller = LQRController(A, B, Q, R)
    print(f"  Q = diag{tuple(np.diag(Q))}")
    print(f"  R = {R[0, 0]}")
    print(f"  最优反馈增益 K = {controller.K.round(4)}")    # .round(4) 保留 4 位小数

    # ===== [4/5] 运行仿真 =====
    print("\n[4/5] 运行闭环仿真...")
    # 初始状态：小车在原点静止，摆杆偏离竖直 15 度
    # np.radians() 把角度转换为弧度（Python 的三角函数使用弧度）
    initial_theta = np.radians(15)               # 初始偏离 15 度
    initial_state = np.array([0.0,               # 小车初始位置 = 0
                              0.0,               # 小车初始速度 = 0（静止）
                              initial_theta,     # 初始角度 = 15°
                              0.0])              # 初始角速度 = 0（静止）
    print(f"  初始状态: x0=0, θ0={np.degrees(initial_theta):.1f}°")

    t_end = 5.0   # 仿真时长 5 秒（足够观察控制器是否稳定）
    t, states, u = run_simulation(pendulum, controller, initial_state,
                                  t_span=(0, t_end), dt_control=0.01)
    # 检查终态角度：理想情况应该接近 0°
    print(f"  仿真完成！共 {len(t)} 个时间步，终态 θ = {np.degrees(states[-1, 2]):.3f}°")

    # ===== [5/5] 可视化结果 =====
    print("\n[5/5] 生成可视化结果...")
    plot_results(t, states, u, pendulum)       # 6 面板图表

    # 动画演示
    # 如果想保存动画为 GIF：改 save_gif=True 即可
    print("\n播放动画演示...")
    animate_pendulum(t, states, pendulum, save_gif=False)

    print("\n仿真结束。")


# ============================================================================
# 附录：动力学方程推导概要
# ============================================================================
"""
以下为小车-倒立摆系统的拉格朗日方程推导（供参考，不需要运行）。

坐标系定义：
    - 小车水平位置：x（向右为正）
    - 摆杆与竖直向上方向的夹角：θ（顺时针为正，θ=0 为直立平衡点）

摆杆质心坐标：
    x_p = x + l * sin(θ)
    y_p = l * cos(θ)            （以转轴为原点，向上为正）

系统动能 T：
    T = 1/2 * M * x_dot²                                    （小车平动动能）
      + 1/2 * m * (x_p_dot² + y_p_dot²)                     （摆杆平动动能）
      + 1/2 * I * θ_dot²                                    （摆杆转动动能）

系统势能 V（以转轴为零势能面）：
    V = m * g * l * cos(θ)

拉格朗日量 L = T - V

广义坐标：q = [x, θ]
广义力：   Q = [F - b*x_dot,  -c*θ_dot]

欧拉-拉格朗日方程：
    d/dt (∂L/∂q_i_dot) - ∂L/∂q_i = Q_i

展开后得到两个耦合的二阶常微分方程，写成矩阵形式即为 dynamics() 方法中的 A * [x_ddot, θ_ddot]^T = b_vec。
"""


# ============================================================================
# 🚀 程序入口 —— 把整个仿真跑起来！
# ============================================================================
#
# Python 知识点：if __name__ == '__main__':
#   这个检查判断当前文件是"直接运行"还是"被 import 导入"。
#   - 直接运行 (python inverted_pendulum_lqr.py) → 执行 main()
#   - 被 import (import inverted_pendulum_lqr) → 不执行 main()，
#     这样其他脚本可以复用这里的类而不自动跑仿真
if __name__ == '__main__':
    main()
