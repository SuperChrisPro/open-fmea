import sys
import PyInstaller.__main__
import os

# 增加递归限制以避免打包过程中出现栈溢出
sys.setrecursionlimit(5000)

# 定义要包含的文件和目录
datas = [
    ('res', 'res'),  # 资源文件目录
]

# 获取当前目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 定义要排除的模块（减小打包体积）
excludes = [
    'tkinter.test',
    'unittest',
    'email',
    'http',
    'urllib',
    'xml',
    'pydoc',
]

# PyInstaller打包参数
pyinstaller_args = [
    'gui_assembly.py',  # 主程序入口
    '--name=PFMEA_装配专用',  # 可执行文件名
    '--windowed',  # 不显示控制台窗口 (Windows)
    '--onefile',  # 打包为单个可执行文件
    '--clean',  # 清理临时文件
]

# 添加数据文件
for src, dest in datas:
    src_path = os.path.join(current_dir, src)
    if os.path.exists(src_path):
        pyinstaller_args.extend(['--add-data', f'{src_path}{os.pathsep}{dest}'])

# 添加要排除的模块
for exclude in excludes:
    pyinstaller_args.extend(['--exclude-module', exclude])

# 添加图标（如果有）
icon_path = os.path.join(current_dir, 'Ofmea_logo.png')
if os.path.exists(icon_path):
    pyinstaller_args.extend(['--icon', icon_path])

print("开始打包PFMEA装配专用系统...")
print("参数:", " ".join(pyinstaller_args))

# 调用PyInstaller
PyInstaller.__main__.run(pyinstaller_args)

print("打包完成！可在 dist 目录中找到可执行文件。")