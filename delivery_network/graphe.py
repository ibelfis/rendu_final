################  Fichier graphe.py  ################   
############################# IMPORTATIONS ################################# 

import numpy as np
import matplotlib.pyplot as plt
from jyquickhelper import RenderJsDot
import pydot
from time import perf_counter

############################# CLASSE Graph ################################# 
class Graph:
    def __init__(self, nodes=[]):
        self.nodes = nodes
        self.graph = dict([(n, []) for n in nodes])
        self.nb_nodes = len(nodes)
        self.nb_edges = 0
        self.edges = []
    
    #########

    def __str__(self):
        """Prints the graph as a list of neighbors for each node (one per line)"""
        if not self.graph:
            output = "The graph is empty"            
        else:
            output = f"The graph has {self.nb_nodes} nodes and {self.nb_edges} edges.\n"
            for source, destination in self.graph.items():
                output += f"{source}-->{destination}\n"
        return output
    
    #########

    # Méthode de la question 1 qui va nous permettre de compléter un graphe 
    def add_edge(self, node1, node2, power_min, dist=1):
        """
        Adds an edge to the graph. Graphs are not oriented, hence an edge is added to the adjacency list of both end nodes. 

        Parameters: 
        -----------
        node1: NodeType
            First end (node) of the edge
        node2: NodeType
            Second end (node) of the edge
        power_min: numeric (int or float)
            Minimum power on this edge
        dist: numeric (int or float), optional
            Distance between node1 and node2 on the edge. Default is 1.
        """
        self.nb_edges += 1
        self.graph[node1].append([node2, power_min, dist])
        self.graph[node2].append([node1, power_min, dist])
        return None
    
    #########

    # Création de la méthode get_path_with_power (question 3)
    # prend en entrée une puissance de camion p et un trajet t 
    # décide si un camion de puissance p peut couvrir le trajet t 
    # renvoie le chemin si possible

    def get_path_with_power(self, src, dest, power): # src, dest, power)
        # Vérification que les deux points sont dans la même composante fortement connexe
        composantes_connexes = self.connected_components()
        connectes=False
        for element in composantes_connexes:
            if (src and dest) in element: 
                composante = element
                connectes=True
        if not connectes :
            print("Les deux points ne sont pas connectés")
            return None
        #fin de la vérification
        
        # Trouver le chemin demandant le moins de "power" entre les deux points
        # Implémentation de l'algorithme de Djikstra
        
        
        cout = [float('inf')]*(len(self.nodes) +1)
        cout[src] = 0
        recuperer_chemin = [0]*(len(self.nodes) +1)
        
        #calcul du coût entre deux voisins dans une liste d'adjacence
        def calcul_cout(v1,v2):
            voisins2 = self.graph[v1]
            for element in voisins2:
                if element[0]==v2:
                    return element[1]
            raise ValueError("Les noeuds ne sont pas voisins")
             
        # implémentation d'un parcours en profondeur classique
        def explore_min_power(liste_comp):
            l=liste_comp
            
            while len(l) > 0:
                mini = cout[l[0]]
                for element in l:
                    
                    if cout[element]<=mini:
                        mini = cout[element]
                        sommet = element
                
                voisins = np.array(self.graph[sommet]).T[0]
                
                for voisin in voisins:
                    
                    cout_voisin = cout[sommet] + calcul_cout(sommet,voisin)
                    if cout_voisin < cout[voisin]:
                        cout[voisin] = cout_voisin
                        recuperer_chemin[voisin]=sommet
                    
                l.remove(sommet)
            chemin = [dest]
            while chemin[-1]!=src:
                chemin.append(recuperer_chemin[chemin[-1]])  
            return chemin[::-1]
        #cout est défini en variable donc on a accès au cout en faisant cout[dest]
        
        explore = explore_min_power(composante)
        
        if cout[dest] > power :
            print("Le camion ne dispose pas d'assez de puissance.")
            return None
        else:
            return explore
    
    #########

    # ON implémente également Djikstra
    # Mêmes arguments 

    def get_path_with_distance(self, src, dest): 

        # Vérification que les deux points sont dans la même composante fortement connexe
        composantes_connexes = self.connected_components()
        connectes=False
        for element in composantes_connexes:
            if (src and dest) in element: 
                composante = element
                connectes=True
        if not connectes :
            print("Les deux points ne sont pas connectés")
            return None
        #fin de la vérification
        
        # Trouver le chemin demandant le moins de distance entre les deux points
        # Implémentation de l'algorithme de Djikstra
            
            
        cout = [float('inf')]*(len(self.nodes) +1)
        cout[src] = 0
        
            
        recuperer_chemin = [0]*(len(self.nodes) +1)
            
        #calcul de la distance entre deux voisins dans une liste d'adjacence
        def calcul_distance(v1,v2):
            voisins2 = self.graph[v1]
            for element in voisins2:
                if element[0]==v2:
                    return element[2]
            raise ValueError("V1 et V2 ne sont pas voisins")         
            
        def explore_min_distance(liste_comp):
            l=liste_comp
                
            while len(l) > 0:
                mini = cout[l[0]]
                for element in l:
                        
                    if cout[element]<=mini:
                        mini = cout[element]
                        sommet = element
                    
                voisins = np.array(self.graph[sommet]).T[0]
                    
                for voisin in voisins:
                        
                    cout_voisin = cout[sommet] + calcul_distance(sommet,voisin)
                    if cout_voisin < cout[voisin]:
                        cout[voisin] = cout_voisin
                        recuperer_chemin[voisin]=sommet
                        
                l.remove(sommet)
            chemin = [dest]
            while chemin[-1]!=src:
                chemin.append(recuperer_chemin[chemin[-1]])  
            return chemin[::-1]
        #cout est défini en variable donc on a accès au cout en faisant cout[dest]
            
        explore = explore_min_distance(composante)
        return explore
    
    #########


    #  méthode connected_components_set qui trouve les composantes connectées du graphe
    # on va implémenter un parcours en profondeur du graphe assez classique en utilisant une fonction récursive

    def connected_components(self):
        composantes_connecte = []
        visite = {noeud : False for noeud in self.nodes}
        
        def dfs(noeud):
            composante = [noeud]
            for voisin in self.graph[noeud]:
                voisin = voisin[0]
                if not visite[voisin]:
                    visite[voisin] = True
                    composante += dfs(voisin)
            return composante
        
        for noeud in self.nodes:
            if not visite[noeud]:
                composantes_connecte.append(dfs(noeud))
        return composantes_connecte
    

    #########
    # calculer, pour un trajet t donné, la puissance minimale un camion pouvant couvrir ce trajet. 
    # La fonction retourne le chemin, et la puissance minimale.

    def min_power(self,trajet):
        #Vérifier qu'un camion peut bien effectuer le trajet
        # Pour cela on vérifie que tous les noeuds de trajet sont dans la même composante fortement connexe 

        composantes_connexes = self.connected_components()
        for noeud in trajet:
            for composante in composantes_connexes:
                if noeud not in composante:
                    composantes_connexes.remove(composante) 
        if len(composantes_connexes)<1:
            print("Le trajet proposé présente des noeuds qui ne sont pas connectés.")
            return None
        else:

            #Il reste alors dans composantes_connexes seulement la composante_connexe qui nous intéresse 
            #Nous voulons désormais la puissance minimale de notre camion pour effectuer le trajet
            #On prend le chemin demandant le moins de "power"
            chemin = self.get_path_with_power(trajet[0], trajet[1], float('inf'))
            
            #On calcul la puissance de ce chemin
            def calcul_cout(v1,v2):
                voisins2 = self.graph[v1]
                for element in voisins2:
                    if element[0]==v2:
                        return element[1]
                raise ValueError("V1 et V2 ne sont pas voisins")
            
            power = 0
            for i in range(len(chemin)-1):
                power = max(power,calcul_cout(chemin[i],chemin[i+1]))
        return (power, chemin)
    

    #########

    #Implémenter une représentation graphique du graphe, du trajet, et du chemin trouvé. 
