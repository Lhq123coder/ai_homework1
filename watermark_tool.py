#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片水印工具
从图片的EXIF信息中提取拍摄时间，并将其作为水印添加到图片上
"""

import os
import sys
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from PIL.ExifTags import TAGS
import datetime


class WatermarkTool:
    def __init__(self):
        self.supported_formats = {'.jpg', '.jpeg', '.png', '.tiff', '.tif', '.bmp'}
        
    def get_exif_datetime(self, image_path):
        """从图片的EXIF信息中提取拍摄时间"""
        try:
            with Image.open(image_path) as img:
                exif_data = img._getexif()
                if exif_data is not None:
                    for tag_id, value in exif_data.items():
                        tag = TAGS.get(tag_id, tag_id)
                        if tag == 'DateTime':
                            # EXIF时间格式: "YYYY:MM:DD HH:MM:SS"
                            return value
                        elif tag == 'DateTimeOriginal':
                            return value
                        elif tag == 'DateTimeDigitized':
                            return value
        except Exception as e:
            print(f"读取 {image_path} 的EXIF信息时出错: {e}")
        return None
    
    def parse_datetime(self, datetime_str):
        """解析EXIF时间字符串，返回年月日"""
        if not datetime_str:
            return None
        try:
            # EXIF格式: "YYYY:MM:DD HH:MM:SS"
            dt = datetime.datetime.strptime(datetime_str, "%Y:%m:%d %H:%M:%S")
            return dt.strftime("%Y年%m月%d日")
        except ValueError:
            try:
                # 尝试其他可能的格式
                dt = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
                return dt.strftime("%Y年%m月%d日")
            except ValueError:
                print(f"无法解析时间格式: {datetime_str}")
                return None
    
    def get_watermark_position(self, img_width, img_height, position, text_width, text_height, margin=20):
        """计算水印文本的位置"""
        if position == "左上角":
            return (margin, margin)
        elif position == "右上角":
            return (img_width - text_width - margin, margin)
        elif position == "左下角":
            return (margin, img_height - text_height - margin)
        elif position == "右下角":
            return (img_width - text_width - margin, img_height - text_height - margin)
        elif position == "居中":
            return ((img_width - text_width) // 2, (img_height - text_height) // 2)
        else:
            # 默认右下角
            return (img_width - text_width - margin, img_height - text_height - margin)
    
    def add_watermark(self, image_path, output_path, watermark_text, font_size=24, 
                     color='white', position='右下角'):
        """给图片添加水印"""
        try:
            # 打开图片
            with Image.open(image_path) as img:
                # 创建绘图对象
                draw = ImageDraw.Draw(img)
                
                # 尝试加载字体，如果失败则使用默认字体
                try:
                    font = ImageFont.truetype("arial.ttf", font_size)
                except:
                    try:
                        # 尝试系统中文字体
                        font = ImageFont.truetype("C:/Windows/Fonts/simsun.ttc", font_size)
                    except:
                        # 使用默认字体
                        font = ImageFont.load_default()
                
                # 获取文本尺寸
                bbox = draw.textbbox((0, 0), watermark_text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                # 计算水印位置
                x, y = self.get_watermark_position(img.width, img.height, position, 
                                                 text_width, text_height)
                
                # 添加半透明背景（可选）
                padding = 5
                bg_bbox = (x - padding, y - padding, x + text_width + padding, y + text_height + padding)
                draw.rectangle(bg_bbox, fill=(0, 0, 0, 128))  # 半透明黑色背景
                
                # 绘制水印文本
                draw.text((x, y), watermark_text, fill=color, font=font)
                
                # 保存图片
                img.save(output_path, quality=95)
                print(f"已保存水印图片: {output_path}")
                
        except Exception as e:
            print(f"处理图片 {image_path} 时出错: {e}")
    
    def process_directory(self, directory_path, font_size=24, color='white', position='右下角'):
        """处理目录中的所有图片文件"""
        directory_path = Path(directory_path)
        
        if not directory_path.exists():
            print(f"目录不存在: {directory_path}")
            return
        
        # 创建输出目录
        output_dir = directory_path.parent / f"{directory_path.name}_watermark"
        output_dir.mkdir(exist_ok=True)
        print(f"创建输出目录: {output_dir}")
        
        # 获取所有支持的图片文件
        image_files = []
        for ext in self.supported_formats:
            image_files.extend(directory_path.glob(f"*{ext}"))
            image_files.extend(directory_path.glob(f"*{ext.upper()}"))
        
        if not image_files:
            print(f"在目录 {directory_path} 中没有找到支持的图片文件")
            return
        
        print(f"找到 {len(image_files)} 个图片文件")
        
        # 处理每个图片文件
        for image_file in image_files:
            print(f"\n处理文件: {image_file.name}")
            
            # 获取EXIF时间信息
            datetime_str = self.get_exif_datetime(image_file)
            watermark_text = self.parse_datetime(datetime_str)
            
            if watermark_text:
                print(f"提取到拍摄时间: {watermark_text}")
            else:
                watermark_text = "未知时间"
                print("未找到拍摄时间信息，使用默认文本")
            
            # 生成输出文件名
            output_file = output_dir / f"watermark_{image_file.name}"
            
            # 添加水印
            self.add_watermark(image_file, output_file, watermark_text, 
                             font_size, color, position)


def main():
    parser = argparse.ArgumentParser(description='图片水印工具 - 从EXIF信息提取拍摄时间并添加水印')
    parser.add_argument('path', help='图片文件或目录路径')
    parser.add_argument('--font-size', type=int, default=24, help='字体大小 (默认: 24)')
    parser.add_argument('--color', default='white', help='水印颜色 (默认: white)')
    parser.add_argument('--position', choices=['左上角', '右上角', '左下角', '右下角', '居中'], 
                       default='右下角', help='水印位置 (默认: 右下角)')
    
    args = parser.parse_args()
    
    tool = WatermarkTool()
    
    path = Path(args.path)
    
    if path.is_file():
        # 处理单个文件
        print(f"处理单个文件: {path}")
        datetime_str = tool.get_exif_datetime(path)
        watermark_text = tool.parse_datetime(datetime_str)
        
        if watermark_text:
            print(f"提取到拍摄时间: {watermark_text}")
        else:
            watermark_text = "未知时间"
            print("未找到拍摄时间信息，使用默认文本")
        
        # 创建输出目录
        output_dir = path.parent / f"{path.stem}_watermark"
        output_dir.mkdir(exist_ok=True)
        
        # 生成输出文件名
        output_file = output_dir / f"watermark_{path.name}"
        
        # 添加水印
        tool.add_watermark(path, output_file, watermark_text, 
                         args.font_size, args.color, args.position)
        
    elif path.is_dir():
        # 处理目录
        print(f"处理目录: {path}")
        tool.process_directory(path, args.font_size, args.color, args.position)
        
    else:
        print(f"路径不存在: {path}")


if __name__ == "__main__":
    main()
