#! /bin/bash
for A in `ls *mov`; do  totem-video-thumbnailer $A /var/www/delvj/thumbsvideo/$A.png; done;

