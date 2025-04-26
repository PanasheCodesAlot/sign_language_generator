from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import json
import os

from util import genRanStr
import scripts


def parse_client_msg (data):
    data = json.loads(data)
    return data['state']


app = FastAPI()
app.mount('/videos', StaticFiles(directory='exports'), name='static')

@app.get('/create/{text}')
async def sl (text):
    id = genRanStr(10)

    #Preprocess
    sentence = scripts.preprocess(text)

    #Get words
    words = scripts.get_words(sentence)

    #Create images
    for w, i in zip(words, range(len(words))):
        img = scripts.create_img_word(w, 10)   
        os.makedirs(f'builds/{id}', exist_ok=True)
        img.save(f'./builds/{id}/{i}.jpg')


    #Video generation
    scripts.generate_video(id)

    #Remove build folder
    scripts.del_folder(id)

    #Send completion
    return {'message': 'Complete', 'data': id}
