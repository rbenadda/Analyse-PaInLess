import sys
from os import path
import csv
from statistics import mean
import warnings
import function as func
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

warnings.filterwarnings('ignore')

files = []
color = []
list_df = []
list_df_time = []
list_dataframe = []
list_df_selected = []
list_df_selected_time = []


element = 0

def read_files(files):

        for file in files:
                df = pd.read_csv(sys.argv[1:][0] + "/" +file)
                df.fillna(0)
                if not "selected" in file:
                        if not "time" in file: # dup
                                list_df.append(df)
                                global element 
                                element = element + 1
                        else: # dup-time
                                list_df_time.append(df)
                elif not "time" in file: # dup-selected
                        list_df_selected.append(df)
                else: # dup-time selected
                        list_df_selected_time.append(df)

        list_dataframe.append(list_df)
        list_dataframe.append(list_df_selected)

##################################################################################################################################################

def lbd_doublons():

        selected = False

        for df in list_dataframe :
                df_GIP = [i.loc[(i['key'].eq('cg')) & (i['ID_worker'].mod(2).eq(1))]['lbd'] for i in df]
                df_GP = [i.loc[(i['key'].eq('cg')) & (i['ID_worker'].mod(2).eq(0))]['lbd'] for i in df]
                df_DIP = [i.loc[(i['key'].eq('cd')) & (i['ID_worker'].mod(2).eq(1))]['lbd'] for i in df]
                df_DP = [i.loc[(i['key'].eq('cd')) & (i['ID_worker'].mod(2).eq(0))]['lbd'] for i in df]

                df_GIP = pd.DataFrame(df_GIP).transpose()
                df_GP = pd.DataFrame(df_GP).transpose()
                df_DIP = pd.DataFrame(df_DIP).transpose()
                df_DP = pd.DataFrame(df_DP).transpose()
                
                fig, axes =  plt.subplots(nrows=2, ncols=2,sharey=True,sharex=True)

                df_GP.boxplot(ax=axes[0,0],grid=True,showfliers=False)
                df_GIP.boxplot(ax=axes[1,0],grid=True,showfliers=False)      
                df_DP.boxplot(ax=axes[0,1],grid=True,showfliers=False)
                df_DIP.boxplot(ax=axes[1,1],grid=True,showfliers=False)
                
                fig.supxlabel("Problems")
                fig.supylabel("Lbd")

                axes[0,0].legend(['LRB'], loc='upper right')
                axes[1,0].legend(['VSIDS'], loc='upper right')
                axes[0,1].legend(['LRB'], loc='upper right')
                axes[1,1].legend(['VSIDS'], loc='upper right')
                axes[0,0].set_title("Global clauses")
                axes[0,1].set_title("Duplicates")
                plt.xticks([])
                
                if selected == False:
                        plt.savefig("graphe/boxplot-lbd-duplicate")
                        selected = True
                else:
                        plt.savefig("graphe/boxplot-lbd-duplicate-selected")
                        selected = False

                plt.figure().clear()
                plt.close()
                plt.cla()
                plt.clf()

def size_doublons(): 

        selected = False

        for df in list_dataframe :
                df_GIP = [i.loc[(i['key'].eq('cg')) & (i['ID_worker'].mod(2).eq(1))]['size'] for i in df]
                df_GP = [i.loc[(i['key'].eq('cg')) & (i['ID_worker'].mod(2).eq(0))]['size'] for i in df]
                df_DIP = [i.loc[(i['key'].eq('cd')) & (i['ID_worker'].mod(2).eq(1))]['size'] for i in df]
                df_DP = [i.loc[(i['key'].eq('cd')) & (i['ID_worker'].mod(2).eq(0))]['size'] for i in df]

                df_GIP = pd.DataFrame(df_GIP).transpose()
                df_GP = pd.DataFrame(df_GP).transpose()
                df_DIP = pd.DataFrame(df_DIP).transpose()
                df_DP = pd.DataFrame(df_DP).transpose()

                fig, axes = plt.subplots(nrows=2, ncols=2,sharey=True,sharex=True)

                df_GP.boxplot(ax=axes[0,0],grid=True,showfliers=False)
                df_GIP.boxplot(ax=axes[1,0],grid=True,showfliers=False)      
                df_DP.boxplot(ax=axes[0,1],grid=True,showfliers=False)
                df_DIP.boxplot(ax=axes[1,1],grid=True,showfliers=False)

                fig.supxlabel("Problems")
                fig.supylabel("Size")

                axes[0,0].legend(['LRB'], loc='upper right')
                axes[1,0].legend(['VSIDS'], loc='upper right')
                axes[0,1].legend(['LRB'], loc='upper right')
                axes[1,1].legend(['VSIDS'], loc='upper right')
                axes[0,0].set_title("Global clauses")
                axes[0,1].set_title("Duplicates")

                plt.xticks([])

                if selected == False:
                        plt.savefig("graphe/boxplot-size-duplicate")
                        selected = True
                else:
                        plt.savefig("graphe/boxplot-size-duplicate-selected")
                        selected = False
                
                plt.figure().clear()
                plt.close()
                plt.cla()
                plt.clf()

