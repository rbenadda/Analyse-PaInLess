import sys
from statistics import mean
import warnings
import function as func
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt



warnings.filterwarnings('ignore')

max_size = 0

#Global
files = []
file_name = []
vide = []
order = 0
workers = 0
# percentage_doublons 
tab_workers_data_pair = []
tab_workers_data_impair = []
tab_total_doublons = []
tab_total_clauses = []
tab_gd = []
#size_doublons
tab_size_doublons = []
#lbd_doublons
tab_size_lbd_doublons_pair = []
tab_size_lbd_doublons_impair = []
#time_doublons
time_doublons = []
tab_lbd_pair = []
tab_lbd_impair = []
#doublons_many 
tab_doublons_many = []
#doublons_many_size/doublons_many_lbd
tab_doublons_many_size_lbd = []
#nb_doublon_round
tab_doublons_round = []
#nb_replica_lbd
tab_replica_lbd_pair = []
tab_replica_lbd_impair = []
#lbd_global:
tab_lbd_global_pair = []
tab_lbd_global_impair = []
tab_lbd_pair_doublons_global = []
tab_lbd_impair_doublons_global = []
tab_size_doublons_global = []
#variable:
tab_variable = []
def read_file(files):
        print("En train de lire les fichiers")
        for file in files:
                tmp_file = []
                tmp_time = []
                tmp_doublons = []
                tmp_lbd_pair = []
                tmp_lbd_impair = []
                tmp_size_doublons = []
                tmp_size_doublons_global = []
                tmp_doublons_many = []
                tmp_doublons_round = []
                tmp_lbd_global_pair = []
                tmp_replica_lbd_pair = []
                tmp_lbd_global_impair = []
                tmp_workers_data_pair = []
                tmp_doublons_size_lbd = []
                tmp_replica_lbd_impair = []
                tmp_workers_data_impair = []
                tmp_size_lbd_doublons_pair = []
                tmp_size_lbd_doublons_impair = []
                tmp_lbd_doublons_global_pair = []
                tmp_lbd_doublons_global_impair = []
                tmp_variable = []
                with open(sys.argv[1:][0] + "/" +file) as data:
                        for line in data.readlines():
                                x = line.split(",")
                                if(x[0] == "t"):
                                        order = x[2]
                                        doublons = x[1]
                                        tmp_file.append(int(order))
                                        tmp_file.append(file)
                                        tmp_workers_data_pair.append(int(order))
                                        tmp_workers_data_impair.append(int(order))

                file_name.append(tmp_file)
                last_index = -1
                name = None
                somme = 0
                with open(sys.argv[1:][0] + "/" +file) as data:
                        for line in data.readlines():
                                x = line.split(",")
                                tmp = []
                                if(x[0] == "w"):
                                        #tmp.append(int(order))
                                        #tmp.append(int(x[1]))
                                        tmp.append(int(x[2]))
                                        tmp.append(int(x[3])) #self doublons | clauses qui ont été vu mais oublié et on retombe sur le problème
                                        if int(x[1])%2:
                                                tmp_workers_data_pair.append(tmp)
                                        else:
                                                tmp_workers_data_impair.append(tmp)
                                        func.add_worker(workers)
                                elif(x[0] == "t"):
                                        tmp.append(int(x[1]))
                                        tmp.append(int(x[2]))
                                        tmp.append(int(x[3]))
                                        tab_total_clauses.append(tmp)
                                        tab_total_doublons.append(x[2])
                                elif(x[0] == "dw"):
                                        pass
                                elif(x[0] == "dd"):
                                        tmp.append(int(x[1]))
                                        tmp.append(int(x[2]))
                                        tmp_doublons_many.append(tmp)
                                elif(x[0] == "gdw"):
                                        tmp.append(int(order))
                                        tmp.append(int(x[1])) #id worker
                                        tmp.append(int(x[2])) #number of doublons shared with other workers
                                        tmp_doublons.append(tmp)
                                elif(x[0] == "gd"):
                                        tmp.append(int(order))
                                        tmp.append(int(x[1]))
                                        tmp.append(int(x[2]))
                                        tmp.append(int(x[3]))
                                        tab_gd.append(tmp)
                                elif(x[0] == "r"):
                                        data.close()
                                elif(x[0] == "tot"):
                                        tmp.append(int(x[1])); #round - time
                                        tmp.append(int(x[2])); # nb_doublons 
                                        tmp.append(int(x[3])); # nb_clause 
                                        tmp.append(file)
                                        tmp_time.append(tmp)
                                elif(x[0] == "dwot"):
                                        pass
                                elif(x[0] == "ddot"):
                                        pass
                                elif(x[0] == "cd" ): #clause avec size, id_worker et lbd
                                        tmp3 = []
                                        k = line.split(";")
                                        size = k[0].split(",")
                                        if len(size) > 2:
                                                tmp_size_doublons.append(int(size[2]))
                                                cpt = 0
                                                for j in k[1:]:
                                                        cpt = cpt + 1
                                                        tmp2 = []
                                                        tmp3.append(int(j[2:]))
                                                        if(int(j[0])%2): #pair
                                                                tmp_lbd_pair.append(int(j[2:]))
                                                                tmp2.append(int(size[2]))
                                                                tmp2.append(int(j[2:]))
                                                                tmp_size_lbd_doublons_pair.append(tmp2)
                                                                tmp_replica_lbd_pair.append(int(j[2:]))
                                                        else:
                                                                tmp_lbd_impair.append(int(j[2:]))
                                                                tmp2.append(int(size[2]))
                                                                tmp2.append(int(j[2:]))
                                                                tmp_size_lbd_doublons_impair.append(tmp2)
                                                                tmp_replica_lbd_impair.append(int(j[2:]))
                                                tmp3.insert(0,size[2])
                                                tmp3.insert(0,int(cpt))
                                                tmp_doublons_size_lbd.append(tmp3)
                                elif(x[0] == "lbdot"):
                                        if(last_index != int(x[2])):
                                                last_index = int(x[2])
                                                tmp.append(int(x[1]))
                                                tmp.append(int(x[3]))
                                                tmp_doublons_round.append(tmp)
                                elif(x[0] == "cg"): # toutes les clauses
                                        k = line.split(";")
                                        size = k[0].split(",")[2]
                                        tmp_size_doublons_global.append(int(size))
                                        for i in range (1,len(k)):
                                                j = k[i].split(",")
                                                tmp_pair = []
                                                tmp_impair = []
                                                if(int(j[0])%2): #pair
                                                        tmp_pair.append(int(size)) # size
                                                        tmp_pair.append(int(j[1])) # lbd
                                                        # contient size + lbd
                                                        tmp_lbd_global_pair.append(tmp_pair)
                                                        # contient uniquement les lbd
                                                        tmp_lbd_doublons_global_pair.append(int(j[1]))
                                                else:
                                                        tmp_impair.append(int(size)) # worker
                                                        tmp_impair.append(int(j[1])) # lbd
                                                        tmp_lbd_global_impair.append(tmp_impair)

                                                        tmp_lbd_doublons_global_impair.append(int(j[1]))
                                elif(x[0] == "lit"):
                                        if(name == x[1]):
                                                somme = somme + int(x[3])
                                        else:
                                                if(somme != 1):
                                                        tmp_variable.append(somme)
                                                name = int(x[1])
                                                somme = int(x[3])

                if tmp_variable:
                        tmp_variable.insert(0,int(order))
                        tab_variable.append(tmp_variable)

                if tmp_lbd_global_pair: # tous les lbd de chaque clauses même doublon
                        tab_lbd_global_pair.append(tmp_lbd_global_pair)
                        tab_lbd_global_impair.append(tmp_lbd_global_impair)

                if tmp_lbd_doublons_global_pair:
                        tab_lbd_pair_doublons_global.append(tmp_lbd_doublons_global_pair)
                        tab_lbd_impair_doublons_global.append(tmp_lbd_doublons_global_impair)
                
                if tmp_replica_lbd_pair:
                        tab_replica_lbd_pair.append(tmp_replica_lbd_pair)
                        tab_replica_lbd_impair.append(tmp_replica_lbd_impair)
                
                if tmp_doublons_round:
                        tab_doublons_round.append(tmp_doublons_round)
                        
                if tmp_doublons_size_lbd:
                        tab_doublons_many_size_lbd.append(tmp_doublons_size_lbd)
                        
                if tmp_lbd_pair:
                        tmp_lbd_pair.insert(0,int(order))
                        tmp_lbd_impair.insert(0,int(order))
                        tab_lbd_pair.append(tmp_lbd_pair)
                        tab_lbd_impair.append(tmp_lbd_impair)
                        
                if tmp_doublons_many:
                        tmp_doublons_many.insert(0,int(doublons))
                        tab_doublons_many.append(tmp_doublons_many)  
                        
                if tmp_workers_data_pair:
                        tab_workers_data_pair.append(tmp_workers_data_pair)
                        tab_workers_data_impair.append(tmp_workers_data_impair)
                        
                if tmp_size_doublons:
                        tmp_size_doublons.insert(0,int(order))
                        tab_size_doublons.append(tmp_size_doublons)
                
                if tmp_size_doublons:
                        tmp_size_doublons_global.insert(0,int(order))
                        tab_size_doublons_global.append(tmp_size_doublons_global)
                
                if tmp_size_lbd_doublons_pair:
                        tab_size_lbd_doublons_pair.append(tmp_size_lbd_doublons_pair)
                        tab_size_lbd_doublons_impair.append(tmp_size_lbd_doublons_impair)
                
                time_doublons.append(tmp_time)
                print("File Done")

        # avoir l'ordre des problèmes
        file_name.sort() 
        tab_workers_data_pair.sort()
        tab_workers_data_impair.sort()
        tab_lbd_pair.sort()
        tab_lbd_impair.sort()
        tab_total_clauses.sort()
        tab_size_doublons.sort()
        tab_gd.sort()
        tab_size_doublons_global.sort()
        tab_variable.sort()
        print("Done")
        
