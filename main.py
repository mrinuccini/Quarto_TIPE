#Importations
from game import *


#Lancement du jeu
n = input("Combien de parties au total ? (défaut: 1) ")
if n=="":
    n=1
else:
    n = int(n)
game = Game(n)