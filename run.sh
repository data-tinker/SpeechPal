#!/bin/bash

# Start the first process
python3 server.py &

# Start the second process
python3 bot.py &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?