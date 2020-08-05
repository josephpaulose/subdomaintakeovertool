#!/bin/bash
chmod +x digger.sh
chmod +x main2.py
if [ -e validUrls.txt ]
then
    rm dig.txt
    rm Takeover.txt
    rm validUrls.txt
    echo previous result removed
else
	echo 
fi
./digger.sh
