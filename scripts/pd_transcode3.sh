#! /bin/bash
for A in `ls *`; do mencoder -vf scale=320:240 -nosound  -oac copy  -ovc lavc -lavcopts vcodec=mjpeg:mbd=1 -of lavf -lavfopts format=mov -o $A.mov $A ; done;

