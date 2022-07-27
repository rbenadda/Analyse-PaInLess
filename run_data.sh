#! /bin/bash

> $4

ls $1|while read -r
do
	./painless-mcomsps -c=$2 -t=$3 $1/$REPLY >> ./logs/$4
	echo "Done"
done