#################################################################################################################################################################################

def percentage_doublons():
        
        print("percentage_doublons")
        
        tab_data_pair  = []
        tab_data_impair = []
        total = []
        data_pair = []
        data_impair = []
        data_global = []

        for p,i in zip(tab_workers_data_pair,tab_workers_data_impair):
                i.pop(0)
                p.pop(0)
                tmp_pair = []
                tmp_impair = []
                for j,k in zip(i,p):
                        pourcentage = (j[1]/j[0])*100
                        tmp_pair.append(pourcentage)
                        pourcentage = (k[1]/k[0])*100
                        tmp_impair.append(pourcentage)
                
                tab_data_pair.append(vide)
                tab_data_pair.append(tmp_pair)
                tab_data_pair.append(vide)
                tab_data_pair.append(vide)
                tab_data_impair.append(vide)
                tab_data_impair.append(tmp_impair)
                tab_data_impair.append(vide)
                tab_data_impair.append(vide)

        for i in tab_total_clauses:
                tmp_total = []
                pourcentage = (i[0]/i[1])*100 #doublons/clauses
                tmp_total.append(pourcentage)
                total.append(tmp_total)
                total.append(vide)
                total.append(vide)
                total.append(vide)

        for i in tab_gd:
                
                tmp_pair = []
                tmp_impair = []
                tmp_global = []

                tmp_pair.append((i[1]/i[0])*100)
                tmp_impair.append((i[2]/i[0])*100)
                tmp_global.append((i[3]/i[0])*100)
                data_pair.append(tmp_pair)
                data_pair.append(vide)
                data_pair.append(vide)
                data_pair.append(vide)
                data_impair.append(tmp_impair)
                data_impair.append(vide)
                data_impair.append(vide)
                data_impair.append(vide)
                data_global.append(tmp_global)
                data_global.append(vide)
                data_global.append(vide)
                data_global.append(vide)
                
        df_pair_doublons = pd.DataFrame(data_pair).transpose()
        df_impair_doublons = pd.DataFrame(data_impair).transpose()
        df_global = pd.DataFrame(data_global).transpose()
        df_total = pd.DataFrame(total).transpose()
        df_pair = pd.DataFrame(tab_data_pair).transpose()
        df_impair = pd.DataFrame(tab_data_impair).transpose()

        ax = plt.subplot(111)
        plt.gcf().set_size_inches(12, 8) #(x,y)

        sns.swarmplot(ax=ax,data=df_total,size=7,color="purple",label="Total of Doublons") #Total
        sns.swarmplot(ax=ax,data=df_global,size=7,color="purple",marker='^',label="Doublons between VSIDS/LRB workers")
        sns.swarmplot(ax=ax,data=df_impair,size=3,color="blue",label="Self Doublons VSIDS") #VSIDS
        sns.swarmplot(ax=ax,data=df_pair,size=3,color="red",label="Self Doublons LRB") #LRB
        sns.swarmplot(ax=ax,data=df_impair_doublons,size=5,color="blue",marker='^',label="Doublons in VSIDS workers")
        sns.swarmplot(ax=ax,data=df_pair_doublons,size=5,color="red",marker='^',label="Doublons in LRB workers")

        #plt.title("Duplicates' Repartition per CNF files before selection")

        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        plt.legend(by_label.values(), by_label.keys())
        plt.ylabel("Duplicates' Percentage")
        plt.xlabel("Clauses' number in ascending order")
        plt.xticks([])
        #plt.show()
        plt.savefig("graphe/swarmplot-duplicate")
        #plt.savefig("graphe/swarmplot-duplicate-selected")
        plt.figure().clear()
        plt.close()
        plt.cla()
        plt.clf()
        print("Done")

