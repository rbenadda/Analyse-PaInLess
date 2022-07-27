#! /bin/bash

ls $1|while read -r
do
	unxz $1/$REPLY   
done


