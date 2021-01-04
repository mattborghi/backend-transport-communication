// Hello World server in Node.js
// Connects REP socket to tcp://*:5560
// Expects "Hello" from client, replies with "World"

var zmq = require('zeromq')

async function run() {
    const responder = new zmq.Reply
    const PORT = 5560
    await responder.connect(`tcp://127.0.0.1:${[PORT]}`)

    for await (const [msg] of responder) {
        console.log('received request:', msg.toString());
        await responder.send("world")
    }
}

run()
