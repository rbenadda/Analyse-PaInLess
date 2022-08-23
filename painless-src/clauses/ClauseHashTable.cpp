#include "../clauses/ClauseHashTable.h"
#include <algorithm>
#include <stdio.h>
#include "../utils/System.h"
#include "../utils/Parameters.h"

using namespace std;

int index_clause = 0;

ClauseHashTable::ClauseHashTable() {
    ///data/rbenadda/painless-sat-competition-2022/painless/dimacs_logs_after
    string path = "/data/rbenadda/painless-sat-competition-2022/painless/logs";
    logPath = Parameters::getParam("log",path);
    string name(Parameters::getFilename());
    name = name.substr(name.find_last_of("/") + 1);
    logPath += "/" + name;
}

int ClauseHashTable::store(ClauseExchange* c, int round) {
    string cls;
    int res = 1;
    int reducer_id = Parameters::getIntParam("c", 30) + 1;
    // The clause is represented by a string, the literals are sorted
    // to ensure uniqueness
    std::vector<int> tmp(c->lits, c->lits + c->size);
    sort(tmp.begin(),tmp.end());
    for (int lit : tmp) {
       cls += std::to_string(lit);
   }
    // If the clause come from a regular solver (not the Reducer),
    // increase the ref counter in 'clauses'
    if (c->from < reducer_id) {
        auto it_solver = clauses[cls].workers.find(c->from);
            // Ajout du lbd de la clause
        clauses[cls].lbds[c->from].push_back(c->lbd);

        clauses[cls].replica = 0;
        for(auto& it_cpt: clauses[cls].lbds){
            clauses[cls].replica = clauses[cls].replica + it_cpt.second.size();
        }

        if (it_solver != clauses[cls].workers.end()) {
            clauses[cls].workers[c->from]++;
        } else {
                //Ajout de la taille 
            clauses[cls].size = (c->size);
            clauses[cls].workers[c->from] = 1;
        }
        
        for(size_t i = 0; i < c->size; ++i){
            auto it_lits = variables[c->lits[i]].find(c->from);
            if(it_lits != variables[c->lits[i]].end()){
                variables[c->lits[i]][c->from]++;                    
            }
            else{
                variables[c->lits[i]][c->from] = 1;
            }
    }
    // Else, increases the ref counter in reduction
    } else if (c->from == reducer_id) {
        auto it_cls = reductions.find(cls);
        if (it_cls != reductions.end()) {
            reductions[cls]++;
        } else {
            reductions[cls] = 1;
        }
}
return res;
}

void ClauseHashTable::store_time(ClauseExchange* c,unsigned int round){
    string cls;
    int reducer_id = Parameters::getIntParam("c", 30) + 1;
    // The clause is represented by a string, the literals are sorted
    // to ensure uniqueness
    std::vector<int> tmp(c->lits, c->lits + c->size);
    sort(tmp.begin(),tmp.end());
    for (int lit : tmp) {
       cls += std::to_string(lit);
    }
    if (c->from < reducer_id) {
       auto it_solver = clauses_time[cls].workers.find(c->from);
       if (it_solver != clauses_time[cls].workers.end()) {
       		clauses_time[cls].workers[c->from]++;
    	} else {
		    // Ajout du temps relatif à la première fois qu'elle apparaît dans le rounds
		    clauses_time[cls].time = 0; 
          	// Ajout de la taille
        	clauses_time[cls].size = (c->size);
		    // Ajout du premier worker
        	clauses_time[cls].workers[c->from] = 1;
    	}
        clauses_lbd[cls].lbds_per_round[c->from][round].push_back(c->lbd);
        if(clauses_lbd[cls].index == 0 ){
            clauses_lbd[cls].index = index_clause;
            clauses_lbd[cls].size = (c->size);
            index_clause++;
        }
    }
}

