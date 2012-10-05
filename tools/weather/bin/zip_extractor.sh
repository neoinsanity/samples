#!/bin/bash

if [ $# -eq 0 ] 
then
   echo "File path to zip code database must be provided." 
   exit 1     
else   
   cat $1 | grep -o "^\"[0-9]*\","
fi
