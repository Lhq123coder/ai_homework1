# 图片水印工具

这是一个命令行工具，可以从图片的 EXIF 信息中提取拍摄时间，并将其作为水印添加到图片上。

## 功能特点

- 自动读取图片的 EXIF 信息中的拍摄时间
- 支持多种图片格式 (JPG, PNG, TIFF 等)
- 可自定义水印的字体大小、颜色和位置
- 批量处理整个目录中的图片
- 自动创建带水印的图片到新目录

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 基本用法

```bash
python watermark_tool.py <图片目录路径>
```

### 高级用法

```bash
python watermark_tool.py <图片目录路径> -s 30 -c red -p top-left
```

### 参数说明

- `input_dir`: 输入图片目录路径（必需）
- `-s, --size`: 字体大小，默认 24
- `-c, --color`: 水印颜色，默认 white
- `-p, --position`: 水印位置，可选值：
  - `top-left`: 左上角
  - `top-right`: 右上角
  - `bottom-left`: 左下角
  - `bottom-right`: 右下角（默认）
  - `center`: 居中

## 使用示例

```bash
# 基本使用
python watermark_tool.py "D:/Photos"

# 自定义设置
python watermark_tool.py "D:/Photos" -s 32 -c yellow -p center

# 处理当前目录
python watermark_tool.py .
```

## 输出

程序会在原目录的同级目录下创建一个名为 `原目录名_watermark` 的新目录，所有带水印的图片都会保存在那里。

## 支持的图片格式

- JPEG (.jpg, .jpeg)
- PNG (.png)
- TIFF (.tiff, .tif)

## 注意事项

- 如果图片没有 EXIF 信息或无法读取，水印将显示为"拍摄时间未知"
- 程序会自动跳过不支持的文件格式
- 建议在处理大量图片前先测试几张图片
