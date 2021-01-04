#!/bin/bash

## There is no particular order for running the files this is ZeroMQ 👍

# Worker
gnome-terminal --tab --title="Worker" -- bash -c "node worker.js"

# Client
gnome-terminal --tab --title="Client" -- bash -c "node client.js"

# Broker
gnome-terminal --tab --title="Broker" -- bash -c "node broker.js"