#################################################################################################################################################################################

def lbd_doublons():
        print("lbd_doublons")
        
        for i,j in zip(tab_lbd_impair,tab_lbd_pair):
                j.pop(0)
                i.pop(0)

        for i,j in zip(tab_lbd_impair_doublons_global,tab_lbd_pair_doublons_global):
                j.pop(0)
                i.pop(0)
        
        fig, axes =  plt.subplots(nrows=2, ncols=2,sharey=False,sharex=True)
        # fig.suptitle("Lbd's repartition per Clauses before selection")
        # fig.supxlabel("Id Problem in Clauses ascending number")
        # fig.supylabel("Lbd' size")
        df_pair_global = pd.DataFrame(tab_lbd_pair_doublons_global).transpose() # LRB
        df_impair_global = pd.DataFrame(tab_lbd_impair_doublons_global).transpose() # VSIDS
        df_pair_global.boxplot(ax=axes[0,0],grid=True,showfliers=False)
        df_impair_global.boxplot(ax=axes[1,0],grid=True,showfliers=False)
        
        # df_pair = pd.DataFrame(tab_lbd_pair).transpose() # LRB
        # df_impair = pd.DataFrame(tab_lbd_impair).transpose() # VSIDS
        # df_pair.boxplot(ax=axes[0,1],grid=True,showfliers=False)
        # df_impair.boxplot(ax=axes[1,1],grid=True,showfliers=False)
        
        axes[0,0].legend(['LRB'], loc='upper right')
        axes[1,0].legend(['VSIDS'], loc='upper right')
        axes[0,1].legend(['LRB'], loc='upper right')
        axes[1,1].legend(['VSIDS'], loc='upper right')
        axes[0,0].set_title("Global's clauses")
        axes[0,1].set_title("Duplicates")
        #plt.show()
        plt.xticks([])
        plt.savefig("graphe/boxplot-lbd-duplicate")
        #plt.savefig("graphe/boxplot-lbd-duplicate-selected")
        plt.figure().clear()
        plt.close()
        plt.cla()
        plt.clf()
        print("Done")

