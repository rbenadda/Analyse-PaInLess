#! /bin/bash

> ../logs/out/$4

namefile=(w_dup w_dup_selected w_dup_time_selected w_dup_time)

ls $1|while read -r
do
	../painless-mcomsps -c=$2 -t=$3 $1/$REPLY >> ../logs/out/$4
	echo "adding CSV Format"
	cd ../logs 

	for name in ${namefile[*]}; 
	do
	if [ -f "$REPLY-$name" ]
	then
		sed -i '1 i\ID,size,ID_worker,lbd,cpt,nb_clauses,nb_doublons,nb_doublons_pair,nb_doublons_impair,nb_reduction,nb_reduction_self,nb_reduction_original,nb_reduction_workers,nb_reduction_workers_total' $REPLY-$name
	else
		echo "cannot proceed"
	fi
	done
	echo "Done adding"
done

echo "DONE"

