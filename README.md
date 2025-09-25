# 图片水印工具

这是一个命令行程序，可以从图片的EXIF信息中提取拍摄时间，并将其作为水印添加到图片上。

## 功能特点

- 📸 自动从图片EXIF信息中提取拍摄时间
- 🎨 支持自定义字体大小、颜色和位置
- 📁 支持批量处理整个目录
- 💾 自动创建带水印的新图片文件
- 🌍 支持多种图片格式（JPG、PNG、TIFF、BMP等）

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 基本用法

```bash
# 处理单个图片文件
python watermark_tool.py path/to/image.jpg

# 处理整个目录
python watermark_tool.py path/to/images/
```

### 高级选项

```bash
# 自定义字体大小
python watermark_tool.py path/to/image.jpg --font-size 32

# 自定义颜色
python watermark_tool.py path/to/image.jpg --color red

# 自定义位置
python watermark_tool.py path/to/image.jpg --position 左上角

# 组合使用
python watermark_tool.py path/to/images/ --font-size 28 --color yellow --position 居中
```

### 参数说明

- `path`: 图片文件或目录路径（必需）
- `--font-size`: 字体大小，默认为24
- `--color`: 水印颜色，默认为白色
- `--position`: 水印位置，可选值：
  - `左上角`
  - `右上角`
  - `左下角`
  - `右下角`（默认）
  - `居中`

## 输出说明

- 对于单个文件：在原文件同目录下创建 `原文件名_watermark` 文件夹，保存带水印的图片
- 对于目录：在原目录同目录下创建 `原目录名_watermark` 文件夹，保存所有带水印的图片

## 示例

```bash
# 处理单张图片，使用默认设置
python watermark_tool.py photo.jpg
# 输出：photo_watermark/watermark_photo.jpg

# 处理整个相册，自定义设置
python watermark_tool.py photos/ --font-size 30 --color blue --position 右下角
# 输出：photos_watermark/watermark_*.jpg
```

## 注意事项

1. 程序会自动尝试从图片的EXIF信息中提取拍摄时间
2. 如果图片没有EXIF信息或时间信息，将使用"未知时间"作为水印
3. 支持中文字体显示
4. 水印会添加半透明背景以提高可读性
5. 程序会保持原图片的质量和格式

## 支持的图片格式

- JPEG (.jpg, .jpeg)
- PNG (.png)
- TIFF (.tiff, .tif)
- BMP (.bmp)

## 系统要求

- Python 3.6+
- Pillow 库