"""""
        def plot_network(graphe):
        #on cherche à représenter le graphe

        rows = pydot.Dot(graph_type='digraph')

        for i in range(1,graphe.nb_nodes+1):
            rows.add_edge(pydot.Edge("  %d;" % i))   
        visited = [False]*(graphe.nb_nodes +1)
        visited[0]= True #on n'utilise pas cet emplacement
        for i in range(1,graphe.nb_nodes+1):
            visited[i]= True
            for j in range(len(graphe.graph[i])):
                if not visited[graphe.graph[i][j][0]]:
                    visited[graphe.graph[i][j][0]] = True
                    rows.add_edge(pydot.Edge("  %d -> %d;" % (i, graphe.graph[i][j][0]))) 
        rows.write_png('test.png')

"""
############################# FONCTIONS #################################      
        

#Fonction qui permet de charger un fichier (c'est la question 4)
def graph_from_file(filename):
    #récupération des données du file
    with open(filename) as file:
        ligne1 = file.readline().split()
        n = int(ligne1[0])
        m = int(ligne1[1])
        nodes = [i for i in range(1,n+1)]
        G = Graph(nodes)
        for i in range(m):
            ligne_i = file.readline().split()
            node1 = int(ligne_i[0])
            node2 = int(ligne_i[1])
            power_min = int(ligne_i[2])
            if len(ligne_i)>3:
                dist = int(ligne_i[3])
                G.add_edge(node1, node2, power_min, dist)
                G.edges.append([node1,node2,power_min,dist])
            else: 
                G.add_edge(node1,node2,power_min,dist=1)
                G.edges.append([node1,node2,power_min,1])
    return G


