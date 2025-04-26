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

@app.websocket('/ws')
async def sl (websocket: WebSocket):
    await websocket.accept()

    while True:
        data = await websocket.receive_text()
        data = json.loads(data)


        if data['msg'] == 'produce':
            text = data['data'] 

            id = genRanStr(10)
            await websocket.send_text(json.dumps({'msg': 'Video ID', 'data': id}))

            #Preprocess
            sentence = scripts.preprocess(text)

            #Get words
            words = scripts.get_words(sentence)

            #Create images
            for w, i in zip(words, range(len(words))):
                img = scripts.create_img_word(w, 10)   
                os.makedirs(f'builds/{id}', exist_ok=True)
                img.save(f'./builds/{id}/{i}.jpg')

                #Send progress
                await websocket.send_text(json.dumps({'msg': 'Image generation', 'data': f'{i + 1}/{len(words)}'}))

            #Video generation
            scripts.generate_video(id)

            #Remove build folder
            scripts.del_folder(id)

            #Send completion
            await websocket.send_text(json.dumps({'msg': 'Done! File path in {data}', 'data': id}))

            try:
                await websocket.close(1000, 'Terminated')
                break

            except WebSocketDisconnect:
                pass
