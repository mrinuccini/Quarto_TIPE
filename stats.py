"Statistiques en fin de jeu"

#Importations
import matplotlib.pyplot as plt
import csv
from toolbox import *
from stats_class import *

def get_res():
    "Renvoie le dictionnaire des résultats obtenus"
    f = open("resultats.csv", "r")
    content = csv.reader(f)
    dico = {}
    for line in content :
        dico[line[0]] = line[1]
    return dico

def get_game_data():
    "Renvoie les statistiques associées au jeu"
    res = get_res()
    g = Game_data()

    g.set_nb_parties(int(res["Nombre de parties total"]))
    g.set_n_nulles(int(res["Nombre de parties nulles"]))
    g.push_victoires(int(res["J1 : Nombre de victoires"]))
    g.push_victoires(int(res["J2 : Nombre de victoires"]))
    g.set_max_tour(int(res["Nombre de tour max"]))
    
    for i in range(1,3):
        typ = res[f"J{i} : Type de joueur"][1:]
        j = stat(typ)
        j.set_total_rt(float(res[f"J{i} : Temps total de reflexion"]))
        l = obtenir_liste(res[f"J{i} : Temps de reflexion par partie"], float)
        j.set_partie_rt(l)
        m = obtenir_mat(res[f"J{i} : Temps de reflexion par coup"], float)
        j.set_reflexion_time(m)
        g.push_type(typ)
        if typ=="MinMax":
            m = obtenir_mat(res[f"J{i} : Pronfondeurs atteintes"], int)
            j.set_prof(m)
        g.push_joueur(j)
       
    return g


def afficher_reflexion_times(game_data:Game_data):
    "Affichage du temps de réflexion par partie"
    n = game_data.get_n_parties()
    J1_reflexion_times = game_data.get_joueur(1).get_partie_reflexion_time()
    J2_reflexion_times = game_data.get_joueur(2).get_partie_reflexion_time()
    parties = range(1, n+1)
    plt.plot(parties, J1_reflexion_times, "b-")
    plt.plot(parties, J2_reflexion_times, "r-")
    plt.xlabel("Partie Numéro :")
    plt.ylabel("Temps de réflexion total (en s)")
    plt.show()

def obtenir_rt_au_tour(game_data:Game_data, jidx, i):
    "Renvoie le temps de réflexion moyen au tour i de gmae data pour le joueur jidx"
    n = game_data.get_n_parties()
    s = 0
    n2 = 0
    for k in range(n):
        if i<len(game_data.get_joueur(jidx).get_reflexion_time()[k]):
            s += game_data.get_joueur(jidx).get_reflexion_time()[k][i]
            n2 += 1
    if n2==0:
        return 0
    return s / n2

def affich_rt_moyen(game_data:Game_data):
    max_tour = game_data.get_max_tour()
    J1 = []
    J2 = []
    for i in range(max_tour):
        J1 += [obtenir_rt_au_tour(game_data, 1, i)]
        J2 += [obtenir_rt_au_tour(game_data, 2, i)]
    
    x = range(max_tour)

    plt.plot(x, J1, "r-",label=f"J1 {game_data.get_type()[0]}")
    plt.plot(x, J2, "b-", label=f"J2 {game_data.get_type()[1]}")
    plt.legend()
    plt.title("Temps de réflexion moyen selon le tour")
    plt.xlabel("Numéro du tour")
    plt.ylabel("Temps de réflexion (en s)")
    plt.show()
    
def get_nb_tour_partie(game_data:Game_data):
    "Renvoie le nombre de tour par partie"
    n = []
    m = game_data.get_joueur(1).get_reflexion_time()
    l = [2*len(k) for k in m]
    return l

def affich_prof_partie(game_data:Game_data,jidx,  partie_idx):
    "Affiche les différentes profondeurs atteintes pour MinMax du joueur jidx (commence à 1) à la partie idx (commence à 0)"
    joueur = game_data.get_joueur(jidx)
    prof = None
    if joueur.get_type()=="MinMax":
        y = []
        prof = joueur.get_prof()
        assert(partie_idx<len(prof))
        for e in prof[partie_idx]:
            y += [e]
    N=len(prof[partie_idx])

    x = range(N)
    plt.plot(x, y, "r-", label=f"J{jidx}")
    plt.title(f"Profondeurs atteintes à la partie {partie_idx}")
    plt.xlabel("Tour numéro")
    plt.ylabel("Profondeur maximale atteinte")
    plt.plot(0,0, label="O")
    plt.show()


def obtenir_profondeur_au_tour(game_data:Game_data, jidx, i):
    "Renvoie la profondeur moyenne au tour i de la matrice m pour le joueur jidx"
    n = game_data.get_n_parties()
    s = 0
    n2 = 0
    for k in range(n):
        if i<len(game_data.get_joueur(jidx).get_prof()[k]):
            s += game_data.get_joueur(jidx).get_prof()[k][i]
            n2 += 1
    if n2==0:
        return 0
    return s / n2

def affich_prof(game_data:Game_data, jidx):
    "Affiche les différentes profondeurs atteintes pour MinMax du joueur jidx (commence à 1) "
    joueur = game_data.get_joueur(jidx)
    prof = None
    if joueur.get_type()=="MinMax":
        y = []
        prof = joueur.get_prof()

    max_tour = game_data.get_max_tour()
    m = [] 
    for i in range(max_tour):
        m += [obtenir_profondeur_au_tour(game_data, jidx, i)]
    
    x = range(max_tour)

    plt.plot(x, m, "r-", label=f"J{jidx}")
    plt.title(f"Profondeurs atteintes moyennes")
    plt.xlabel("Tour numéro")
    plt.ylabel("Profondeur maximale atteinte")
    plt.plot(0,0, label="O")
    plt.show()  

def get_moyenne_par_coup(game_data:Game_data, jidx):
    "Renvoie le temps de réflexion total moyen sur toutes les parties du joueur jidx (commence à 1)"
    assert(jidx in (1,2))
    y = game_data.get_joueur(jidx).get_reflexion_time()

    #On compte le nombre de coups joués au total
    n = 0
    for i in range(len(y)):
        ligne = y[i]
        for j in range(len(ligne)):
            n += 1

    moy = game_data.get_joueur(jidx).get_total_reflexion_times() / n
    return moy

game_data = get_game_data()
# print(get_nb_tour_partie(game_data))
#affich_rt_moyen(game_data)

print(get_moyenne_par_coup(game_data,1))