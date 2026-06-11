from player import *
from time import sleep
from zobrist import Zobrist
import pickle
import csv

def get_res(name="resultats"):
    "Renvoie le dictionnaire des résultats obtenus"
    f = open(name+".csv", "r")
    content = csv.reader(f)
    dico = {}
    for line in content :
        dico[line[0]] = line[1]
    return dico

def get_game_data(name="resultats"):
    "Renvoie les statistiques associées au jeu"
    res = get_res(name)
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