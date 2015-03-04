#!/bin/bash

FIRST="http://www.tpmlphelps.com/150218P";
ZEROS="000";
FILETYPE=".htm";

for i in $(seq 1 40); do
	wget $FIRST$(printf '%03d' $i)$FILETYPE
done;