def variables_repartition():
        
        selected = False

        for df in list_dataframe :
                fig, axes = plt.subplots(nrows=1, ncols=2,sharey=True,sharex=True)
                
                df_G = [i.loc[i['key'].eq('glit')].groupby('ID')['cpt'].sum() for i in list_df]
                df_D = [i.loc[i['key'].eq('dlit')].groupby('ID')['cpt'].sum() for i in list_df]

                df_G = pd.DataFrame(df_G).transpose()
                df_D = pd.DataFrame(df_D).transpose()

                df_G.boxplot(ax=axes[0],grid=True,showfliers=False)
                df_D.boxplot(ax=axes[1],grid=True,showfliers=False)
                
                fig.supxlabel("Problems")
                fig.supylabel("Number of literals")
                axes[0].set_title("Global's clauses")
                axes[1].set_title("Duplicates")
                
                plt.xticks([])
                plt.yscale('log')

                if selected == False:
                        plt.savefig("graphe/boxplot-variable-duplicate")
                        selected = True
                else:
                        plt.savefig("graphe/boxplot-variable-duplicate-selected")
                        selected = False
        
                plt.figure().clear()
                plt.close()
                plt.cla()
                plt.clf()
        
def size_lbd_doublon():

        selected = False

        for df in list_dataframe :
                fig, axes = plt.subplots(nrows=2, ncols=2,sharey=True,sharex=True)
                for i,c in zip(df,color):

                        df_GIP = i.loc[i['key'].eq('cg') & i['ID_worker'].mod(2).eq(1)].groupby('size')['size','lbd'].mean() 
                        df_GP = i.loc[i['key'].eq('cg') & i['ID_worker'].mod(2).eq(0)].groupby('size')['size','lbd'].mean() 
                        df_DIP = i.loc[i['key'].eq('cd') & i['ID_worker'].mod(2).eq(1)].groupby('size')['size','lbd'].mean() 
                        df_DP = i.loc[i['key'].eq('cd') & i['ID_worker'].mod(2).eq(0)].groupby('size')['size','lbd'].mean() 
                        
                        df_GIP = pd.DataFrame(df_GIP)
                        df_GP = pd.DataFrame(df_GP)
                        df_DIP = pd.DataFrame(df_DIP)
                        df_DP = pd.DataFrame(df_DP)

                        df_GP.plot(kind="scatter",x="size",y='lbd',ax=axes[0,0],legend=None,color=c,grid=True)
                        df_GIP.plot(kind="scatter",x='size',y='lbd',ax=axes[1,0],legend=None,color=c,grid=True)      
                        df_DP.plot(kind="scatter",x='size',y='lbd',ax=axes[0,1],legend=None,color=c,grid=True)
                        df_DIP.plot(kind="scatter",x='size',y='lbd',ax=axes[1,1],legend=None,color=c,grid=True)

                axes[0,0].legend(['LRB'], loc='upper right')
                axes[1,0].legend(['VSIDS'], loc='upper right')
                axes[0,1].legend(['LRB'], loc='upper right')
                axes[1,1].legend(['VSIDS'], loc='upper right')
                axes[0,0].set_title("Global's clauses")
                axes[0,1].set_title("Duplicates")   
                axes[1,0].xaxis.set_label_text("")
                axes[1,1].xaxis.set_label_text("")
                axes[0,0].yaxis.set_label_text("")
                axes[1,0].yaxis.set_label_text("")
                fig.supxlabel("Size")
                fig.supylabel("Lbd")
                plt.xscale('log')
                

                if selected == False:
                        plt.savefig("graphe/doublons-number-size-lbd")
                        selected = True
                else:
                        plt.savefig("graphe/doublons-number-size-lbd-selected")
                        selected = False

                plt.figure().clear()
                plt.close()
                plt.cla()
                plt.clf()