#################################################################################################################################################################################

def size_doublons():
        print("Size_doublons")
        for i,j in zip(tab_size_doublons,tab_size_doublons_global):
                i.pop(0)
                j.pop(0)
        
        fig, axes = plt.subplots(nrows=2, ncols=1,sharey=True,sharex=True)

        df = pd.DataFrame(tab_size_doublons_global).transpose()
        df.boxplot(ax=axes[0],grid=True,showfliers=False)

        df = pd.DataFrame(tab_size_doublons).transpose()
        df.boxplot(ax=axes[1],grid=True,showfliers=False)        
        
        plt.title("Clauses' size repartition per Problems before selection")
        plt.ylabel("Size")
        plt.xlabel("Id Problem in Clauses ascending number")

        axes[0].set_title("Global's clauses")
        axes[1].set_title("Duplicates")
        plt.xticks([])
        #plt.show()
        
        plt.savefig("graphe/boxplot-size-duplicate")
        #plt.savefig("graphe/boxplot-size-duplicate-selected")
        plt.figure().clear()
        plt.close()
        plt.cla()
        plt.clf()
        print("Done")

#################################################################################################################################################################################

def size_lbd_doublon():
        print("size_lbd_doublon")
        max_size = 0
        fig, axes =  plt.subplots(nrows=2, ncols=2,sharey=True,sharex=True)
        
        for i,j,k,l in zip(tab_size_lbd_doublons_pair,tab_size_lbd_doublons_impair,tab_lbd_global_impair,tab_lbd_global_pair):
                max_size = max(max_size,func.max_value(i))
                max_size = max(max_size,func.max_value(j))
                max_size = max(max_size,func.max_value(k))
                max_size = max(max_size,func.max_value(l))
        #TODO Taille maximal entre les globaux/doublons
        for p,ip,gp,gip in zip(tab_size_lbd_doublons_pair,tab_size_lbd_doublons_impair,tab_lbd_global_pair,tab_lbd_global_impair):
                tab_mem_pair = []
                tab_mem_impair = []
                tab_mem_pair_global = []
                tab_mem_impair_global = []
                
                for i in range(1,max_size+1):
                        tmp = []
                        tmp_mem = []
                        for j in p:   
                                if i == j[0]:
                                        tmp_mem.append(j[1])
                        if tmp_mem:
                                moyenne = mean(tmp_mem)
                        else:
                                moyenne = None                                        
                        tmp.append(i)
                        tmp.append(moyenne)
                        tab_mem_pair.append(tmp)                        
                        tmp = []
                        tmp_mem = []
                        for j in ip:   
                                if i == j[0]:
                                        tmp_mem.append(j[1])
                        if tmp_mem:
                                moyenne = mean(tmp_mem)
                        else:
                                moyenne = None   
                        tmp.append(i)
                        tmp.append(moyenne)
                        tab_mem_pair_global.append(tmp)
                        #! --- global ---
                        tmp = []
                        tmp_mem = []
                        for j in gp:   
                                if i == j[0]:
                                        tmp_mem.append(j[1])
                        if tmp_mem:
                                moyenne = mean(tmp_mem)
                        else:
                                moyenne = None                                        
                        tmp.append(i)
                        tmp.append(moyenne)
                        tab_mem_impair_global.append(tmp)
                        
                        tmp = []
                        tmp_mem = []
                        for j in gip:   
                                if i == j[0]:
                                        tmp_mem.append(j[1])
                        if tmp_mem:
                                moyenne = mean(tmp_mem)
                        else:
                                moyenne = None                                        
                        tmp.append(i)
                        tmp.append(moyenne)
                        tab_mem_impair.append(tmp)
                        
                color = func.random_color()
                df_pair_global = pd.DataFrame(data=tab_mem_pair_global,columns=["Size","Lbd"])
                df_impair_global = pd.DataFrame(data=tab_mem_impair_global,columns=["Size","Lbd"])
                df_pair = pd.DataFrame(data=tab_mem_pair,columns=["Size","Lbd"])
                df_impair = pd.DataFrame(data=tab_mem_impair,columns=["Size","Lbd"])
                
                df_pair_global.plot(ax=axes[0, 0],kind='scatter',x='Size',y='Lbd',color=color) #LRB
                df_impair_global.plot(ax=axes[1, 0],kind='scatter',x='Size',y='Lbd',color=color)
                df_pair.plot(ax=axes[0, 1],kind='scatter',x='Size',y='Lbd',color=color) #LRB
                df_impair.plot(ax=axes[1, 1],kind='scatter',x='Size',y='Lbd',color=color)

        axes[0, 0].legend(['LRB'], loc='upper right')
        axes[1, 0].legend(['VSIDS'], loc='upper right')
        axes[0, 1].legend(['LRB'], loc='upper right')
        axes[1, 1].legend(['VSIDS'], loc='upper right')
        axes[0,0].set_title("Global's clauses")
        axes[0,1].set_title("Duplicates")
        #fig.suptitle("Lbd's repartition per size before selection")
        #plt.show() 
        plt.savefig("graphe/scatter-lbd-size-duplicate")
        #plt.savefig("graphe/scatter-lbd-size-duplicate-selected")
        plt.figure().clear()
        plt.close()
        plt.cla()
        plt.clf()
        print("Done")

