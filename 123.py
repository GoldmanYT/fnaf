from PIL import Image, ImageDraw, ImageFont

im = Image.open('data/textures/cameras.png')
font = ImageFont.truetype(r'C:\Windows\Fonts\CENTURY.TTF', 72)
draw = ImageDraw.Draw(im)
draw.font = font

for i in range(52):
    draw.text((i * 1600, 0), f'{i}')

im.save('data/textures/cameras_frames.png', 'PNG')
