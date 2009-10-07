#! /bin/bash
for A in `ls`; do ffmpeg -hq -sameq -vcodec mjpeg -an -i $A -s 320x240 -an $A.mov; done;