def doublons_many_lbd():

        selected = False

        for df in list_dataframe :
                fig, axes = plt.subplots(nrows=1, ncols=2,sharey=True,sharex=True)
                for i,c in zip(df,color):

                        df_P = i.loc[i['key'].isin(['cg','cd']) & i['ID_worker'].mod(2).eq(0)].groupby('cpt')['lbd'].mean().to_frame('lbd')
                        df_IP = i.loc[i['key'].isin(['cg','cd']) & i['ID_worker'].mod(2).eq(1)].groupby('cpt')['lbd'].mean().to_frame('lbd')
                
                        df_P = pd.DataFrame(df_P,columns=["lbd"])
                        df_IP = pd.DataFrame(df_IP,columns=["lbd"])

                        df_P.insert(0,"Number of duplicates",range(1,len(df_P)+1),True)
                        df_IP.insert(0,"Number of duplicates",range(1,len(df_IP)+1),True)

                        df_P.plot(kind="scatter",x="Number of duplicates",y="lbd",ax = axes[0],legend=None,color=c,grid=True)
                        df_IP.plot(kind="scatter",x="Number of duplicates",y="lbd",ax = axes[1],legend=None,color=c,grid=True)
                
                axes[0].legend(['LRB'], loc='upper right')
                axes[1].legend(['VSIDS'], loc='upper right') 
                axes[0].yaxis.set_label_text("")
                axes[0].xaxis.set_label_text("")
                axes[1].xaxis.set_label_text("")
                fig.supxlabel("Number of duplicates")
                fig.supylabel("Lbd")
                plt.ylim(0,40)
                if selected == False:
                        plt.savefig("graphe/doublons-number-lbd")
                        selected = True
                else:
                        plt.savefig("graphe/doublons-number-lbd-selected")
                        selected = False

                plt.figure().clear()
                plt.close()
                plt.cla()
                plt.clf()

def doublons_many_size():

        selected = False

        for df in list_dataframe :
                fig, axes = plt.subplots(nrows=1, ncols=2,sharey=True,sharex=True)
                for i,c in zip(df,color):

                        df_P = i.loc[i['key'].isin(['cg','cd']) & i['ID_worker'].mod(2).eq(0)].groupby('cpt')['size'].mean().to_frame('size')
                        df_IP = i.loc[i['key'].isin(['cg','cd']) & i['ID_worker'].mod(2).eq(1)].groupby('cpt')['size'].mean().to_frame('size')
                
                        df_P = pd.DataFrame(df_P,columns=["size"])
                        df_IP = pd.DataFrame(df_IP,columns=["size"])

                        df_P.insert(0,"Number of duplicates",range(1,len(df_P)+1),True)
                        df_IP.insert(0,"Number of duplicates",range(1,len(df_IP)+1),True)

                        df_P.plot(kind="scatter",x="Number of duplicates",y="size",ax = axes[0],legend=None,color=c,grid=True)
                        df_IP.plot(kind="scatter",x="Number of duplicates",y="size",ax = axes[1],legend=None,color=c,grid=True)
        
                axes[0].legend(['LRB'], loc='upper right')
                axes[1].legend(['VSIDS'], loc='upper right') 
                axes[0].yaxis.set_label_text("")
                axes[0].xaxis.set_label_text("")
                axes[1].xaxis.set_label_text("")
                fig.supxlabel("Number of duplicates")
                fig.supylabel("Size")
                plt.ylim(0,60)
        
                if selected == False:
                        plt.savefig("graphe/doublons-number-size")
                        selected = True
                else:
                        plt.savefig("graphe/doublons-number-size-selected")
                        selected = False
                
                plt.figure().clear()
                plt.close()
                plt.cla()
                plt.clf()

