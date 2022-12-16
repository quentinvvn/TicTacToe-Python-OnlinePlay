# /usr/bin/env python3
# voir https://docs.python.org/3/library/socket.html

import socket
import pickle

socket = socket.socket()
socket.bind(("127.0.0.1", 9998))
socket.listen(5)

print("En attente d'un adversaire...")
connexionClient, adresse = socket.accept()
print("Connection établie depuis " + format(adresse))


def creerGrille():
    return ['.' for i in range(3*3)]


def jouerPartie(m):
    while (m[0] == '.' or m[1] == '.' or m[2] == '.' or m[3] == '.' or m[4] == '.' or m[5] == '.' or m[6] == '.' or m[7] == '.' or m[8] == '.'):
        if (m[0] == m[1] == m[2] == 'X' or (m[0] == m[1] == m[2] == 'O')):
            if (m[0] == 'X'):
                return True
            else:
                return False
        elif (m[3] == m[4] == m[5] == 'X' or (m[3] == m[4] == m[5] == 'O')):
            if (m[3] == 'X'):
                return True
            else:
                return False
        elif (m[6] == m[7] == m[8] == 'X' or (m[6] == m[7] == m[8] == 'O')):
            if (m[6] == 'X'):
                return True
            else:
                return False
        elif (m[0] == m[3] == m[6] == 'X' or (m[0] == m[3] == m[6] == 'O')):
            if (m[0] == 'X'):
                return True
            else:
                return False
        elif (m[1] == m[4] == m[7] == 'X' or (m[1] == m[4] == m[7] == 'O')):
            if (m[1] == 'X'):
                return True
            else:
                return False
        elif (m[2] == m[5] == m[8] == 'X' or (m[2] == m[5] == m[8] == 'O')):
            if (m[2] == 'X'):
                return True
            else:
                return False
        elif (m[0] == m[4] == m[8] == 'X' or (m[0] == m[4] == m[8] == 'O')):
            if (m[0] == 'X'):
                return True
            else:
                return False
        elif (m[6] == m[4] == m[2] == 'X' or (m[6] == m[4] == m[2] == 'O')):
            if (m[6] == 'X'):
                return True
            else:
                return False
        print("En attente du jeu de " + nomJoueur1)
        tourJoueur1(m)
        if (m[0] == '.' or m[1] == '.' or m[2] == '.' or m[3] == '.' or m[4] == '.' or m[5] == '.' or m[6] == '.' or m[7] == '.' or m[8] == '.'):
            attente = "En attente du jeu de " + nomJoueur2
            connexionClient.send(attente.encode())
            tourJoueur2(m)

    else:
        return None


def tourJoueur1(m):
    Col = "> Veuillez entrer la colonne sur laquelle vous souhaitez jouer : "
    data = "| " + m[(3*0)+0] + " | " + m[(3*0)+1] + " | " + m[(3*0)+2] + " |\n> | " + m[(3*1)+0] + " | " + m[(3*1)+1] + " | " + m[(3*1)+2] + " |\n> | " + m[(3*2)+0] + " | " + m[(3*2)+1] + " | " + m[(3*2)+2] + " |" + "\n" + Col
    connexionClient.send(data.encode())
    Col = int(connexionClient.recv(255).decode())
    Lign = "Veuillez entrer la ligne où vous souhaitez jouer : "
    connexionClient.send(Lign.encode())
    Lign = int(connexionClient.recv(255).decode())
    Col -= 1
    Lign -= 1
    if (Col < 0 or Col > 2 or Lign < 0 or Lign > 2):
        error = "Valeures incorrectes, la colonne et la ligne doivent être comprises entre 0 et 2\n"
        connexionClient.send(error.encode())
        tourJoueur1(m)
    elif (m[(3*Lign)+Col] == '.'):
        ecrireValeurGrille(m, Col, Lign, 'X')
    else:
        error = "------------------------ \n> L'espace est déjà occupé \n> ------------------------"
        connexionClient.send(error.encode())
        tourJoueur1(m)


def tourJoueur2(m):
    afficherGrille(m)
    Col = int(
        input("> Veuillez entrer la colonne sur laquelle vous souhaitez jouer : "))
    Lign = int(input("> Veuillez entrer la ligne où vous souhaitez jouer : "))
    Col -= 1
    Lign -= 1
    if (Col < 0 or Col > 2 or Lign < 0 or Lign > 2):
        print("Valeures incorrectes, la colonne et la ligne doivent être comprises entre 0 et 2")
        tourJoueur2(m)
    elif (m[(3*Lign)+Col] == '.'):
        ecrireValeurGrille(m, Col, Lign, 'O')
    else:
        print("------------------------")
        print("L'espace est déjà occupé")
        print("------------------------")
        tourJoueur2(m)


def lireValeurGrille(m, i, j):
    return m[(3*j)+i]


def ecrireValeurGrille(m, i, j, valeur):
    m[(3*j)+i] = valeur


def afficherGrille(m):
    ligne = 0
    while ligne < 3:
        colonne = 0
        while colonne < 3:
            print('|', lireValeurGrille(m, colonne, ligne), end=' | ')
            colonne = colonne+1
        print("")
        ligne = ligne+1


reponse = ""
print("Le serveur est en attente des messages du client...")
while True:
    reponse = "Bonjour, vous serez le Joueur 1, vous jourez les 'X'. Veuillez entrer votre prénom: "
    connexionClient.send(reponse.encode())
    nomJoueur1 = connexionClient.recv(255).decode()
    nomJoueur2 = input("> Vous allez jouer contre " + nomJoueur1 +
                       " vous serez les 'O'. Veuillez entrer votre prénom: ")

    m = creerGrille()
    jouerPartie(m)

    if (jouerPartie(m) == True):
        afficherGrille(m)
        print(nomJoueur1 + " vous a battu !")
        win = "Félicitations " + nomJoueur1 + " vous avez battu " + nomJoueur2
        connexionClient.send(win.encode())
    elif (jouerPartie(m) == False):
        afficherGrille(m)
        print("Félicitations " + nomJoueur2 + " vous avez battu " + nomJoueur1)
        loose = nomJoueur2 + " vous a battu !"
        connexionClient.send(loose.encode())
    elif (jouerPartie(m) == None):
        print("Égalité !")
        egality = "Égalité !"
        connexionClient.send(egality.encode())

    print("(1) Oui (2) Non")
    replay = int(input("Souhaitez vous rejouer ? "))
    if (replay == 2):
        print("Au revoir !")
        stop = nomJoueur2 + "a décidé d'arrêté de jouer, au revoir !"
        connexionClient.send(stop.encode())
        break

    replay = "(1) Oui (2) Non \nSouhaitez vous rejouer ? "
    connexionClient.send(replay.encode())
    replay = int(connexionClient.recv(255).decode())
    if (replay == 2):
        print(nomJoueur1 + "a décidé d'arrêté de jouer, au revoir !")
        stop = "Au revoir !"
        connexionClient.send(stop.encode())
        break

    m = creerGrille()
    jouerPartie()

print("Fermeture de la connexion")
connexionClient.close()
socket.close()
