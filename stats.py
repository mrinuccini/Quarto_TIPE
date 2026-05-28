"Statistiques en fin de jeu"

#Importations
import matplotlib.pyplot as plt
import csv
from toolbox import *
from stats_class import *

def get_res():
    "Renvoie le dictionnaire des résultats obtenu"
    f = open("resultats.csv", "r")
    content = csv.reader(f)
    dico = {}
    for line in content :
        dico[line[0]] = line[1]
    return dico

def get_game_data():
    "Renvoie les statistiques associées au joueur i (i=0 => statistiques générales)"
    res = get_res()
    g = Game_data()

    g.set_nb_parties(int(res["Nombre de parties total"]))
    g.set_n_nulles(int(res["Nombre de parties nulles"]))
    g.push_victoires(int(res["J1 : Nombre de victoires"]))
    g.push_victoires(int(res["J2 : Nombre de victoires"]))
    g.set_max_tour(int(res["Nombre de tour max"]))
    
    for i in range(1,3):
        j = stat()
        j.set_total_rt(float(res[f"J{i} : Temps total de reflexion"]))
        l = obtenir_liste(res[f"J{i} : Temps de reflexion par partie"], float)
        j.set_partie_rt(l)
        m = obtenir_mat(res[f"J{i} : Temps de reflexion par coup"], float)
        j.set_reflexion_time(m)
        g.push_joueur(j)
        g.push_type(res[f"J {i} : Type de joueur"])

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
    "Renvoie le temps de réflexion moyen au tour i de la matrice m pour le joueur jidx"
    n = game_data.get_n_parties()
    s = 0
    for k in range(n):
        if i<len(game_data.get_joueur(jidx).get_reflexion_time()[k]):
            s += game_data.get_joueur(jidx).get_reflexion_time()[k][i]
    return s / n

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
    


game_data = get_game_data()
affich_rt_moyen(game_data)