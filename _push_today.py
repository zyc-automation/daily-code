import subprocess, os
os.chdir(r'C:\Users\allen\daily-code')
print('[第2步] 拍快照，打标签...')
subprocess.run(['git','commit','-m','2026-08-09 Python打卡-搭建GitHub打卡体系'])
print('[第3步] 推送到GitHub...')
subprocess.run(['git','push'])
print('完成！去 github.com/zyc-automation/daily-code 看看你的绿点吧')
