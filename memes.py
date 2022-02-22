import cv2
import yaml
import os
import numpy as np
import PIL
# print('PIL version:', PIL.__version__) 
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import io
import math
config = yaml.safe_load(open("./configs/memes.yaml", "r"))

def search_img(meme, path_src=config['templates_path']) -> str:
    files = os.listdir(path_src)
    if meme + ".jpg" in files:
        meme_path = os.path.join(path_src, meme + ".jpg")
    elif meme + ".png" in files:
        meme_path = os.path.join(path_src, meme + ".png")
    else:
        meme_path = ""
    return meme_path

def cv2AddText(img, text, position, textColor=(0, 0, 0), textSize=30, font=os.path.join(config['fonts_path'], config['font_name'])):
    if (isinstance(img, np.ndarray)):
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    # font style
    fontStyle = ImageFont.truetype(
        font, textSize, encoding="utf-8")
    # put text
    draw.text(position, text, textColor, font=fontStyle, align="right")

    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)

def maker_main(meme:str, sentences:list[str]):
    flag_success = 0
    if meme in config['surjection']:
        info = config['surjection'][meme]
        if 'font_size' not in info:
            info['font_size'] = [10 for _ in range(len(info['box']))]
    else:
        return flag_success, None, None

    if meme_path := search_img(meme, path_src=config['templates_path']):
        # meme_path = search_img
        # info['src'] = meme_path
        pass
    else:
        return flag_success, None, None

    img = cv2.imread(meme_path)
    contents = list()
    if len(sentences) < len(info['box']):
        sentences = sentences + [" " for _ in range(len(info['box']) - len(sentences))]
    for idx, itm in enumerate(info['box']):
        # contents.append(
        #     {
        #         'content': sentences[idx],
        #         'pos': itm,
        #         'size': info['font_size'][idx]
        #     },
        # )

        contents += get_sentences(txt=sentences[idx], box=info['box'][idx], font_size_min=info['font_size'][idx])
    for content in contents:
        txt = content['content']
        txt_pos = content['pos']
        txt_size = content['size']
        # print(txt)
        img = cv2AddText(img, text=txt, position=txt_pos, textColor=(0, 0, 0), textSize=txt_size)
    is_success, buffer = cv2.imencode(".png", img)
    io_buf = io.BytesIO(buffer)
    flag_success = 1
    # cv2.imwrite(filename='text.png',img=img)
    # plt.imshow(img)
    # return img
    return flag_success, io_buf, img

def count_ascii(txt:str):
    cnt = 0
    for word in txt:
        if word.isascii():
            cnt += 1
        else:
            cnt += 2
    return cnt

def get_sentences(txt:str, box:list[int], font_size_min:int=15):
    # box in [left top width height]
    res = list()
    left, top, width, height = box
    # row_max = math.floor(height/font_size_min)
    txts = txt_split_mix(txt=txt, len_max=width, font_size=font_size_min)
    font_size = fitting_fs(txt=txts[0], box=box, font_size_min=font_size_min)

    # for idx, txt in enumerate(txts):
    #     cnt = count_ascii(txt)
    #     if idx == 0:
    #         x = left + (width-font_size*cnt/2)/2
    #     else:
    #         x = left
    #     res.append({
    #         'content':txt,
    #         'pos': [x, top+(height-font_size)/2+font_size*idx],
    #         # 'pos': [left, top],
    #         'size': font_size
    #     })
    cnt = count_ascii(txt)

    if len(txts) == 1:
        res.append({
            'content':txt,
            'pos': [left+(width-font_size*cnt/2)/2, top+(height-font_size)/2],
            # 'pos': [left, top],
            'size': font_size
        })
    else:
        for idx, txt in enumerate(txts):
            res.append({
                'content': txt,
                # 'pos': [left+(width-font_size*cnt/2)/2, top+(height-font_size)/2],
                'pos': [left, top+font_size_min*idx],                
                'size': font_size,            
            })
    return res

def txt_split_mix(txt:str, len_max:int, font_size:int):
    res = list()
    tmp = str()
    cnt = 0

    for letter in txt:
        tmp += letter
        cnt = count_ascii(tmp)*font_size/2
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

def fitting_fs(txt:str, box:list[int], font_size_min=20):
    # w_max, h_max = box[2::]
    # step = 2
    # for size in range(1, font_size_max, 2):
    #     ft = ImageFont.truetype(font_src, size=size)
    #     # w, h = arial.getsize(txt)  # older versions
    #     left, top, right, bottom = ft.getbbox(txt)  # needs PIL 8.0.0
    #     # print(left, top, right, bottom)
    #     w = right - left
    #     h = bottom - top
    #     # print(w, h)

    #     # if w > w_max or h > h_max:
    #     if w > w_max:
    #         break
    cnt = count_ascii(txt)
    width = box[2]
    height = box[3]
    size = min(math.floor(width*2/cnt), height)
    return max(size, font_size_min)

def maker_template(meme):
    flag_success = 0
    if meme in config['surjection']:
        info = config['surjection'][meme]
    else:
        return flag_success, None, None

    if meme_path := search_img(meme, path_src=config['templates_path']):
        # info['src'] = meme_path
        pass
    else:
        return flag_success, None, None

    img = cv2.imread(meme_path)
    for idx, box in enumerate(info['box']):
        left, top, width, height = box[:]
        start_point = (left, top)
        end_point = (left+width, top+height)
        color = (71, 33, 0)
        thickness = 1
        cv2.rectangle(img, start_point, end_point, color, thickness)

        center = (math.floor(left+width/2), math.floor(top+height/2))
        radius = math.floor(0.75*height/2)
        # cv2.circle(img, center=center, radius=radius, color=color, thickness=-1)
        
        text_face = cv2.FONT_HERSHEY_SIMPLEX
        text_scale = radius/25
        txt = str(idx+1)
        thickness = 1
        text_size, _ = cv2.getTextSize(str(idx), text_face, text_scale, thickness)
        # print(text_size)
        text_origin = (math.ceil(center[0]-text_size[0]/2), math.ceil(center[1]+text_size[1]/2))
        cv2.putText(img, text=txt, org=text_origin, color=(71, 33, 0), fontFace=text_face, fontScale=text_scale, thickness=thickness)
    
    cv2.putText(img, text=meme, org=(0, text_size[1]), color=(71, 33, 0), fontFace=text_face, fontScale=text_scale, thickness=thickness)

    is_success, buffer = cv2.imencode(".png", img)
    io_buf = io.BytesIO(buffer)
    flag_success = 1
    # cv2.imwrite(filename='text.png',img=img)
    # plt.imshow(img)
    # return img
    return flag_success, io_buf, img

  

if __name__ == "__main__":
    meme = '表演一下'
    meme = '我无法创造奇迹'
    sentences = ['把心里想的说出来就好', '想不到也没有办法, 我要去吃饭了. ']
    sentences = ['让时间永远停留在2月22号 我无法创造奇迹']
    # sentences = ['12345678123456781234567812345678', '123456789098765432112345678909876543211234567890987654321']
    flag_success, io_buf, img= maker_main(meme, sentences)
    # flag_success, io_buf, img2= maker_template(meme)
    plt.imshow(img)
    # plt.imshow(img2)
    # print(1)