void ClauseHashTable::print_duplicate_time(unsigned int round,string end_file){
 FILE* file = fopen(string(logPath + end_file).c_str(), "a"); //-w_dup_time
    if (!file) {
        perror("print_duplicate_time");
        exit(EXIT_FAILURE);
    }

    // Permet de compter le nombre de clauses envoyer par un worker
    map<int, unsigned long> nb_clauses_by_w;

    // Permet de compter le nombre de doublons venant d'un worker
    map<int, unsigned long> nb_doublons_self_by_w;

    // Permet de créer un histogramme des nombres de doublons
    // (est-ce que les clauses ont tendance à être dupliquées 2,3,4..,n fois)
    map<unsigned int, unsigned long> distrib_nb_doublons;

    // Permet de créer un histogramme des workers à l'origine des réplicas
    // (est-ce que les doublons viennent de tous les workers ou certains en particuliers)
    map<unsigned int, unsigned long> distrib_over_workers;

    // Global
    unsigned long nb_doublons = 0;
    unsigned long nb_clause = 0;
    unsigned long nb_lbd = 1;
    bool first = true;
    vector<int> tmp;

    for (auto& it_cls : clauses_time) {
	    int tmp_nb_doublons_clause = -1;
        // For each worker that shared clauses{its_cls}
        for (auto& it_solver: it_cls.second.workers) {
            // nb_clauses_by{worker}: increment the number of clauses send by this worker
            if(nb_clauses_by_w.find(it_solver.first) != nb_clauses_by_w.end()) {
                nb_clauses_by_w[it_solver.first] += it_solver.second;
            } else {
                nb_clauses_by_w[it_solver.first] = it_solver.second;
            }
            // tmp_nb_doublons_clause
            tmp_nb_doublons_clause += it_solver.second;
            
            // nb_doublons_self: increment the number of replicas send by this worker
            if(nb_doublons_self_by_w.find(it_solver.first) != nb_doublons_self_by_w.end()) {
                nb_doublons_self_by_w[it_solver.first] += it_solver.second - 1;
            } else {
                nb_doublons_self_by_w[it_solver.first] = it_solver.second - 1;
            }
        }

        for(auto& it_solver: it_cls.second.workers){
                if(it_solver.second != 0 ){
                    tmp.push_back(it_solver.first);
                }
            }
        tmp.clear();

        // nb_doublons
        nb_doublons += tmp_nb_doublons_clause;
        // distrib_over_doublons
        if (distrib_nb_doublons.find(tmp_nb_doublons_clause) != distrib_nb_doublons.end()) {
            distrib_nb_doublons[tmp_nb_doublons_clause]++;
        } else {
            distrib_nb_doublons[tmp_nb_doublons_clause] = 1;

        }
        // distrib_over_workers
        int nb_workers = it_cls.second.workers.size();
        if (distrib_over_workers.find(nb_workers) != distrib_over_workers.end()) {
            distrib_over_workers[nb_workers]++;
        } else {
            distrib_over_workers[nb_workers] = 1;
        }
    }

    for (auto& it_cls : clauses_lbd) {
        for(auto& it_wkr : it_cls.second.lbds_per_round){ // Pour chacun des workers
            for (auto it_vec = it_wkr.second[round].begin();it_vec != it_wkr.second[round].end();it_vec++){
                nb_lbd++;       
            }
        }

        if(nb_lbd > 1){
            for(auto& it_wkr : it_cls.second.lbds_per_round){ // Pour chacun des workers
                for (auto it_vec = it_wkr.second[round].begin();it_vec != it_wkr.second[round].end();it_vec++){
                        fprintf(file,"lbdot,%ld,%ld,%d,NULL,NULL,%ld,%d,%d\n",round,it_cls.second.index,it_wkr.first,nb_lbd,it_cls.second.size,*it_vec);
                }                  
            }
        }
        nb_lbd = 0;
    }
        fprintf(file, "tot,%d,NULL,NULL%lu,%lu,NULL,NULL,NULL\n",round, nb_doublons, clauses_time.size());
    	for (auto& it_solver: nb_clauses_by_w) {
        	fprintf(file, "wot,%d,NULL,%d,%lu,%lu,NULL,NULL,NULL\n",round, it_solver.first, nb_doublons_self_by_w[it_solver.first], it_solver.second);
	    }
    	for (auto& it_solver: distrib_over_workers) {
        	fprintf(file, "dwot,%d,NULL,NULL,%d,%lu,NULL,NULL,NULL\n",round, it_solver.first, it_solver.second);
    	}
    	for (auto& it_solver: distrib_nb_doublons) {
        	fprintf(file, "ddot,%d,NULL,NULL,%d,%lu,NULL,NULL,NULL\n",round, it_solver.first, it_solver.second);
    	}

    fclose(file);
    clauses_time.clear();
}

