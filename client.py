import socket


hote = "127.0.0.1"
port = 9998
connexionServeur = socket.socket()
connexionServeur.connect((hote, port))
print("Connection établie vers " + format(port))

chaineAEnvoyer = ""
while (chaineAEnvoyer != "quit"):
    data = connexionServeur.recv(255).decode()
    chaineAEnvoyer = input("> " + data)
    connexionServeur.send(chaineAEnvoyer.encode())

print("Fermeture de la connexion")
connexionServeur.close()
