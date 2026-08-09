from docx import Document
import subprocess, os

os.chdir(r'C:\Users\allen\daily-code')

# 1. 修复 09.md 的重复内容
md = r'python/2026-08/09.md'
with open(md, 'r', encoding='utf-8') as f:
    content = f.read()

# 删除重复的"踩坑/收获"和"明天计划"
lines = content.split('\n')
new_lines = []
seen_keng = False
seen_plan = False
for line in lines:
    if line.startswith('## 踩坑 / 收获'):
        if seen_keng:
            continue
        seen_keng = True
    elif line.startswith('## 明天计划'):
        if seen_plan:
            continue
        seen_plan = True
    new_lines.append(line)

with open(md, 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_lines))
print('09.md 修复完成')

# 2. 从 git 中移除误加的外部文件
subprocess.run(['git','rm','--cached','-r','%SystemDrive%/ProgramData'], capture_output=True)
subprocess.run(['git','commit','-m','fix: remove stray files'])

# 3. 重新提交修复后的打卡文件
subprocess.run(['git','add','-A'])
subprocess.run(['git','commit','-m','fix: clean up duplicate content in 09.md'])

# 4. 推送
subprocess.run(['git','push'])

# 5. 清理临时脚本
os.remove('_push_today.py')

print('全部完成!')