#################################################################################################################################################################################

def doublons_temps():
        print("Doublons par temps")
        tmp_doublons = [x for x in time_doublons if x != []]
        tab_doublons = []
        ax =  plt.subplot(111)
        for i in tmp_doublons: # Découpe par fichiers
                tmp_file = []
                for j in i: # découpe par minute du fichier
                        tmp = []
                        timer = (j[0] + 1)*3
                        if(j[2] != 0):
                                pourcentage = (j[1]/j[2])*100
                        else:
                                pourcentage = 0
                        tmp.append(timer)
                        tmp.append(pourcentage)
                        tmp_file.append(tmp)

                tab_doublons.append(tmp_file)
        for i in tab_doublons:
                df = pd.DataFrame(data=i,columns=["Time","Doublon"])
                df.plot(ax = ax,x="Time",y="Doublon",legend=None,style='-o')

        plt.title("Percentage's doublons per Minutes before selection delayed")
        plt.ylabel("Percentage's doublon")
        plt.xlabel("Minutes")
        plt.savefig("graphe/time-duplicate-delayed-60s")
        #plt.savefig("graphe/time-duplicate-selected")
        #plt.show()
        plt.figure().clear()
        plt.close()
        plt.cla()
        plt.clf()
        print("Done")

#################################################################################################################################################################################