def lbd_number_replica(): #-
        print("lbd_number_replica")
        selected = False

        for df in list_dataframe :
                fig, axes = plt.subplots(nrows=2, ncols=2,sharey=True,sharex=True)
                for i,c in zip(df,color):

                        df_GP = i.loc[i['key'].eq('cg') & i['ID_worker'].mod(2).eq(0)].groupby('lbd').size().to_frame('Number')
                        df_GP = pd.DataFrame(df_GP,columns=["Number"])
                        df_GP.insert(0,"Lbd",range(1,len(df_GP)+1),True)
                        df_GP.plot(kind="scatter",x="Lbd",y="Number",ax =axes[0,0],legend=None,color=c,grid=True)

                        df_GIP = i.loc[i['key'].eq('cg') & i['ID_worker'].mod(2).eq(1)].groupby('lbd').size().to_frame('Number')
                        df_GIP = pd.DataFrame(df_GIP,columns=["Number"])
                        df_GIP.insert(0,"Lbd",range(1,len(df_GIP)+1),True)
                        df_GIP.plot(kind="scatter",x="Lbd",y="Number",ax =axes[1,0],legend=None,color=c,grid=True)
                        
                        df_DP = i.loc[i['key'].eq('cd') & i['ID_worker'].mod(2).eq(0)].groupby('lbd').size().to_frame('Number')
                        df_DP = pd.DataFrame(df_DP,columns=["Number"])
                        df_DP.insert(0,"Lbd",range(1,len(df_DP)+1),True)
                        df_DP.plot(kind="scatter",x="Lbd",y="Number",ax =axes[0,1],legend=None,color=c,grid=True)

                        df_DIP = i.loc[i['key'].eq('cd') & i['ID_worker'].mod(2).eq(1)].groupby('lbd').size().to_frame('Number')
                        df_DIP = pd.DataFrame(df_DIP,columns=["Number"])
                        df_DIP.insert(0,"Lbd",range(1,len(df_DIP)+1),True)
                        df_DIP.plot(kind="scatter",x="Lbd",y="Number",ax =axes[1,1],legend=None,color=c,grid=True)
                
                axes[0,0].legend(['LRB'], loc='upper right')
                axes[1,0].legend(['VSIDS'], loc='upper right')
                axes[0,1].legend(['LRB'], loc='upper right')
                axes[1,1].legend(['VSIDS'], loc='upper right')
                axes[0,0].set_title("Global's clauses")
                axes[0,1].set_title("Duplicates")
                axes[0,0].yaxis.set_label_text("")
                axes[1,0].yaxis.set_label_text("")
                axes[1,0].xaxis.set_label_text("")
                axes[1,1].xaxis.set_label_text("")
                plt.xscale('log')
                plt.yscale('log')
                fig.supxlabel("Lbd")
                fig.supylabel("Number of clauses")
                
                if selected == False:
                        plt.savefig("graphe/scatter-lbd-number-replica")
                        selected = True
                else:
                        plt.savefig("graphe/scatter-lbd-number-replica-selected")
                plt.figure().clear()
                plt.close()
                plt.cla()
                plt.clf()
                
