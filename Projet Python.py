import os
import csv
import math
from math import *
import matplotlib.pyplot as plt
print(os.getcwd())

os.chdir("C:/Users/") #chemin pour aller chercher le fichier csv à adapter

fichier=open("EIVP_KM.csv") 
excel = csv.reader(fichier) #on ouvre le fichier avec le module csv


def tableau(C):                      #on fait une fonction qui permet de créer un tableau sous format liste de listes comprenant des entiers et des flottants 
    T=[]
    for ligne in C:
        carac=''.join(ligne)
        T.append(carac.split(';'))
    n=len(T)
    for i in range (1,n):
        T[i][0]=int(T[i][0])
        T[i][1]=int(T[i][1])
        for k in range(2,7):
            T[i][k]=float(T[i][k])
    return T

T= tableau(excel) 
n=len(T)             #on définit en variable globale notre tableau T ainsi que sa longueur n



#p correspond au numéro de la colonne
#c correspond au numéro du capteur


def separationcapteur(c):          #seule alternative trouvée pour pouvoir initialiser correctement le xmin
    C1=[]                          #de la fonction suivante
    C2=[]
    C3=[]
    C4=[]
    C5=[]
    C6=[]
    T2=[]
    for i in range(1,n):
        if T[i][1]==1 :
            C1.append(T[i])
        elif T[i][1]==2:
            C2.append(T[i])
        elif T[i][1]==3:
            C3.append(T[i])
        elif T[i][1]==4:
            C4.append(T[i])
        elif T[i][1]==5:
            C5.append(T[i])
        else :
            C6.append(T[i])
    T2=[C1,C2,C3,C4,C5,C6]
    return T2[c-1]

#       p=0 -> inutile
#       p=1 -> numéro du capteur (p=1 représente c)
#       p=2 -> l'intensité sonore en dBA
#       p=3 -> température en °C
#       p=4 -> l'humidité relative en %
#       p=5 -> l'indice lumineux en lux
#       p=6 -> quantité de CO2 en ppm
#       p=7 -> date du relevé


def min(p, c):
    Tmin=separationcapteur(c)
    xmin=Tmin[1][p]
    for i in range(1,len(Tmin)):
            if xmin>Tmin[i][p]:
                xmin=Tmin[i][p]
    return xmin


def maxi(p, c):
    xmax=0                       #car toutes les valeurs du tableau CSV sont positives !!
    for i in range(1,n):
        if T[i][1]==c:
             if xmax<T[i][p]:
                xmax=T[i][p]
    return xmax


def moyenne(p,c):
    s=0
    m=len(separationcapteur(c))
    for i in range(1,n):
        if T[i][1]==c:
            s+=T[i][p]
    return s/m


def variance(p,c):
    sc=0
    m=len(separationcapteur(c))
    for i in range(1,n):
        if T[i][1]==c:
            sc+=T[i][p]*T[i][p]
    return (sc*1./m)-(moyenne(p,c)**2)


def ecarttype(p, c):
    return variance(p, c)**0.5


def indicehumidex(c):
    L=separationcapteur(c)
    m=len(separationcapteur(c))
    HUMIDEX=[[0,0] for i in range(1,m+1)]
    for j in range(1,m):
        HUMIDEX[j][0]=L[j][1]
        HUMIDEX[j][1]=(L[j][3]+5./9*(6.112*10**(7.5*L[j][3]/(237.7+L[j][3])-10))*L[j][4]/100)
    return HUMIDEX

#on renvoie une liste de liste comportant 2 éléments, le numéro du capteur et l'indice humidex pour ensuite

#pouvoir plus facilement utiliser les algorithmes précédents pour calculer les moyennes/variances/etc

#on effectue un tri rapide car il y a un grand nombre de valeur à trier, donc il faut faire attention à la complexité !

#et le tri fusion à une complexité linéaire, mais ne convient pas pour les grandes listes car sa complexité spaciale est

#beaucoup trop importante


def tri(p):
    liste_g=[]
    liste_d=[]
    for i in range(2,n):
        if T[i][p]<=T[1][p]:
            liste_g.append(T[i][p])
        else:
            liste_d.append(T[i][p])
    return tri(liste_g)+[T[1][p]]+tri(liste_d)