def doublons_many():
        
        print("doublons_many")
        ax = plt.subplot(111)
        
        for i in tab_doublons_many:
                max_doublons = 0
                i.pop(0)
                tmp_data = [0]
                tab_data = []
                index = 1
                for j in i[1:]:
                        tmp_data.append(tmp_data[-1]+(j[1]))
                        max_doublons = max_doublons + j[1]
                for j in tmp_data[:10]:
                        tmp = []
                        pourcentage = (j/max_doublons)*100
                        tmp.append(index)
                        tmp.append(pourcentage)
                        index = index + 1
                        tab_data.append(tmp)
                
                df = pd.DataFrame(tab_data,columns=["Doublons","Number"])
                df.plot(ax = ax,x="Doublons",y="Number",legend=None)
        
        #plt.title("Percentage's doublons per number of time they appear after selection")
        plt.ylabel("Percentage's doublon")
        plt.xlabel("Number's doublons")
        plt.xlim(1)
        #plt.savefig("graphe/doublons-number-selected")
        plt.savefig("graphe/doublons-number")
        #plt.show()
        plt.figure().clear()
        plt.close()
        plt.cla()
        plt.clf()
        print("Done")

#################################################################################################################################################################################

def doublons_many_lbd():
        print("doublons_many_lbd")
        ax = plt.subplot(111)
        max_value = 0
        for f in tab_doublons_many_size_lbd:
                max_value = max(max_value,func.max_value(f)) #plus grand nombre de fois qu'une clause apparaît
        for f in tab_doublons_many_size_lbd:
                tab_size_lbd = []
                for cpt in range(1,max_value+1):
                        tmp = [] # reset de doublons
                        tmp2 = []
                        for i in f:
                                if(i[0] == cpt):
                                        for k in i[2:]:
                                                tmp.append(k) # récupère les lbd
                        if tmp:
                                moyenne = mean(tmp)
                        else: 
                                moyenne = None
                        tmp2.append(cpt)
                        tmp2.append(moyenne)
                        tab_size_lbd.append(tmp2)
                
                df = pd.DataFrame(tab_size_lbd,columns=["Number","lbd"])
                df.plot(kind="scatter",x="Number",y="lbd",ax = ax,legend=None,color=func.random_color())
        
        plt.title("lbd per number of time they appear before selection")
        plt.ylabel("lbd")
        plt.xlabel("Number of time clauses appear")
        #plt.show()
        #plt.savefig("graphe/doublons-number-lbd-selected")
        plt.savefig("graphe/doublons-number-lbd")
        plt.figure().clear()
        plt.close()
        plt.cla()
        plt.clf()
        print("Done")

