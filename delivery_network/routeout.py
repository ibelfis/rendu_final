################  Fichier routeout.py  ################   
############################# IMPORTATIONS ################################# 
from graphe import *
from time import *


############################# Fonctions ################################# 
def routes_out(i):
     # générer le fichier route.out (T lignes : sur chaque ligne, puissance minimale pour parcourir la route et utilité)
    filename=f"projetpython2023/ensae-prog23-main/input/routes.{i}.in"
    filename_nv=f"projetpython2023/ensae-prog23-main/delivery_network/outputs/routes.{i}.out"
    network = f"projetpython2023/ensae-prog23-main/input/network.{i}.in"
    
    graphe = graph_from_file(network)
    arbre_couvrant= kruskal(graphe)
    
    rangs, peres = peres_rangs(1, arbre_couvrant)
    res=[]

    with open(filename) as file: #on ouvre le fichier
            ligne1=file.readline().split()
            nb_trajets=int(ligne1[0])
            debuttemps = perf_counter()
            for j in range(nb_trajets):
                lignej=file.readline().split() # i eme ligne du fichier file 
                utilite=str(lignej[2]) #on récupère l'utilité
                src=int(lignej[0]) # Premier noeud à relier 
                dest=int(lignej[1]) # Second noeud à relier
                chemin, p_min = min_power_update(src, dest, arbre_couvrant, peres, rangs)
                res.append((p_min, utilite))
            fintemps = perf_counter()
            temps=fintemps-debuttemps

    with open(filename_nv, "w") as file :
        for  element in res :
            puissance = element[0]
            utilite = element[1]
            file.write(f"{puissance} {utilite} \n")
    print(f"Fichier route {i} créé en {temps}")


for i in range(1,10):
    print(routes_out(i))
