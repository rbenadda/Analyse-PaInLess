#! /bin/bash

ls $1|while read -r
do
	if [[ -f $1/$REPLY ]]
	then
		if ! grep "key" $1/$REPLY
		then
			echo "Adding"
			sed -i '1s/^/key,/' $1/$REPLY 
		fi
	fi
done