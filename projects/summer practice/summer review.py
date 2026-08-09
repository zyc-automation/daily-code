# print('欢迎来到黑马动物园')
# height=int(input('请输入你的身高：'))
# if height>= 120:
#    print('您的身高超出120cm，游玩需要购票10元')
# else:
#    print('您的身高未超出120cm，可以免费游玩')
# print('祝您游玩愉快。')

# i=1
# sum=0
# while i<=100:
#     sum=i+sum
#     i+=1
# print(sum)

# line=1
# hang=1
# while  hang <= 9 :
#     while line <= 9 and hang>=line:
#         print(f"{line}*{hang}={line*hang}\t",end="")
#         line+=1
#     print()
#     line=1
#     hang+=1

# name="itheima is a brand of itcast"
# num=0
# for x in name:
#     if x=='a' :
#        num+=1
# print(f"itheima is a brand of itcast中共含有：{num}个字母a")

# for hang in range(1,10):
#     for line in range(1,hang+1):
#         print(f"{line}*{hang}={hang*line}\t",end="")
#     print()

#发工资综合练习案例
# import random
# account=10000
# for x in range(1,21):
#     num=random.randint(1,10)
#     if account==0:
#         print("工资发完了，下个月领取吧")
#         break
#     else:
#         if num<5:
#             print(f"员工{x},绩效分{num},低于5,不发工资,下一位")
#         else:
#             account-=1000
#             print(f"向员工{x}发放工资1000元，账户余额还剩下{account}元")
#

# def temper(tem):
#     print('测体温')
#     if tem<=37.5:
#         print("请进")
#     else:
#         print("隔离")
#
# temper(float(input()))

#                                          heima ATM
# money=5000000
# name=input("请输入姓名")
#
# def check():
#     print("--------------查询余额-----------------")
#     print(f"{name}，您好，你的余额剩余：{money}元")
#     menu()
#
# def addplus():
#     print("--------------存款-----------------")
#     global money
#     add_money=int(input(f"{name}，您好，你需要存"))
#     print(f"{name}，您好，您存款{add_money}成功")
#     money+=add_money
#     print(f"{name}，您好，你的余额剩余：{money}元")
#     menu()
#
# def take():
#     print("--------------取款-----------------")
#     global money
#     take_money =int(input(f"{name}，您好，你需要取"))
#     if money>=take_money:
#         money-=take_money
#         print(f"{name}，您好，您取款{take_money}成功")
#         print(f"{name}，您好，你的余额剩余：{money}元")
#     else:
#         print(f"{name}您没有这么多钱")
#     menu()
#
# def menu():
#     print("--------------主菜单-----------------")
#     print(f"{name},您好，欢迎来到黑马银行ATM。请选择操作")
#     print("查询余额\t[输入1]")
#     print("存款\t[输入2]")
#     print("取款\t[输入3]")
#     print("退出\t[输入4]")
#     chosen=input("请输入您的选择")
#     if chosen=='1':
#         check()
#     elif chosen=='2':
#         addplus()
#     elif chosen=='3':
#         take()
#
# menu()

# my_str="itheima itcast boxuegu"
# num1=my_str.count('it')
# num2=my_str.replace(" ","|")
# num3=num2.split("|")
# print(f"{num1},{num2},{num3}")

# my_str="万过薪月，员序程马黑来，nohtyP学"
# num1=my_str[::-1][9:14]
# print(f"{num1}")

# my_list=['黑马程序员','传智播客','黑马程序员','传智播客','itheima','itcast','itheima','itcast','best']
# num=set()
# for x in my_list:
#     num.add(x)
# print(f"{num}")

# my_dict={"王力宏":{'部门':'科技部','工资':3000,'级别':1},
#          "周杰伦":{'部门':'市场部','工资':5000,'级别':2},
#          "林俊杰":{'部门':'市场部','工资':7000,'级别':3},
#          "张学友":{'部门':'科技部','工资':4000,'级别':1},
#          "刘德华":{'部门':'市场部','工资':6000,'级别':2}}
# print(f"全体员工信息如下{my_dict}")
# for key in my_dict:
#     if my_dict[key]['级别']==1:
#         my_dict[key]['级别']+=1
#         my_dict[key]['工资'] += 1000
# print(f"全体员工信息如下{my_dict}")





























