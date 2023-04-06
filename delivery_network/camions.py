################  Fichier routeout.py  ################   
############################# IMPORTATIONS ################################# 
from graphe import *


############################# Fonctions #################################   


# QUESTION 18
#Récupération de la liste des camions 
def collection_camions(filename):
    with open(filename) as file:
        nb_modele = int(file.readline())
        liste_camions = []
        for i in range(int(nb_modele)):
            ligne = file.readline().split()
            liste_camions.append([int(ligne[0]),int(ligne[1])])
        return liste_camions
    
#################

def recuperation_routes(filename):
    with open(filename) as file: 
        nb_routes = int(file.readline())
        liste_routes = []
        for i in range(int(nb_routes)):
            ligne = file.readline().split()
            liste_routes.append([int(ligne[0]),int(ligne[1]), int(ligne[2])])
        return liste_routes

#################

# Fonctions nécessaires pour la suite : détermination du meilleur camion pour couvrir un chemin


#format de la liste camions en entrée : camions[i] = puissance, coût, nom ; on suppose ici que la liste des camions est triée par puissance en entrée
#  -> complexité en log(len(camions))
#renvoie l'ensemble des camions capables de couvrir un chemin d'une puissance donnée

def camions_couvrant_dicho(puiss, camions):
    n = len(camions)
    x1=0
    x2=n-1
    if camions[n-1][0]-puiss<0:
        return [] #aucun camion ne convient
    if camions[0][0]-puiss>=0:
        return camions #tous les camions conviennent
    
    while True :
        x=(x1+x2)//2 
        if camions[x][0]-puiss==0:
            return camions[x:] #tous les camions de puissance supérieure conviennent
        elif camions[x][0]-puiss<0:
            x1 = x 
        else: 
            if camions[x-1][0]-puiss<0:
                return camions[x:] 
            else:
                x2=x

#################

#format de la liste camions en entrée : camions[i] = puissance, coût, nom ; on suppose ici que la liste des camions est triée par puissance en entrée
#renvoie le camion de coût minimnal

def camion_couvrant_opti(puiss,camions):      
    cam=camions_couvrant_dicho(puiss, camions)
    if cam==[]:
        return -1  #aucun camion ne convient
    else : 
         return min(cam,key=lambda camion: camion[1])[2]


def format(file_network,file_routein,file_camion): 
    network = graph_from_file(file_network)
    
    #format chemin
    routes = recuperation_routes(file_routein)
    chemins = []
    for route in routes:
        chemin_min_power = network.min_power_acm(route[0],route[1])
        chemins.append([chemin_min_power[0],chemin_min_power[1],route[2]])

    #format camion
    camions = []
    collection = collection_camions(file_camion)
    i = 0
    for camion in collection:
        camions.append([camion[0],camion[1],i])
        i +=1
    return (chemins,camions)


#################

### Algorithme glouton 


#format de la liste chemins en entrée : chemins[i] = [chemin = liste de noeuds], puissance du chemin, utilité du chemin
#format de la liste camions en entrée : camions[i] = puissance, coût, nom = position dans le catalogue (important pour ne pas les perdre en triant)

def knapsack_glouton(chemins,camions,budget=10**9):
    chemins_triee=sorted(chemins, key=lambda chemin: chemin[2])
    min_cout = min(camions,key=lambda camion: camion[1])[1]
    achats_camions=np.zeros(len(camions))
    chemins_couverts=[]
    utilite=0
    budget_restant=budget
    i=0
    while budget_restant>min_cout:
        puissancei=chemins_triee[i][1]
        camion=camion_couvrant_opti(puissancei,camions) 
        if camion==-1: #cas où aucun camion ne convient 
            continue
        elif camions[camion][1]<budget_restant:
            budget_restant-=camions[camion][1]
            achats_camions[camion]+=1
            chemins_couverts.append(chemins_triee[i])
            utilite+=chemins_triee[i][2]
    return(chemins_couverts,achats_camions,budget-budget_restant,utilite)

#################



### Algorithme de force brute 
# Principe : L'idée est de parcourir l'ensemble des possibilités représentées par des clés binaires, faciles à gérer

#format de la liste chemins en entrée : chemins[i] = [chemin = liste de noeuds], utilité du chemin, coût de couverture optimale, nom du camion de couverture optimale


def utilite(combinaison):
    u=0
    for chemin in combinaison:
        u+=chemin[1]
    return u

#################

def cout(combinaison):
    c=0
    for chemin in combinaison:
        c+=chemin[2]
    return c

#################

#format de la liste chemins en entrée : chemins[i] = [chemin = liste de noeuds], puissance du chemin, utilité du chemin
#format de la liste camions en entrée : camions[i] = puissance, coût, nom = position dans le catalogue 
# (important pour ne pas les perdre en triant)

def pre_process(chemins,camions):
    chemins_processed=[]
    for chemin in chemins:
        chemin_processed=chemin
        camion_opti=camion_couvrant_opti(chemin[1],camions)
        if camion_opti != -1: #cas où aucun camion ne convient
            chemin_processed.append(camions[camion_opti][1])
            chemin_processed.append(camion_opti)
            chemins_processed.append(chemin_processed)
    return(chemins_processed)

#################

#format de la liste chemins en entrée : chemins[i] = [chemin = liste de noeuds], utilité du chemin, coût de couverture optimale, nom du camion de couverture optimale

def post_process(chemins,camions):
    chemins_couverts=[]
    achats_camions=np.zeros(len(camions))
    for chemin in chemins:
        chemins_couverts.append(chemin[0])
        achats_camions[chemin[3]]+=1
    return chemins_couverts, achats_camions

#################


#format de la liste chemins en entrée : chemins[i] = [chemin = liste de noeuds], puissance du chemin, utilité du chemin
#format de la liste camions en entrée : camions[i] = puissance, coût, nom = position dans le catalogue (important pour ne pas les perdre en triant)
# Fonction très très coûteuse ....

def force_brute(chemins,camions,budget=10**9):
    n = len(chemins)
    univers = 2 ** n 
    meilleure_combinaison = []
    cout_mc=0
    utilite_mc=0


    # PRE PROCESSING pour le format
    chemins_processed = pre_process(chemins,camions)
 
    for cle in range(univers): 
        
        chaine_binaire = bin(cle)[2:]
        long = len(chaine_binaire)
        if long < n:
            chaine_binaire = (n - long) * '0' + chaine_binaire 

        combinaison = []
        for i in range(n):
            if chaine_binaire[i] == '1':
                combinaison.append(chemins_processed[i])
        
        utilite_temp = utilite(combinaison)
        cout_temp = cout(combinaison)

        if utilite_temp > utilite_mc:
            if cout_temp < budget:
                meilleure_combinaison = combinaison
                cout_mc=cout_temp
                utilite_mc=utilite_temp

        # POST PROCESSING pour le format
        chemins_couverts,achats_camions=post_process(meilleure_combinaison,camions)
        return(chemins_couverts,achats_camions,cout_mc,utilite_mc)

#################