#################################################################################################################################################################################

def doublons_many_size():
        print("doublons_many_size")
        ax = plt.subplot(111)
        max_value = 0
        for f in tab_doublons_many_size_lbd:
                max_value = max(max_value,func.max_value(f))
        
        for f in tab_doublons_many_size_lbd:
                tab_size = []
                for cpt in range(1,max_value+1):
                        tmp = [] # reset de doublons
                        tmp2 = []
                        for i in f:
                                if(i[0] == cpt):
                                        tmp.append(int(i[1])) # récupère la size
                        if tmp:
                                moyenne = mean(tmp)
                        else: 
                                moyenne = None
                        tmp2.append(cpt)
                        tmp2.append(moyenne)
                        tab_size.append(tmp2)
                df = pd.DataFrame(tab_size,columns=["Number","size"])
                df.plot(kind="scatter",x="Number",y="size",ax = ax,legend=None,color=func.random_color())
        
        plt.title("size per number of time they appear after selection")
        plt.ylabel("size")
        plt.xlabel("Number of time clauses appear")
        #plt.show()
        #plt.savefig("graphe/doublons-number-size-selected")
        plt.savefig("graphe/doublons-number-size")
        plt.figure().clear()
        plt.close()
        plt.cla()
        plt.clf()
        print("Done")
        
##########################################################################################################################################

def doublons_round():
        print("doublons_round")
        ax = plt.subplot(111)

        for i in tab_doublons_round:
                tab_nb_doublons = []
                tmp_nb_doublons = []
                tmp_nb_doublons.append(0)
                tmp_nb_doublons.append(0)
                max_round = func.max_value(i)
                for k in range(max_round+1):
                        tmp_nb_doublons = []
                        diviseur = 1
                        dividende = 0
                        for j in i:
                                if(int(j[0]) == k ):
                                        dividende = dividende + int(j[1])
                                        diviseur =  diviseur + 1
                        tmp_nb_doublons.append(k*3+3)
                        tmp_nb_doublons.append(dividende/diviseur)
                        tab_nb_doublons.append(tmp_nb_doublons)
        
                df = pd.DataFrame(tab_nb_doublons,columns=["Minutes","Number"])
                
                df.plot(ax = ax,x="Minutes",y="Number",legend=None)
        
        #plt.title("Number's Replica per Minutes before selection")
        plt.ylabel("Number's replica")
        plt.xlabel("Minutes")
        plt.xlim(3,45)
        #plt.show()
        #plt.savefig("graphe/doublons-round-selected")
        plt.savefig("graphe/doublons-round-size")
        plt.figure().clear()
        plt.close()
        plt.cla()
        plt.clf()
        print("Done")

##########################################################################################################################################

