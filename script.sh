#!/bin/bash

# Путь к файлу server.py
SERVER_SCRIPT="/home/ec2-user/server.py"
# Порт сервера
PORT=8080

while true; do
    # Поиск в файле server.log по ключевому слову "exit"
    if grep -q "exit" /home/ec2-user/server.log; then
        echo "Detected 'exit' in server.log. Restarting the server..."
        
        # Убить все процессы, связанные с server.py
        pkill -f "python3 $SERVER_SCRIPT"
        
        # Подождать 2 секунды перед повторным запуском
        sleep 2
        
        # Запустить сервер заново
        if sudo lsof -i :$PORT | grep -q "LISTEN"; then
            echo "Port $PORT is in use. Terminating the process..."
        
            # Получаем PID процесса, использующего порт
            PID=$(sudo lsof -t -i :$PORT)
        
            # Завершаем процесс
            sudo kill -9 $PID
        
            echo "Process with PID $PID terminated."
        fi  
        
        sleep 10
        
        # Запустить сервер заново
        /usr/bin/python3 "$SERVER_SCRIPT" &
    fi
    
    # Подождать некоторое время перед следующей проверкой
    sleep 10  # Проверка каждую минуту (можно изменить по желанию)
done
