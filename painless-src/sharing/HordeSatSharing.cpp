// -----------------------------------------------------------------------------
// Copyright (C) 2017  Ludovic LE FRIOUX
//
// This file is part of PaInleSS.
//
// PaInleSS is free software: you can redistribute it and/or modify it under the
// terms of the GNU General Public License as published by the Free Software
// Foundation, either version 3 of the License, or (at your option) any later
// version.
//
// This program is distributed in the hope that it will be useful, but WITHOUT
// ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
// FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
// details.
//
// You should have received a copy of the GNU General Public License along with
// this program.  If not, see <http://www.gnu.org/licenses/>.
// -----------------------------------------------------------------------------

#include "../clauses/ClauseManager.h"
#include "../sharing/HordeSatSharing.h"
#include "../solvers/SolverFactory.h"
#include "../utils/Logger.h"
#include "../utils/Parameters.h"
#include "../utils/System.h"

// Adding ClauseHashTable
#include "../clauses/ClauseHashTable.h"

int HordeSatSharing::current_round = 0; // 0.5 --> 120 fois dosharing avant de vider la base
double HordeSatSharing::interval = 180.0; // en secondes 180 = 3 min
double  HordeSatSharing::current_interval = 180.0; // en secondes

HordeSatSharing::HordeSatSharing()
{
   this->literalPerRound = Parameters::getIntParam("shr-lit", 1500);
   this->initPhase = true;
   // number of round corresponding to 5% of the 5000s timeout
   this->roundBeforeIncrease = 250000000 / Parameters::getIntParam("shr-sleep", 500000);
}

HordeSatSharing::~HordeSatSharing()
{
  for (auto pair : this->databases) {
    delete pair.second;
 }
}

void
HordeSatSharing::doSharing(int idSharer, const vector<SolverInterface *> & from,
   const vector<SolverInterface *> & to)
{
   static unsigned int round = 1;
   // vector<ClauseExchange*> cls_to_reduce;
   // vector<ClauseExchange*> cls_to_send;
   for (size_t i = 0; i < from.size(); i++) {
      int used, usedPercent, selectCount;
      int id = from[i]->id;

      if (!this->databases.count(id)) {
        this->databases[id] = new ClauseDatabase();
     }

     tmp.clear();
      // cls_to_reduce.clear();
      // cls_to_send.clear();
     from[i]->getLearnedClauses(tmp);
      //le temps relatif est suppérieur à l'interval
     if( getRelativeTime() < current_interval){
        for(size_t k = 0; k < tmp.size();k++){	      
           stats_doublons.store_time(tmp[k],current_round);
        }
     }
	    // clause before selection //
     for( size_t k = 0; k < tmp.size();k++){
      stats_doublons.store(tmp[k],1);
   }
      //------------------------------------------//
   stats.receivedClauses += tmp.size();

   for (size_t k = 0; k < tmp.size(); k++) {
      this->databases[id]->addClause(tmp[k]);
   }
   tmp.clear();
   used        = this->databases[id]->giveSelection(tmp, literalPerRound, &selectCount);
   usedPercent = (100 * used) / literalPerRound;

      // clauses after selection //
   if( getRelativeTime() < current_interval){
     for(size_t k = 0; k < tmp.size();k++){
       stats_doublons_selected.store_time(tmp[k],current_round);
    }
 }

 for( size_t k = 0; k < tmp.size();k++){
   stats_doublons_selected.store(tmp[k],1);
}

      //------------------------------------------//
stats.sharedClauses += tmp.size();
	   //tmp clauses partagées
if (usedPercent < 75 && !this->initPhase) {
   from[i]->increaseClauseProduction();
   log(2, "Sharer %d production increase for solver %d.\n", idSharer,
     from[i]->id);
} else if (usedPercent > 98) {
   from[i]->decreaseClauseProduction();
   log(2, "Sharer %d production decrease for solver %d.\n", idSharer,
     from[i]->id);
}

if (selectCount > 0) {
   log(2, "Sharer %d filled %d%% of its buffer %.2f\n", idSharer,
     usedPercent, used/(float)selectCount);
   this->initPhase = false;
}
if (round >= this->roundBeforeIncrease) {
   this->initPhase = false;
}

for (size_t j = 0; j < to.size(); j++) {
   if (from[i]->id != to[j]->id) {
      for (size_t k = 0; k < tmp.size(); k++) {
         ClauseManager::increaseClause(tmp[k], 1);
      }
      to[j]->addLearnedClauses(tmp);
   }
}

for (size_t k = 0; k < tmp.size(); k++) {
   ClauseManager::releaseClause(tmp[k]);
}
}
   if(getRelativeTime() > current_interval){ // Log for doublons per time
   	stats_doublons.print_duplicate_time(current_round,"-w_dup_time");
      stats_doublons_selected.print_duplicate_time(current_round,"-w_dup_time_selected");
      current_interval = current_interval + interval;
      current_round++;
   }
   round++;
}

void
HordeSatSharing::print_duplicate(string end_file,string end_file_selected){
   stats_doublons.print_duplicate(end_file); //Before selection
   stats_doublons_selected.print_duplicate(end_file_selected); //After Selection
}

SharingStatistics
HordeSatSharing::getStatistics()
{
   return stats;
}
