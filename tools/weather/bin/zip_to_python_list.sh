#!/bin/bash

if [ $# -eq 0 ]
then
   echo "File path to zip code database must be provided."
   exit 1
else
   echo zip_list = [$(bin/zip_extractor.sh $1)]
fi
