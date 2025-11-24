@echo off
echo 正在安装设备装配工厂PFMEA系统...

echo 检查Python环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误：未找到Python环境，请先安装Python 3.9-3.11
    pause
    exit /b 1
)

echo 安装依赖包...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo 错误：依赖包安装失败
    pause
    exit /b 1
)

echo 依赖包安装完成!

echo 启动PFMEA系统...
python gui_assembly.py

pause