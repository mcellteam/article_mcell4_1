#!/usr/bin/python3
from PIL import Image, ImageDraw, ImageFont
from glob import glob
import os

# os.chdir('../result/png')
 
iml = []

path = 'result/png/*.png'
pdf = "result/combined.pdf"

#font = ImageFont.truetype(font='fonts/SourceCodePro-Regular.ttf', size=42)
#font = ImageFont.load_default() 
font = ImageFont.truetype("/Library/Fonts/Arial Unicode.ttf", 40)

files = glob(path)
files.sort()
print('files = ',files)
# rgb.save(PDF_FILE, 'PDF', resoultion=100.0)
# for f in files:
#     print(f)
#     print(f[:-4])
#     newname = f[:-4] + ".png"
#     print(newname)
#     os.rename(f, newname)
# print(files)
# rgba = Image.open(PNG_FILE)
# To avoid ValueError: cannot save mode RGBA 
rgba = Image.open(files[0])
rgb = Image.new('RGB', rgba.size, (255, 255, 255))  # white background
rgb.paste(rgba, mask=rgba.split()[3])               # paste using alpha channel as mask
for img in files[1::]:
    rgba2 = Image.open(img)
    w, h = rgba2.size
    draw = ImageDraw.Draw(rgba2)
    draw.text((0, 0),os.path.basename(img),fill="black",font=font,size=72)
    rgb2 = Image.new('RGB', rgba2.size, (255, 255, 255))  # white background
    rgb2.paste(rgba2, mask=rgba2.split()[3])               # paste using alpha channel as mask
    iml.append(rgb2)
 
rgb.save(pdf, "PDF" ,resolution=600.0, save_all=True, append_images=iml)
