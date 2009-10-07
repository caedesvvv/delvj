#! /bin/bash
for A in `ls`; do mencoder -oac mp3lame -ovc lavc $A -o $A.avi; done;

