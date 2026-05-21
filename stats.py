import matplotlib.pyplot as plt
import csv
from toolbox import *

def get_res():
    "Renvoie le dictionnaire des résultats obtenu"
    f = open("resultats.csv", "r")
    content = csv.reader(f)
    dico = {}
    for line in content :
        dico[line[0]] = line[1]
    return dico


def afficher_reflexion_times(res):
    "Affichage du temps de réflexion par partie"
    n = int(res["Nombre de parties total"])
    J1_reflexion_times = obtenir_liste(res["J1 : Temps de reflexion par partie"], float)
    J2_reflexion_times = obtenir_liste(res["J2 : Temps de reflexion par partie"], float)
    parties = range(1, n+1)
    plt.plot(parties, J1_reflexion_times, "b-")
    plt.plot(parties, J2_reflexion_times, "r-")
    plt.xlabel("Partie Numéro :")
    plt.ylabel("Temps de réflexion total (en s)")
    plt.show()

def afficher_rt_par_coup(res):
    m = obtenir_mat(res["J1 : Temps de reflexion par coup"], float)
    count = 0
    for e in m[0]:
        count += 1
    x = range(count)
    plt.plot(x, m[0])
    plt.show()

res = get_res()
afficher_rt_par_coup(res)