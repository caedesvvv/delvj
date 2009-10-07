#! /bin/bash
for A in `ls *`; do transcode -x mplayer -n null -y mov -F jpeg -Z 320x240 -i "$A" -o "$A".mov ; done;

