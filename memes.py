import cv2
import yaml
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont 
import matplotlib.pyplot as plt
import io

config = yaml.safe_load(open("./configs/memes.yaml", "r"))

def cv2AddChineseText(img, text, position, textColor=(0, 0, 0), textSize=30, font="./data/fonts/simhei.ttf"):
    if (isinstance(img, np.ndarray)):
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    # font style
    fontStyle = ImageFont.truetype(
        font, textSize, encoding="utf-8")
    # put text
    draw.text(position, text, textColor, font=fontStyle)

    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)

def maker(meme, sentences):
    flag_success = 0
    if meme in config['surjection']:
        info = config['surjection'][meme]
    else:
        return flag_success, None

    img = cv2.imread(os.path.join(config['path_meker'], info['src']))
    contents = list()
    if len(sentences) < len(info['pos']):
        sentences = sentences + [" " for _ in range(len(info['pos']) - len(sentences))]
    for idx, itm in enumerate(info['pos']):
        contents.append(
            {
                'content': sentences[idx],
                'pos': itm,
                'size': info['font_size'][idx]
            },
        )
    for content in contents:
        txt = content['content']
        txt_pos = content['pos']
        txt_size = content['size']
        img = cv2AddChineseText(img, text=txt, position=txt_pos, textColor=(0, 0, 0), textSize=txt_size, font="./data/fonts/simhei.ttf")
    is_success, buffer = cv2.imencode(".png", img)
    io_buf = io.BytesIO(buffer)
    flag = 1
    # plt.imshow(img)
    return flag, io_buf

if __name__ == "__main__":
    meme = config['surjection']['表演一下']['src']
    meme = '表演一下'
    sentences = ['忘了我吧', '你我本就不是一路人']
    img = maker(meme, sentences)
    # plt.imshow(img)
    # print(1)