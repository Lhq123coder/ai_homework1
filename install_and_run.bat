@echo off
chcp 65001 >nul
echo 图片水印工具 - 安装和运行脚本
echo ================================

echo.
echo 正在安装依赖包...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo 依赖安装失败！请检查网络连接或 Python 环境。
    pause
    exit /b 1
)

echo.
echo 依赖安装成功！
echo.
echo 使用方法：
echo python watermark_tool.py ^<图片目录路径^> [选项]
echo.
echo 示例：
echo python watermark_tool.py "D:\Photos"
echo python watermark_tool.py "D:\Photos" -s 30 -c red -p top-left
echo.
echo 按任意键退出...
pause >nul
