import requests
from decouple import config
import os
import random
from PIL import Image, ImageDraw, ImageFont
import pandas as pd

PIX_API_KEY = config('PIX_API_KEY')


def get_images(search_term, number_images=20, order='latest', image_type='photo', safesearch='true', min_width='800', min_height='800'):
    r = requests.get(
        f"https://pixabay.com/api/?key={PIX_API_KEY}&q={search_term}&per_page={number_images}&order={order}&image_type={image_type}&safesearch={safesearch}&min_width={min_width}&min_height{min_height}")

    urls = [hit["largeImageURL"] for hit in r.json().get("hits", [])]

    # Pick 2 random images from results
    urls = random.sample(urls, 2)

    image_files = []
    root_dir = os.getcwd()
    for url in urls:
        get_image = requests.get(url)
        if get_image.content is not None:
            f_dir = os.path.join(root_dir, "images")
            if not os.path.isdir(f_dir):
                os.makedirs(f_dir)
            with open(os.path.join(f_dir, os.path.basename(url)), "wb") as f:
                f.write(get_image.content)
            image_files.append(os.path.basename(url))
    return image_files


def resizeCrop(image, max):
    # if image width > height scale image according to max height
    if image.size[0] > image.size[1]:
        maxsize = (image.size[0], max)
        image.thumbnail(maxsize)
        # Setting the middle points for cropped image
        left = int(image.size[0]/2 - max/2)
        upper = 0
        right = left+max
        lower = image.size[1]
        im_crop = image.crop((left, upper, right, lower))
    else:
        maxsize = (max, image.size[1])
        image.thumbnail(maxsize)
        left = 0
        upper = int(image.size[1]/2 - max/2)
        right = image.size[0]
        lower = upper+max
        im_crop = image.crop((left, upper, right, lower))

    return im_crop


def text_wrap(text, font, max_width):
    lines = []
    # if text width is smaller than image width add to list
    if font.getsize(text)[0] <= max_width:
        lines.append(text)
    else:
        # get the words
        words = text.split(' ')
        i = 0
        # add each word to the line while it's shorter than image width
        while i < len(words):
            line = ''
            while i < len(words) and font.getsize(line + words[i])[0] <= max_width:
                line = line + words[i] + " "
                i += 1
            if not line:
                line = words[i]
                i += 1

            # add the line to list of lines
            lines.append(line)
    return lines


def build_image_post():
    searches = ['yoga', 'man', 'woman', 'sun', 'vacation', 'beach', 'people']

    selected_search = random.choice(searches)
    fonts = os.listdir(os.getcwd()+'/fonts')
    selected_font = random.choice(fonts)
    selected_font_size = random.randint(45, 90)
    selected_alpha = random.uniform(0.3, 0.7)

    imglist = get_images(selected_search)

    im1 = Image.open("images/"+imglist[0])
    im2 = Image.open("images/"+imglist[1])

    # find the minimum size from images to set as max image resizing
    if min(im1.size) < min(im2.size):
        max = min(im1.size)
    else:
        max = min(im2.size)

    blended_image = Image.blend(resizeCrop(
        im1, max), resizeCrop(im2, max), alpha=selected_alpha)
    # blended_image.save("images/blended.jpg")

    base = blended_image.convert('RGBA')
    # make a blank image for the text, initialized to transparent text color
    txt = Image.new('RGBA', base.size, (0, 0, 0, 75))

    draw = ImageDraw.Draw(txt)
    # create font object with the font file and size
    font = ImageFont.truetype(
        'fonts/' + selected_font, size=selected_font_size)

    df = pd.read_csv('quotes.csv')
    text = ''
    for ind in df.index:
        if df['Posted'][ind] == 0:
            text = df.at[ind, 'Quote']
            df.at[ind, 'Posted'] = 1
            break

    df.to_csv('quotes.csv', index=False)

    lines = text_wrap(text, font, 0.9*max)
    line_height = font.getsize('hg')[1]

    x = 40
    y = random.randint(10, 135)
    B = random.randint(0, 255)
    f_transparnt = random.randint(65, 200)
    for line in lines:
        # draw text line on image
        draw.text((x, y), line, fill=(255, 255, B, f_transparnt), font=font)

        # update height for next line
        y = y + line_height

    final_image = Image.alpha_composite(base, txt)
    final_image.convert("RGB").save('images/final.jpg')
    return(text)
