#! /bin/bash

ls $1|while read -r
do
	sed -i '1s/^/key,/' $1/$REPLY 
done