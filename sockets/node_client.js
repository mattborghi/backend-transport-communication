var net = require('net'),
    JsonSocket = require('json-socket');

var port = 2000; //The same port that the server is listening on
var host = '127.0.0.1';
var socket = net.Socket();
// var socket = new JsonSocket(new net.Socket()); //Decorate a standard net.Socket with JsonSocket
socket.connect(port, host);
socket.on('connect', function() { //Don't send until we're connected
    socket.sendMessage("hello");
    // socket.sendMessage({x: 5, y: "hello"});
    socket.on('message', function(message) {
        console.log(String(message))
        // console.log('The result is: '+message.x);
        // if(message.y == "bye") {
        //     console.log("byee")
        //     socket.destroy()
        // }
    });
socket.on('close', function() {
    console.log('closed client connection')
})
});