#le programme affiche une erreur mais nous ne comprenons pas pourquoi 


def mediane(p):
    M=tri(p)
    if n!=0%2:
        return M[(n-1)/2]                      #Attention, ne pas rajouter le +1 car en numéro de liste ca renvoie 
    else :                                     #le cran d'après automatiquement
        return (M[(n-2)/2]+M[n/2])/2


def correlation(p1, p2, c):
    s=0
    d=0
    for i in range(1,n):
        if T[i][1]==c:
            s+=T[i][p1]-moyenne(p1,c)
            d+=T[i][p2]-moyenne(p2,c)
    return (s*d)/(ecarttype(p1, c)*ecarttype(p2, c))

def similarites(c1, c2, p, i):           #c1 est le capteur dit de "référence" et i est l'intervalle de confiance
    m1=moyenne(p, c1)
    m2=moyenne(p, c2)
    if m1-m2<=i and m1-m2>=-i :
        return 'similaires'
    else :
        return 'pas similaires'


def courbesimilarites(c, p, i) :
    m=moyenne(p, c)
    sup=m+i
    inf=m-i
    X=[j for j in range(10)]                  #liste peu importante, juste pour que ca soit lisible graphiquement
    plt.plot(X,m, label='capteur référence')
    plt.plot(X,sup, label='borne supérieure')
    plt.plot(X,inf, label='borne inférieure')
    for l in range(1,7):                      #les capteurs vont du numéro 1 au numéro 6
        if l!=c :
            if l==1 :
                plt.plot(X,[moyenne(p,1) for h in range(10)], label='capteur 1')  #pour que les deux listes aient la même dimension
            elif l==2 :
                plt.plot(X,[moyenne(p,2) for h in range(10)], label='capteur 2')
            elif l==3 :
                plt.plot(X,[moyenne(p,3) for h in range(10)], label='capteur 3')
            elif l==4 :
                plt.plot(X,[moyenne(p,4) for h in range(10)], label='capteur 4')
            elif l==5 :
                plt.plot(X,[moyenne(p,5) for h in range(10)], label='capteur 5')
            else :
                plt.plot(X,[moyenne(p,6) for h in range(10)], label='capteur 6')
    plt.show()

#les programmes courbesimilarites et courbe renvoient une erreur mais nous ne comprenont pas pourquoi

def courbe (c):
    X=[0]
    Y1=[]    
    Y2=[]    
    Y3=[]    
    Y4=[]    
    Y5=[]
    fig,ax= plt.subplots(nrows=1,ncols=5)
    for i in range (1,n):
        if T[i][1]==c:            
            X.append(T[i][-1])            
            Y1.append(T[i][2])            
            Y2.append(T[i][3])
            Y3.append(T[i][4])
            Y4.append(T[i][5])                                    
    ax[0].plot(X,Y1,label='niveau sonore')
    ax[0].set(Xlabel='temps',Ylabel='niveau sonore(dB)',title='niveau sonore en fonction du temps pour le capteur'+str(c))
    ax[0].grid(True)
    ax[1].plot(X,Y2,label='température')
    ax[1].set(Xlabel='temps',Ylabel='température (°C)',title='température en fonction du temps pour le capteur'+str(c))
    ax[1].grid(True)
    ax[2].plot(X,Y3,label='humidité')
    ax[2].set(Xlabel='temps',Ylabel='humidité',title='humidité en fonction du temps pour le capteur'+str(c))
    ax[2].grid(True)
    ax[3].plot(X,Y4,label='luminosité')
    ax[3].set(Xlabel='temps',Ylabel='luminosité (lux)',title='luminosité en fonction du temps pour le capteur'+str(c))
    ax[3].grid(True)
    ax[4].plot(X,Y5,label='quantité de CO2')
    ax[5].set(Xlabel='temps',Ylabel='quantité de CO2 (ppm)',title='quantité de CO2 en fonction du temps pour le capteur'+str(c))
    ax[5].grid(True)
    plt.show()

plt.close()

