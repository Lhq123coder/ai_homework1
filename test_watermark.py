#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试水印工具
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

def create_test_image(filename, width=800, height=600):
    """创建一个测试图片"""
    # 创建一个渐变背景
    img = Image.new('RGB', (width, height), color='lightblue')
    draw = ImageDraw.Draw(img)
    
    # 绘制一些装饰性内容
    for i in range(0, width, 50):
        draw.line([(i, 0), (i, height)], fill='white', width=1)
    for i in range(0, height, 50):
        draw.line([(0, i), (width, i)], fill='white', width=1)
    
    # 添加一些文字
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 48)
    except:
        font = ImageFont.load_default()
    
    draw.text((width//2-100, height//2-50), "测试图片", fill='darkblue', font=font)
    
    # 保存图片
    img.save(filename, 'JPEG', quality=95)
    print(f"创建测试图片: {filename}")

def main():
    """创建测试环境"""
    # 创建测试目录
    test_dir = "test_images"
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
        print(f"创建测试目录: {test_dir}")
    
    # 创建几张测试图片
    for i in range(3):
        filename = os.path.join(test_dir, f"test_image_{i+1}.jpg")
        create_test_image(filename)
    
    print("\n测试图片创建完成！")
    print("现在可以运行以下命令来测试水印工具：")
    print(f"python watermark_tool.py {test_dir}")

if __name__ == "__main__":
    main()
