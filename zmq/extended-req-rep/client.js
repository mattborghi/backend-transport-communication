// Hello World client in Node.js
// Connects REQ socket to tcp://localhost:5559
// Sends "Hello" to server, expects "World" back

var zmq = require('zeromq')

async function run() {
    const sock = new zmq.Request

    const PORT = 5559
    sock.connect(`tcp://localhost:${PORT}`)
    console.log(`Producer bound to port ${PORT}`)

    for (var i = 0; i < 10; ++i) {
        await sock.send("Hello");

        const [result] = await sock.receive()

        console.log(result.toString())
    }
}

run()
