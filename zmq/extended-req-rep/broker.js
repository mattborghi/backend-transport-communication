// Simple request-reply broker in Node.js

// var zmq = require('zeromq')
//     , frontend = zmq.socket('router')
//     , backend = zmq.socket('dealer');

// frontend.bindSync('tcp://*:5559');
// backend.bindSync('tcp://*:5560');

// frontend.on('message', function () {
//     // Note that separate message parts come as function arguments.
//     var args = Array.apply(null, arguments);
//     // Pass array of strings/buffers to send multipart messages.
//     backend.send(args);
// });

// backend.on('message', function () {
//     var args = Array.apply(null, arguments);
//     frontend.send(args);
// });

// ---------------------------------------------------
// INSTEAD OF DOING THAT WE CAN USE THE PROXY FUNCTION
// ---------------------------------------------------

//  Simple message queuing broker
//  Same as request-reply broker but using shared queue proxy

var zmq = require('zeromq');

async function run() {

    //  Socket facing clients

    var frontend = new zmq.Router;

    //  Socket facing services
    var backend = new zmq.Dealer;

    //  Start the proxy
    console.log('starting proxy...');
    const proxy = new zmq.Proxy(frontend, backend);

    // Binding
    console.log('binding frontend...');
    await frontend.bind('tcp://*:5559');

    console.log('binding backend...');
    await backend.bind('tcp://*:5560');

    await proxy.run()

    process.on('SIGINT', function () {
        proxy.close()
        frontend.close();
        backend.close();
    });

}

run()