void ClauseHashTable::print_duplicate(string end_file) {
    /***
     * w  : id_worker,nombre_de_cls,nombre_de_replica
     * dw : nombre de workers, nombre de clauses
     * dd : nombre de doublons, nombre de clauses
     * r  : nb_reduction,nb_reduction_doublon_self,nb_reductions_originals,nb_de_doublons_avec_w,nombre_de_doublons_W_total
     * rdd: nombre de doublons, nombre de clauses
     */
    FILE* file = fopen(string(logPath + end_file).c_str(), "w");
    if (!file) {
        perror("print_duplicate");
        exit(EXIT_FAILURE);
    }
    // Local to a worker/clause

    // Permet de compter le nombre de clauses envoyer par un worker
    map<int, unsigned long> nb_clauses_by_w;

    // Permet de compter le nombre de doublons venant d'un worker
    map<int, unsigned long> nb_doublons_self_by_w;

    // Permet de créer un histogramme des nombres de doublons
    // (est-ce que les clauses ont tendance à être dupliquées 2,3,4..,n fois)
    map<unsigned int, unsigned long> distrib_nb_doublons;

    // Permet de créer un histogramme des workers à l'origine des réplicas
    // (est-ce que les doublons viennent de tous les workers ou certains en particuliers)
    map<unsigned int, unsigned long> distrib_over_workers;

    // Permet de créer un histogramme des lbd des clauses venant d'un worker
    map<unsigned int,unsigned long> nb_lbd_clauses;

    // Permet de créer un histogramme des tailles de clauses en doublons
    map<unsigned int,vector<unsigned long>> nb_size_doublons;

    // Permet de créer un histogramme des lbd de cluases en doublons
    map<unsigned int,vector<unsigned long>> nb_lbd_doublons;
    // Permiet de créer un histogramme des doublons envoyé par chaque worker
    map<int,vector<unsigned long>> worker_doublons;
    // Global
    unsigned long nb_doublons = 0;
    unsigned long nb_clause = 0;
    vector<int> tmp;
    // pair-impair
    unsigned int nb_pair = 0;
    unsigned int nb_impair = 0;
    unsigned int nb_global = 0;
    for (auto& it_cls : clauses) {
        // tmp_nb_doublons_clause: count the number of replicas for this clause
        int tmp_nb_doublons_clause = -1;
        // For each worker that shared clauses{its_cls}
        for (auto& it_solver: it_cls.second.workers) {
            // nb_clauses_by{worker}: increment the number of clauses send by this worker
            if(nb_clauses_by_w.find(it_solver.first) != nb_clauses_by_w.end()) {
                nb_clauses_by_w[it_solver.first] += it_solver.second;
            } else {
                nb_clauses_by_w[it_solver.first] = it_solver.second;
            }
            // tmp_nb_doublons_clause
            tmp_nb_doublons_clause += it_solver.second;
            // nb_doublons_self: increment the number of replicas send by this worker
            if(nb_doublons_self_by_w.find(it_solver.first) != nb_doublons_self_by_w.end()) {
                nb_doublons_self_by_w[it_solver.first] += it_solver.second - 1;
            } else {
                nb_doublons_self_by_w[it_solver.first] = it_solver.second - 1;
            }
        }

        for(auto& it_solver: it_cls.second.workers){
            if(it_solver.second != 0 ){
                tmp.push_back(it_solver.first);
            }
        }

	/* si c'est un doulon */
	if(tmp.size() > 1){
		bool global_pair = false;
		bool global_impair = false;		
		for(auto& it_solver : it_cls.second.workers){
			if((it_solver.first & 1 && it_solver.second != 0)){
                                global_impair = true;
                        }
                        /* si je suis pair et que j'ai envoyé cette clause */
                        if((it_solver.first & 1) == 0 && it_solver.second != 0){
                                global_pair = true;
                        }
		}
		/* Doublons entre LRB et VSIDS */
		if( global_pair == true && global_impair == true){
			nb_global++;
		}else{
			/* Comparaison pair-impair */
			unsigned int pair = 0;
			unsigned int impair = 0;
			for(auto& it_solver: it_cls.second.workers){
				/* si je suis impair et que j'ai envoyé cette clause */
				if((it_solver.first & 1 && it_solver.second != 0)){
					impair++;
				}
				/* si je suis pair et que j'ai envoyé cette clause */
				if((it_solver.first & 1) == 0 && it_solver.second != 0){
					pair++;
				}
			}

			if(pair > 1){nb_pair++;}
			if(impair > 1){nb_impair++;}
		}
	}

        tmp.clear();
        // nb_doublons
        nb_doublons += tmp_nb_doublons_clause;
        // distrib_over_doublons
        if (distrib_nb_doublons.find(tmp_nb_doublons_clause) != distrib_nb_doublons.end()) {
            distrib_nb_doublons[tmp_nb_doublons_clause]++;
        } else {
            distrib_nb_doublons[tmp_nb_doublons_clause] = 1;

        }
        // distrib_over_workers
        int nb_workers = it_cls.second.workers.size();
        if (distrib_over_workers.find(nb_workers) != distrib_over_workers.end()) {
            distrib_over_workers[nb_workers]++;
        } else {
            distrib_over_workers[nb_workers] = 1;
        }
        // PARTIE AJOUTEE
        //size_doublons
        if(it_cls.second.lbds.size() > 1 ){
            // clause doublons | respectivement id_worker, size et les lbds
            //* fprintf(file,"cd,%ld,%d",nb_clause,it_cls.second.size);
            for (auto it_lbd = it_cls.second.lbds.begin(); it_lbd != it_cls.second.lbds.end(); it_lbd++){
                for (auto it_vec = it_lbd->second.begin();it_vec != it_lbd->second.end();it_vec++){
                    fprintf(file,"cd,%ld,%d,%d,%ld,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL\n",nb_clause,it_cls.second.size,it_lbd->first,*it_vec); // worker/lbd     
                }
            }
            nb_clause++;
        }
    // Pour toutes les clauses 
        //* fprintf(file,"cg,%ld,%d",nb_clause,it_cls.second.size); // clauses globales
        for (auto it_lbd = it_cls.second.lbds.begin(); it_lbd != it_cls.second.lbds.end(); it_lbd++){
                for (auto it_vec = it_lbd->second.begin();it_vec != it_lbd->second.end();it_vec++){
                    fprintf(file,"cg,%ld,%d,%d,%ld,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL\n",nb_clause,it_cls.second.size,it_lbd->first,*it_vec); //ajoute les lbd de chaque clause       
                }
            }
        nb_clause++;
    }
    fprintf(file, "t,NULL,NULL,NULL,NULL,NULL,%lu,%lu,%lu,NULL,NULL,NULL,NULL,NULL,NULL\n", clauses.size(), nb_doublons, reductions.size());
    fprintf(file, "gd,NULL,NULL,NULL,NULL,NULL,NULL,%d,NULL,%d,%d,NULL,NULL,NULL,NULL\n", nb_global,nb_pair,nb_impair);
    for (auto& it_solver: nb_clauses_by_w) {
        fprintf(file, "w,%d,NULL,NULL,NULL,NULL,%lu,%lu,NULL,NULL,NULL,NULL,NULL,NULL,NULL\n", it_solver.first, nb_doublons_self_by_w[it_solver.first], it_solver.second);
    }
    for (auto& it_solver: distrib_over_workers) {
        fprintf(file, "dw,NULL,NULL,NULL,NULL,%d,NULL,%lu,NULL,NULL,NULL,NULL,NULL,NULL,NULL\n", it_solver.second, it_solver.first);
    }
    for (auto& it_solver: distrib_nb_doublons) {
        fprintf(file, "dd,NULL,NULL,NULL,NULL,%d,NULL,%lu,NULL,NULL,NULL,NULL,NULL,NULL,NULL\n", it_solver.first, it_solver.second);
    }

    for (auto& it_lits: variables){
        for( auto& it_wkrs : it_lits.second){
            fprintf(file, "lit,%d,NULL,%d,NULL,%lu,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL\n",it_lits.first, it_wkrs.first, it_wkrs.second);
        }
    }


unsigned long nb_reduction = 0;
unsigned long nb_reduction_originals = 0;
unsigned long nb_reduction_self_doublon = 0;
unsigned long nb_reduction_doublon_avec_w = 0;
unsigned long nb_reduction_doublon_avec_w_total = 0;
map<unsigned int, unsigned long> distrib_nb_doublons_reductions;
nb_doublons = 0;

for (auto& it_cls: reductions) {
    nb_reduction += it_cls.second;
    nb_reduction_self_doublon += it_cls.second - 1;
    if (clauses.find(it_cls.first) == clauses.end()) {
        nb_reduction_originals++;
    } else {
        nb_reduction_doublon_avec_w++;
        nb_reduction_doublon_avec_w_total += it_cls.second;
    }
    nb_doublons += it_cls.second - 1;
    if (distrib_nb_doublons_reductions.find(it_cls.second - 1) != distrib_nb_doublons_reductions.end()) {
        distrib_nb_doublons_reductions[it_cls.second - 1]++;
    } else {
        distrib_nb_doublons_reductions[it_cls.second - 1] = 1;
    }
}
fprintf(file,"r,NULL,NULL,NULL,NULL,NULL,NULL,%lu,%lu,NULL,NULL,%lu,%lu,%lu,%lu\n", nb_doublons, nb_reduction, nb_reduction_self_doublon, nb_reduction_originals, nb_reduction_doublon_avec_w, nb_reduction_doublon_avec_w_total);
for (auto& it_solver: distrib_nb_doublons_reductions) {
    fprintf(file, "rdd,NULL,NULL,NULL,NULL,NULL,NULL,%d,%lu,NULL,NULL,NULL,NULL,NULL,NULL\n",  it_solver.second,it_solver.first);
}
fclose(file);
}

/*double ClauseHashTable::ratio_clauses_duplicate() {
    print_duplicate();
    return 0;
}*/
