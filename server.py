import random
import threading
import socket, time

clients = []
XorO = ['X', 'O']
start = "False"

def main():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind(('localhost', 7747))
        server.listen(3)
    except:
        return print('\nNão foi possível iniciar o servidor!\n')

    while True:
        client, addr = server.accept()
        clients.append(client)

        thread1 = threading.Thread(target=messagesTreatment, args=[client])
        thread2 = threading.Thread(target=definirLado)

        thread1.start()
        thread2.start()


def messagesTreatment(client):
        while True:
            try:
                print(len(clients))
               
                if len(clients) >= 2: 
                    time.sleep(2)
                    global start
                    start = "True"
                    aguardando(start)  
                    msg = client.recv(2048)
                    broadcast(msg, client) 
                elif len(clients) < 2:
                    time.sleep(0.2)
                    print("Aqui1")
                    start = "False"
                    aguardando(start)   
                    print("Aqui") 
            except:
                deleteClient(client)
                break
def definirLado():
    if len(clients) >= 2 and start == "False":   
        lado = random.choice(XorO)
        vez = random.choice(XorO)
        valor1 = f"lado {lado}, {vez}"
        valor2 = f'lado O, {vez}' if lado == 'X' else f'lado X, {vez}'
        print(type(valor1.encode('utf-8')))
        clients[0].send(valor1.encode('utf-8'))
        clients[1].send(valor2.encode('utf-8'))
   
        


def broadcast(msg, client):
    for clientItem in clients:
        if clientItem != client:
            try:
                clientItem.send(msg)
            except:
                print("vish")
                deleteClient(clientItem)

def aguardando(msg):
    for clientItem in clients:
            try:
                clientItem.send(msg.encode('utf-8'))
            except:
                print("vish1")
                deleteClient(clientItem)


def deleteClient(client):
    clients.remove(client)

main()