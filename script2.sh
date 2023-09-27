#!/bin/bash

SERVER_SCRIPT="/home/ec2-user/server.py"
PORT=8080

while true; do
    if grep -q "exit" /home/ec2-user/server.log; then
        echo "Detected 'exit' in server.log. Restarting the server..."
        
        pkill -f "python3 $SERVER_SCRIPT"
        
        sleep 2
        
        if sudo lsof -i :$PORT | grep -q "LISTEN"; then
            echo "Port $PORT is in use. Terminating the process..."
        
            PID=$(sudo lsof -t -i :$PORT)
        
            sudo kill -9 $PID
        
            echo "Process with PID $PID terminated."
        fi  
        
        sleep 10
        
        /usr/bin/python3 "$SERVER_SCRIPT" &
    fi
    
    if ! pgrep -f "python3 $SERVER_SCRIPT" >/dev/null; then
        echo "Server is not running. Restarting the server..."
        
        sleep 2
        
        /usr/bin/python3 "$SERVER_SCRIPT" &
    fi
    
    sleep 10
done
