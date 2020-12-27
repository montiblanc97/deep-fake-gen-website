#!/bin/bash

ffmpeg -y -i $1.mp4 -filter:v fps=15,scale=640:480,crop=3*in_h/4:3*in_h/4:in_w/2-3*in_h/8:in_h/8 $1_square.mp4

#ffmpeg -i $1.webm -vf "scale=640:480,crop=3*in_h/4:3*in_h/4:in_w/2-3*in_h/8:0,select=eq(n\,0)" -q:v 3 $1.jpg