def size_number_replica():

        selected = False

        for df in list_dataframe :
                fig, axes = plt.subplots(nrows=2, ncols=2,sharey=True,sharex=True)
                for i,c in zip(df,color):

                        df_GP = i.loc[i['key'].eq('cg') & i['ID_worker'].mod(2).eq(0)].groupby('size').size().to_frame('Number')
                        df_GP = pd.DataFrame(df_GP,columns=["Number"])
                        df_GP.insert(0,"Size",range(1,len(df_GP)+1),True)
                        df_GP.plot(kind="scatter",x="Size",y="Number",ax =axes[0,0],legend=None,color=c,grid=True)

                        df_GIP = i.loc[i['key'].eq('cg') & i['ID_worker'].mod(2).eq(1)].groupby('size').size().to_frame('Number')
                        df_GIP = pd.DataFrame(df_GIP,columns=["Number"])
                        df_GIP.insert(0,"Size",range(1,len(df_GIP)+1),True)
                        df_GIP.plot(kind="scatter",x="Size",y="Number",ax =axes[1,0],legend=None,color=c,grid=True)
                        
                        df_DP = i.loc[i['key'].eq('cd') & i['ID_worker'].mod(2).eq(0)].groupby('size').size().to_frame('Number')
                        df_DP = pd.DataFrame(df_DP,columns=["Number"])
                        df_DP.insert(0,"Size",range(1,len(df_DP)+1),True)
                        df_DP.plot(kind="scatter",x="Size",y="Number",ax =axes[0,1],legend=None,color=c,grid=True)

                        df_DIP = i.loc[i['key'].eq('cd') & i['ID_worker'].mod(2).eq(1)].groupby('size').size().to_frame('Number')
                        df_DIP = pd.DataFrame(df_DIP,columns=["Number"])
                        df_DIP.insert(0,"Size",range(1,len(df_DIP)+1),True)
                        df_DIP.plot(kind="scatter",x="Size",y="Number",ax =axes[1,1],legend=None,color=c,grid=True)
        
                axes[0,0].legend(['LRB'], loc='upper right')
                axes[1,0].legend(['VSIDS'], loc='upper right')
                axes[0,1].legend(['LRB'], loc='upper right')
                axes[1,1].legend(['VSIDS'], loc='upper right')
                axes[0,0].set_title("Global's clauses")
                axes[0,1].set_title("Duplicates")
                axes[0,0].yaxis.set_label_text("")
                axes[1,0].yaxis.set_label_text("")
                axes[1,0].xaxis.set_label_text("")
                axes[1,1].xaxis.set_label_text("")
                plt.xscale('log')
                plt.yscale('log')
                fig.supxlabel("Size")
                fig.supylabel("Number of clauses")

                if selected == False:
                        plt.savefig("graphe/scatter-size-number-replica")
                        selected = True
                else:
                        plt.savefig("graphe/scatter-size-number-replica-selected")
                plt.figure().clear()
                plt.close()
                plt.cla()
                plt.clf()

def percentage_doublons():

        selected = False

        for df in list_dataframe :
                ax = plt.subplot(111).grid()
                sns.set_palette("pastel")
                for i,c in zip(df,color):
        
                        total = (i.loc[i['key'].eq('t')]['nb_doublons'] / i.loc[i['key'].eq('t')]['nb_clauses']) * 100
                        self_reducer = (i.loc[i['key'].eq('r')]['nb_doublons'] / i.loc[i['key'].eq('r')]['nb_doublons_pair']) * 100

                        df_total = pd.DataFrame(total,columns=["Global duplicates"])
                        df_self_reducer = pd.DataFrame(self_reducer,columns=["Reducer's duplicates"])

                        list_df = [df_total,df_self_reducer]
                        data = pd.concat(list_df)
                        sns.swarmplot(ax=ax,data=data) #Total

                plt.ylabel("Percentage of Duplicates")  
                if selected == False:
                        plt.savefig("graphe/swarmplot-duplicate-w-reducer")
                        selected = True
                else:
                        plt.savefig("graphe/swarmplot-duplicate-w-reducer-selected")
                plt.figure().clear()
                plt.close()
                plt.cla()
                plt.clf()

##################### main ####################
#* Pair : LRB | Impair : VSISD
func.read_directory(sys.argv[1:][0],files)
read_files(files)
color  = func.random_color_list(element)
# lbd_doublons() 
# size_doublons() #-Mis à jour et le rendu est correct sur le rapport
# variables_repartition() #-Mis à jour et le rendu est correct sur le rapport
# size_lbd_doublon() #-Mis à jour et le rendu est correct sur le rapport
# doublons_many_lbd() #-Mis à jour et le rendu est correct sur le rapport
# doublons_many_size() #-Mis à jour et le rendu est correct sur le rapport
# lbd_number_replica() #-Mis à jour et le rendu est correct sur le rapport
# size_number_replica() #-Mis à jour et le rendu est correct sur le rapport
percentage_doublons() 