def lbd_number_replica():
        print("lbd_number_replica")
        fig, axes =  plt.subplots(nrows=2, ncols=2,sharey=True,sharex=True)
        
        for p,ip,gp,gip in zip(tab_replica_lbd_pair,tab_replica_lbd_impair,tab_lbd_pair_doublons_global,tab_lbd_impair_doublons_global):
                max_value_pair = max(p)
                tab_pair = []
                for i in range(max_value_pair+1):
                        number_replica = 0
                        tmp = []
                        for j in p:
                                if(i == j):
                                        number_replica = number_replica + 1
                        tmp.append(i)
                        tmp.append(number_replica)
                        tab_pair.append(tmp)
                
                couleur = func.random_color()
                df_pair = pd.DataFrame(tab_pair,columns=["Lbd","Replica"]) 
                df_pair.plot(ax=axes[0,1],kind='scatter',x='Lbd',y='Replica',color=couleur)
                
                max_value_impair = max(ip)
                tab_impair = []
                for i in range(max_value_impair+1):
                        number_replica = 0
                        tmp = []
                        for j in ip:
                                if(i == j):
                                        number_replica = number_replica + 1
                        tmp.append(i)
                        tmp.append(number_replica)
                        tab_impair.append(tmp)
                
                df_impair = pd.DataFrame(tab_impair,columns=["Lbd","Replica"]) 
                df_impair.plot(ax=axes[1,1],kind='scatter',x='Lbd',y='Replica',color=couleur)

                max_value_pair = max(gp)
                tab_global_pair = []
                for i in range(max_value_pair+1):
                        number_replica = 0
                        tmp = []
                        for j in gp:
                                if(i == j):
                                        number_replica = number_replica + 1
                        tmp.append(i)
                        tmp.append(number_replica)
                        tab_global_pair.append(tmp)
                
                df_pair_global = pd.DataFrame(tab_global_pair,columns=["Lbd","Replica"]) 
                df_pair_global.plot(ax=axes[0,0],kind='scatter',x='Lbd',y='Replica',color=couleur)

                max_value_impair = max(gip)
                tab_global_impair = []
                for i in range(max_value_impair+1):
                        number_replica = 0
                        tmp = []
                        for j in gip:
                                if(i == j):
                                        number_replica = number_replica + 1
                        tmp.append(i)
                        tmp.append(number_replica)
                        tab_global_impair.append(tmp)
                
                df_impair_global = pd.DataFrame(tab_global_impair,columns=["Lbd","Replica"]) 
                df_impair_global.plot(ax=axes[1,0],kind='scatter',x='Lbd',y='Replica',color=couleur)

        plt.xlim(0)
        axes[0,1].legend(['LRB'], loc='upper right')
        axes[1,1].legend(['VSIDS'], loc='upper right')
        #fig.suptitle("Lbd's repartition per clause after selection")
        plt.savefig("graphe/scatter-lbd-number-replica")
        #plt.savefig("graphe/scatter-lbd-number-replica-selected")
        plt.figure().clear()
        plt.close()
        plt.cla()
        plt.clf()
        #plt.show()

###################################################################################################

def variables_repartition():
        for i in tab_variable:
                i.pop(0)
                i.pop(0)

        ax = plt.subplot(111)

        df = pd.DataFrame(tab_variable).transpose()
        sns.boxplot(data=df,ax=ax)

        plt.title("Literals repartition per clauses per Problems before selection")
        plt.ylabel("redondance's literal")
        plt.xlabel("Problem in Clauses ascending number")

        plt.xticks([])
        #plt.show()
        
        plt.savefig("graphe/boxplot-variable-duplicate")
        #plt.savefig("graphe/boxplot-variable-duplicate-selected")
        plt.figure().clear()
        plt.close()
        plt.cla()
        plt.clf()
        print("Done")
##################### main ####################
func.read_directory(sys.argv[1:][0],files)
read_file(files)
func.aff_probs(file_name)
percentage_doublons() #- Mis à jour et le rendu est correct sur le rapport
lbd_doublons() #? Fait mais à tester
# size_doublons() #? Fait mais à tester
# size_lbd_doublon() #? Fait mais à tester
# doublons_temps() #? Fait mais à tester
# doublons_many() #- Mis à jour et le rendu est correct sur le rapport
# doublons_many_lbd() #? Fait mais à tester
# doublons_many_size() #? Fait mais à tester
# doublons_round() #- Mis à jour et le rendu est correct sur le rapport
# lbd_number_replica() #? Fait mais à tester
variables_repartition()