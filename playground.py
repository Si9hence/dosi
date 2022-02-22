import PIL
print('PIL version:', PIL.__version__) 
import textwrap
from PIL import Image, ImageDraw, ImageFont
import math
# create empty image
img = Image.new(size=(400, 300), mode='RGB')
draw = ImageDraw.Draw(img)

# draw white rectangle 200x100 with center in 200,150
draw.rectangle((200-100, 150-50, 200+100, 150+50), fill='white')
draw.line(((0, 150), (400, 150)), 'gray')
draw.line(((200, 0), (200, 300)), 'gray')

def get_sentences(txt:str, box:list[int], font_size_min:int=15):
    # box in [left top width height]
    res = list()
    left, top, width, height = box
    # row_max = math.floor(height/font_size_min)
    inline_max = math.floor(width/font_size_min)
    txts = txt_split_mix(txt=txt, len_max=inline_max)
    if len(txts) == 1:
        font_size = fitting_fs(txt=txts[0], box=box, font_size_min=font_size_min, font_size_max=math.floor(0.75*height))
        res.append({
            'content':txt,
            'pos': [left+math.ceil(width/2), top+math.ceil(height/2)],
            'size': font_size
        })
        return res
    else:
        for idx, txt in enumerate(txts):
            res.append({
                'content': txt,
                'pos': [left+math.ceil(width/2), top+math.ceil(font_size_min/2)+font_size_min*idx],
                'size': font_size_min,            
            })
    return res

def txt_split_mix(txt:str, len_max:int):
    res = list()
    tmp = str()
    cnt = 0
    for letter in txt:
        tmp += letter
        cnt += 1 if len(letter.encode('utf-8') < 3) else 2
        if cnt <= len_max:
            pass
        else:
            cnt = 0
            res.append(tmp)
            tmp = str()
    res.append(tmp)
    if res[-1] == "":
        res.pop()
    return res

def fitting_fs(txt:str, box:list[int], font_size_min:int, font_src='./data/fonts/simhei.ttf', font_size_max:int=50):
    w_max, h_max = box[2::]
    step = 2
    for size in range(1, font_size_max, 2):
        arial = ImageFont.FreeTypeFont(font_src, size=size)
        # w, h = arial.getsize(txt)  # older versions
        left, top, right, bottom = arial.getbbox(txt)  # needs PIL 8.0.0
        # print(left, top, right, bottom)
        w = right - left
        h = bottom - top
        # print(w, h)
        
        if w > w_max or h > h_max:
            break
    size = size - step
    return size


txt = "你能表演一下那个吗? 好运, 不会眷顾傻瓜."
# txt = 'asdasdfasdfddsafasfasdfsa'
txt1 = "1234567890"
# find font size for text `"Hello World"` to fit in rectangle 200x100
selected_size = 1
for size in range(1, 150):
    arial = ImageFont.FreeTypeFont('./data/fonts/simhei.ttf', size=size)
    # w, h = arial.getsize(txt)  # older versions
    left, top, right, bottom = arial.getbbox(txt)  # needs PIL 8.0.0
    print(left, top, right, bottom)
    w = right - left
    h = bottom - top
    print(w, h)
    
    if w > 200 or h > 100:
        break
    selected_size = size

    print(arial.size)
    
# draw text in center of rectangle 200x100        
arial = ImageFont.FreeTypeFont('./data/fonts/simhei.ttf', size=selected_size)

#draw.text((200-w//2, 150-h//2), "Hello World", fill='black', font=arial)  # older versions
#img.save('center-older.png')

draw.text((200, 150), txt, fill='black', anchor='mm', font=arial)
img.save('center-newer.png')

img.show()