from PIL import Image

n = 8
name = 'data/textures/office_'
file_list = [f'{name}{i}.png' for i in range(1, n + 1)]
im_list = [Image.open(file) for file in file_list]
width = max(im_list, key=lambda im: im.width).width
height = max(im_list, key=lambda im: im.height).height
res = Image.new('RGBA', (width * n, height), (0, 0, 0, 0))

for i, im in enumerate(im_list):
    w, h = im.size
    res.paste(im, (i * width, 0, (i + 1) * w, h))

res.save(f'{name[:-1]}.png', 'png')
