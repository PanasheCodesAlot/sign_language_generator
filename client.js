import WebSocket from 'ws'

const ws = new WebSocket('ws://sign-language-generator.onrender.com:8000')

ws.on('open', () => {
    console.log('Connection started')

    ws.send(JSON.stringify({'msg': 'produce', 'data': 'Hey my name is Panashe Jere'}))
})
ws.on('error', (e) => console.log(`Connection disconnected: ${e.message}`))

ws.on('message', m => {
    console.log(m.toString())
})
