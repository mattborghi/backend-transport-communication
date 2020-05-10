// subber.js
var zmq = require("zeromq"),
  sock = zmq.socket("sub");

sock.connect("tcp://127.0.0.1:3000");
sock.subscribe("kitty cats");
console.log("Subscriber connected to port 3000");

sock.on("message", function(topic, message) {
  console.log(
    "received a message related to:",
    topic.toString(),
    "containing message:",
    message.toString()
  );
});


// Another subber in dogs channel
var sock2 = zmq.socket("sub");

sock2.connect("tcp://127.0.0.1:3000");
sock2.subscribe("puppy dogs");
// console.log("Subscriber connected to port 3000");

sock2.on("message", function(topic, message) {
  console.log(
    "received a message related to:",
    topic.toString(),
    "containing message:",
    message.toString()
  );
  sock2.close()
});

sock2.on("close", function() {
  console.log("bye Julia from dogs") // IDK why this is not being called
})

sock2.on("error", function(err) {
  console.log("An error happened: ", err)
})