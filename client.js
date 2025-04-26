import WebSocket from 'ws'

const ws = new WebSocket('ws://127.0.0.1:8000/ws')

ws.on('open', () => {
    console.log('Connection started')

    ws.send(JSON.stringify({'msg': 'produce', 'data': 'Hey my name is Panashe Jere'}))
})
ws.on('error', () => console.log(`Connection disconnected: ${e.message}`))

ws.on('message', m => {
    console.log(m.toString())
})
