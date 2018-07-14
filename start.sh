#!/bin/bash
net start mysql
start ../nginx/nginx
nohup python bin/start.py &
