#! /bin/bash
for A in `ls *.mpg.avi *.mpeg.avi *.mov.avi *avi.avi`; do transcode -z -k -p /dev/dsp -Z 320x240 -y mov -F jpeg -i $A -o $A.mov ; done;

