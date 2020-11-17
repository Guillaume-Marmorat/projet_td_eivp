import os
import csv
print(os.getcwd())
os.chdir("C:/Users/Guillaume/Documents/EIVP/IVP1/Info")
fichier=open("EIVP_KM.csv")
ficher.close()
excel = csv.reader(fichier)

def liste(C):
    T=[]
    for ligne in C:
        T.append(ligne)
    return (T)

