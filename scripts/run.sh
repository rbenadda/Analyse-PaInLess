#! /bin/bash

> ../scripts/out/$4

Namefile=(w_dup w_dup_selected)
NamefileTime=(w_dup_time_selected w_dup_time)
ls $1|while read -r
do
	../painless-mcomsps -c=$2 -t=$3 $1/$REPLY >> ../scripts/out/$4
	echo "Adding CSV Format"
	cd ../logs 
	for name in ${Namefile[*]}; 
	do
	if [ -f "$REPLY-$name" ]
	then
		sed -i '1 i\key,ID,size,ID_worker,lbd,cpt,nb_clauses,nb_doublons,nb_doublons_pair,nb_doublons_impair,nb_reduction,nb_reduction_self,nb_reduction_original,nb_reduction_workers,nb_reduction_workers_total' $REPLY-$name
	else
		echo "Cannot proceed"
	fi
	done
	for name in ${NamefileTime[*]}; 
	do
	if [ -f "$REPLY-$name" ]
	then
		sed -i '1 i\key,ID,round,ID_clause,ID_worker,nb_doublons,nb_clauses,cpt,size,lbd' $REPLY-$name
	else
		echo "Cannot proceed"
	fi
	done
	echo "Done adding"
done

echo "DONE"

