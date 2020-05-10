const WebSocket = require('ws');

const ws = new WebSocket('ws://localhost:8080',{
  perMessageDeflate: false
});

ws.on('open', function open() {
  ws.send('something');
});

ws.on('message', function incoming(data) {
  console.log(data);
  ws.close();
});

ws.on('error', function incoming(error) {
  console.log(error);
});

ws.on('close', function close() {
  console.log('disconnected');
});
