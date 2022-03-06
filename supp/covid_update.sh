#!/bin/bash

cd /home/si9h/COVID-19
sudo git config --global http.proxy http://127.0.0.1:7890
while true
do
	sudo git pull
	sleep 600
done
