#!/bin/bash
python main2.py -l subdomains
input="/root/Documents/subdomaintakeovertool/subdomains"
while IFS= read -r line
do
   echo "$line"
   dig $line >>dig.txt 
done < "$input"
  
