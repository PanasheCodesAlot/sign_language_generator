from PIL import Image
import os
from moviepy import ImageSequenceClip
import math
import random
import shutil

#Get sentence
#Preprocess
#Get word
#Get length
#Get square root
#Divide by width to get the width of each word image
#Scale by height: (r / (height + 200)) * img_height
#Arrange
#Write the word text at the bottom:
#   Font = 100 / r
#Do this with all images
#Merge clip with 5s fps
#Save clip

def preprocess (sentence):
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 '
    collected = ''

    for i in sentence:
        if i in characters:
            collected += i

    return collected

def get_words (sentence):
    return sentence.split(' ')

def find_height (sentence):
    words = get_words(sentence)
    found = 0

    for word in words:
        length = len(word)

        if length > found:
            found = length
    
    return found

def get_img_word (w):
    w = w.lower()

    path = f'./dataset/{w}'
    imgs = os.listdir(path)

    img = random.choice(imgs)
    path += f'/{img}'

    return path

def create_img_word (word, height):
    word = word.upper()
    #Dimensions
    x = 1080
    y = 1920

    #For each letter image
    l_xy = 400

    #Equaliser
    r = math.sqrt(len(word))
    r = int(r)

    if r < 2:
        r = 2

    #Find size of the each image
    row_size = x / r

    #Find scale factor
    scale_factor = row_size / l_xy

    #New row size
    row_size = l_xy * scale_factor
    row_size = round(row_size)


    #Positions and images
    pos = [0, 0]
    img = Image.new('RGB', (x, y), '#000000')

    for w in word:
        path = get_img_word(w)
        l_img = Image.open(path)
        l_img = l_img.resize((row_size, row_size))

        #Paste
        img.paste(l_img, tuple(pos))

        pos[0] += row_size

        if pos[0] >= x:
            pos[1] += row_size
            pos[0] = 0

    return img
        

def generate_video(id):
    path = f'./builds/{id}/'
    imgs = [path + img for img in os.listdir(path)]
    imgs.sort()

    clip = ImageSequenceClip(imgs, fps=0.1)
    clip.write_videofile(f'./exports/{id}.mp4', codec='libx264')


def del_folder (id):
    path = f'./builds/{id}'
    shutil.rmtree(path)
