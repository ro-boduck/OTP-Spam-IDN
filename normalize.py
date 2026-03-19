import re

with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
for i, line in enumerate(lines):
    if "[DEAD API]" in line:
        continue
    # Only uncomment requests
    if re.search(r'#\s*.*=.*(?:requests\.|json\.loads\(requests)', line):
        lines[i] = re.sub(r'^(\s*)#\s*', r'\1', line)

new_content = '\n'.join(lines)

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Updated main.py successfully')