############################# Kruskal et ses amis ################################# 


    
################# 

def kruskal(graphe):
    # algorithme de Kruskal pour calculer un arbre couvrant minimal 
    arbre_couvrant = Graph(graphe.nodes)
    edges_sorted = sorted(graphe.edges, key = lambda arrete : arrete[2])
    parent = list(range(graphe.nb_nodes)) #on initialise la liste représentant les sous-ensembles, chaque noeud est parent de lui-même à l'initialisation

    compt=0 #un arbre a au max nb_nodes -1 arêtes, donc on ajoute une variable compteur

    def find(parent, x):
    # opération de find d' l'union-find
        if parent[x] != x:
            parent[x]=find(parent, parent[x])
        return parent[x] #père de x

    for arete in edges_sorted : #opération d'union en coût log (structure d'arbre de profondeur 
        n1= arete[0] -1 
        n2=arete[1] -1
        a=arete[0]

        pere1=find(parent, n1)
        pere2=find(parent, n2)

        if pere1 != pere2 :
            parent[pere1] = pere2 

            if len(arete)>3:
                arbre_couvrant.add_edge(arete[0], arete[1], arete[2], arete[3])   
            else :
                arbre_couvrant.add_edge(arete[0], arete[1], arete[2])  
    
    return arbre_couvrant

################# 





def min_power_update(src, dest, arbre_couvrant, peres, rangs):
    # L'idée est de capitaliser sur la structure d'arbre couvrant minimal
    # On définit une racine arbitrairement, puis on recherche les chemins qui vont à la racine en regardant leur rang par rapport à la racine
    # (c'est assez similaire à notre méthode d'implémentation de la structure d'unionfind)

    #on exclut le cas trivial
    if src == dest :
        return ([src],0)

    c_src=[src] 
    c_dest=[dest]

    rang_dest= rangs[dest]
    rang_src= rangs[src]

    
    #le but est d'amener le noeud dont le rang est le plus grand
    #au niveau du rang de l'autre noeud, pour remonter ensuite en même temps jusqu'au parent commun
    if rang_src>rang_dest :
        while rang_src!= rang_dest :
            src=peres[src]
            if src==dest :
                c_src.append(src)
                c_dest=[]
                break
            else :
                rang_src = rangs[src]
                c_src.append(src)


    if rang_dest>rang_src :
        while rang_src!= rang_dest :
            dest=peres[dest]
            if src==dest:
                c_dest.append(dest)
                c_src=[]
                break
            
            else :
                rang_dest = rangs[dest]
                
                c_dest.append(dest)
    
    if peres[src]==peres[dest] and src!=dest :
        src1=peres[src]
        
        c_src.append(src1)

    #Une fois que les noeuds sont à la même hauteur, on remonte jusqu'au parent commun
    while peres[src]!=peres[dest]:
        c_src.append(peres[src])
        c_dest.append(peres[dest])
        src=peres[src]
        dest=peres[dest]
    

        c_src.append(peres[src])

    c_dest.reverse()
    chemin = c_src + c_dest

    puissances = []
    p_min = -1 

    for i in range (len(chemin)-1):
        key = chemin[i]
        

        for e in arbre_couvrant.graph[key]:

            if e[0]==chemin[i+1]:
                puissances.append(e[1])
    
    if len(puissances)!=0 :
        p_min=max(puissances)
    return (chemin, p_min)
# chemin : liste contenant les noeuds composant le chemin le plus économique en puissance entre src et dest
# p_min : puissance minimale que le camion doit posséder pour rejoindre les deux noeuds.



## Pré processing pour avoir les bons formats en entrée de min_power_updat

def rang_noeud(node, rang, parent, graphe, rangs, peres):
    rangs[node]= rang 
    peres[node]= parent 

    for voisin in graphe.graph[node] :
        if voisin[0] != parent : 
            rang_noeud(voisin[0], rang +1, node, graphe, rangs, peres)


def peres_rangs(racine, graphe) :
    rangs={} #on initialise
    peres ={} # on initialise

    rang_noeud(racine, 0, -1, graphe, rangs, peres) 
    return rangs, peres # un dictionnaire des rangs et un dictionnaires des peres