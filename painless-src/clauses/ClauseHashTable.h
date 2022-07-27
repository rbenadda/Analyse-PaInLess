#pragma once
#include <map>
#include <unordered_map>
#include <vector>
#include "ClauseExchange.h"

using namespace std;

struct Data {    
    int replica;
    int size; // taille de la clause
    unordered_map<int,unsigned long> workers; //qui a envoyé la clause et combien de fois 
    unordered_map<int,vector<unsigned long>> lbds; //qui a envoyé le lbd et stocké sous forme de ID | lbds
};


struct Data_time {
    double time;
    int size;
    unordered_map<int,unsigned long> workers;
};

struct Data_lbd {
    double time;
    int size;
    int index = 0;
    /** 
     * This map is used to see lbds send by workers and calcul lbd's difference between the fisrt and the last round
     * Worker<round,lbds>
     */
    map<int,map<int,vector<int>>> lbds_per_round;
};

class ClauseHashTable
{
private:
    /**
     * This map assosiates to a clause (string representation ) the pair (id_worker, cpt)
     * id_worker: The ID of this clause's producer 
     * cpt: the number of time this solver send this clause
     */
     unordered_map<string,Data> clauses_select;
    /**
     * This map assosiates to a clause (string representation) the pair (id_worker, cpt)
     * id_worker: the ID of this clause's producer
     * cpt: the number of time this solver send this clause
     */
    unordered_map<string, Data> clauses;
    /**
     * This map associates to a clause (string representation the pair (id_worker,cpt))
     * id_worker: the ID of this clause's producer
     * cpt: the number of time this solver send this clause
     * It will be use to calculate the percentage of doublons each X period
     */
    unordered_map<string,Data_time> clauses_time;
    /**
     *
     */
    unordered_map<string,Data_lbd> clauses_lbd;
    /**
     * This map associates to a clause the number of times the reducer
     * has produced it.
     */
    unordered_map<string, unsigned long> reductions;
    /** this map associates to a literal the number of time a worker has produce this
     * literal
     */
    unordered_map<int,map<int,unsigned long>> variables;
    /** this map associates to a literal the number of time a worker has produce this
     * literal
     */
    unordered_map<int,map<int,unsigned long>> variables_doublons;
    string logPath;
public:
    ClauseHashTable();
    ~ClauseHashTable() {}

    int store(ClauseExchange* c, int round);
    void print_duplicate(string end_file);

    void store_time(ClauseExchange* c,unsigned int round);
    void print_duplicate_time(unsigned int round,string end_file);
};
