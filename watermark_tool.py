#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片水印工具
从图片的 EXIF 信息中提取拍摄时间作为水印，并添加到图片上
"""

import os
import sys
import argparse
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from PIL.ExifTags import TAGS
import exifread
from pathlib import Path


class WatermarkTool:
    def __init__(self):
        self.supported_formats = {'.jpg', '.jpeg', '.png', '.tiff', '.tif'}
        
    def get_exif_date(self, image_path):
        """从图片的 EXIF 信息中提取拍摄日期"""
        try:
            with open(image_path, 'rb') as f:
                tags = exifread.process_file(f, details=False)
                
            # 尝试不同的日期字段
            date_fields = ['EXIF DateTimeOriginal', 'EXIF DateTimeDigitized', 'Image DateTime']
            
            for field in date_fields:
                if field in tags:
                    date_str = str(tags[field])
                    # 解析日期格式 "YYYY:MM:DD HH:MM:SS"
                    if ':' in date_str:
                        try:
                            date_obj = datetime.strptime(date_str.split()[0], '%Y:%m:%d')
                            return date_obj.strftime('%Y年%m月%d日')
                        except ValueError:
                            continue
            
            return None
            
        except Exception as e:
            print(f"读取 EXIF 信息失败 {image_path}: {e}")
            return None
    
    def get_watermark_position(self, img_width, img_height, position, font_size):
        """计算水印位置"""
        # 根据字体大小估算文本尺寸（粗略估算）
        text_width = font_size * 8  # 假设每个字符宽度约为字体大小的0.8倍
        text_height = font_size
        
        if position == 'top-left':
            return (10, 10)
        elif position == 'top-right':
            return (img_width - text_width - 10, 10)
        elif position == 'bottom-left':
            return (10, img_height - text_height - 10)
        elif position == 'bottom-right':
            return (img_width - text_width - 10, img_height - text_height - 10)
        elif position == 'center':
            return ((img_width - text_width) // 2, (img_height - text_height) // 2)
        else:
            return (10, 10)  # 默认左上角
    
    def add_watermark(self, image_path, output_path, watermark_text, font_size=24, 
                     color='white', position='bottom-right'):
        """为图片添加水印"""
        try:
            # 打开图片
            with Image.open(image_path) as img:
                # 如果是 RGBA 模式，转换为 RGB
                if img.mode == 'RGBA':
                    img = img.convert('RGB')
                
                # 创建绘图对象
                draw = ImageDraw.Draw(img)
                
                # 尝试加载字体，如果失败则使用默认字体
                try:
                    font = ImageFont.truetype("arial.ttf", font_size)
                except:
                    try:
                        font = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", font_size)  # 微软雅黑
                    except:
                        font = ImageFont.load_default()
                
                # 计算水印位置
                x, y = self.get_watermark_position(img.width, img.height, position, font_size)
                
                # 绘制水印文本
                draw.text((x, y), watermark_text, fill=color, font=font)
                
                # 保存图片
                img.save(output_path, quality=95)
                print(f"✓ 已处理: {os.path.basename(image_path)}")
                
        except Exception as e:
            print(f"✗ 处理失败 {image_path}: {e}")
    
    def process_directory(self, input_dir, font_size=24, color='white', position='bottom-right'):
        """处理目录中的所有图片"""
        input_path = Path(input_dir)
        
        if not input_path.exists():
            print(f"错误: 目录不存在 {input_dir}")
            return
        
        # 创建输出目录
        output_dir = input_path.parent / f"{input_path.name}_watermark"
        output_dir.mkdir(exist_ok=True)
        
        print(f"输入目录: {input_dir}")
        print(f"输出目录: {output_dir}")
        print(f"字体大小: {font_size}, 颜色: {color}, 位置: {position}")
        print("-" * 50)
        
        processed_count = 0
        
        # 遍历目录中的所有文件
        for file_path in input_path.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in self.supported_formats:
                # 获取 EXIF 日期
                date_text = self.get_exif_date(file_path)
                
                if date_text:
                    watermark_text = f"拍摄于 {date_text}"
                else:
                    watermark_text = f"拍摄时间未知"
                
                # 生成输出文件名
                output_path = output_dir / f"{file_path.stem}_watermark{file_path.suffix}"
                
                # 添加水印
                self.add_watermark(str(file_path), str(output_path), watermark_text, 
                                 font_size, color, position)
                processed_count += 1
        
        print("-" * 50)
        print(f"处理完成! 共处理 {processed_count} 张图片")


def main():
    parser = argparse.ArgumentParser(description='图片水印工具 - 从 EXIF 信息提取拍摄时间作为水印')
    parser.add_argument('input_dir', help='输入图片目录路径')
    parser.add_argument('-s', '--size', type=int, default=24, help='字体大小 (默认: 24)')
    parser.add_argument('-c', '--color', default='white', help='水印颜色 (默认: white)')
    parser.add_argument('-p', '--position', 
                       choices=['top-left', 'top-right', 'bottom-left', 'bottom-right', 'center'],
                       default='bottom-right', help='水印位置 (默认: bottom-right)')
    
    args = parser.parse_args()
    
    # 创建水印工具实例
    tool = WatermarkTool()
    
    # 处理目录
    tool.process_directory(args.input_dir, args.size, args.color, args.position)


if __name__ == "__main__":
    main()
