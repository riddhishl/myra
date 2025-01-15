#!/bin/sh
# get rid of the cursor
setterm -cursor off
SERVICE='omxplayer'
while true; do
    if ps ax | grep -v grep | grep $SERVICE > /dev/null
    then
        echo "running" # >> /dev/null
    else
        for video in "/home/alpha/Ads"/*
        do
                clear
                omxplayer -o hdmi $video --aspect-mode fill >/dev/null
        done
    fi
done