from distutils.log import error
from itertools import count
import pygame, sys, threading, socket, time

pygame.init()

WIDTH, HEIGHT = 900, 900
 
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe!")

BOARD = pygame.image.load("assets/Board.png")
X_IMG = pygame.image.load("assets/X.png")
O_IMG = pygame.image.load("assets/O.png")

BG_COLOR = (214, 201, 227)

global board
board = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
graphical_board = [[[None, None], [None, None], [None, None]], 
                    [[None, None], [None, None], [None, None]], 
                    [[None, None], [None, None], [None, None]]] 
sua_vez = ''
to_move = ''
client = ''
count = 0

SCREEN.fill(BG_COLOR)
SCREEN.blit(BOARD, (64, 64))
game_finished = False
pygame.display.update()


def main():
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect(('3.82.147.83', 5001))
    except:
        return print('\nNão foi possívvel se conectar ao servidor!\n')

    # username = input('Usuário> ')
    # print('\nConectado')

    thread1 = threading.Thread(target=receiveMessages, args=[client])
    # thread2 = threading.Thread(target=sendMessages, args=[client])

    thread1.start()
    # thread2.start()
def receiveMessages(client):
    while True:
        try:
            global count 
            msg = client.recv(2048).decode('utf-8')

            if msg.startswith('lado'):
                print("aqui3")
                valor = msg.replace('lado', ' ').strip().split(', ')
                global to_move 
                to_move =  valor[0]
                global sua_vez
                sua_vez = valor[1]
                SCREEN.fill(BG_COLOR)
                SCREEN.blit(BOARD, (64, 64))
                pygame.display.update()
                print(msg)
            elif msg == "True" and count == 0:
                pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
                time.sleep(2)
                SCREEN.fill(BG_COLOR)
                SCREEN.blit(BOARD, (64, 64))
                count += 1
                pygame.display.update()
            elif msg == "True" and count == 1:
                count += 1
                pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
                pygame.display.update()

                print(to_move)
                
            elif msg == "False":
                print("mensagem")
                decay_font = pygame.font.Font('assets/Roboto-Regular.ttf', 70)
                text_surface = decay_font.render("Aguardando Jogadores!",True,(0, 0,0))
                text_rect = text_surface.get_rect(center=(WIDTH/2, HEIGHT/2))
                SCREEN.blit(text_surface, text_rect)
                count = 0
                pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
                pygame.display.update()

            elif msg.startswith('jogada'):
                pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
                print("jogada")
                move = msg.replace('jogada', ' ').strip().split(', ')
                x = float(move[0])
                y = float(move[1])
                print(round(x), round(y), move[2])
                sua_vez = move[3]
                board[round(y)][round(x)] = move[2]  
                render_board(board, X_IMG, O_IMG)

                for i in range(3):
                    for j in range(3):
                        if graphical_board[i][j][0] is not None:
                            SCREEN.blit(graphical_board[i][j][0], graphical_board[i][j][1])    
                if check_win(board) is not None:
                    print("entrou aqui mané!")
                    global game_finished
                    game_finished = True
                pygame.display.update()
        except:
            print()
            print('\nNão foi possível permanecer conectado no servidor!\n')
            print('Pressione <Enter> Para continuar...')
            client.close()
            break
           

            

def sendMessages(client, converted_x, converted_y):
        try:
            print('aqui123')
            global sua_vez
            vez = 'O' if sua_vez == 'X' else 'X'
            sua_vez = vez
            data = f'jogada {converted_x},  {converted_y}, {to_move}, {vez}'
            print("aqui1234", data)
            client.send(data.encode('utf-8'))
        except:
            print(";(")
            return



def render_board(board, ximg, oimg):
    global graphical_board
    print("render", board)
    for i in range(3):
        for j in range(3):
            if board[i][j] == 'X':
                graphical_board[i][j][0] = ximg
                graphical_board[i][j][1] = ximg.get_rect(center=(j*300+150, i*300+150))
            elif board[i][j] == 'O':
                graphical_board[i][j][0] = oimg
                graphical_board[i][j][1] = oimg.get_rect(center=(j*300+150, i*300+150))

def add_XO(board, graphical_board, to_move, sua_vez):
    print("opa", to_move)
    if to_move == sua_vez:
        print("passou")
        current_pos = pygame.mouse.get_pos()
        converted_x = (current_pos[0]-65)/835*2
        converted_y = current_pos[1]/835*2
        if board[round(converted_y)][round(converted_x)] != 'O' and board[round(converted_y)][round(converted_x)] != 'X':
            board[round(converted_y)][round(converted_x)] = to_move
            print(to_move)
            sendMessages(client, converted_x, converted_y)
            print("enviou")
        render_board(board, X_IMG, O_IMG)

        for i in range(3):
            for j in range(3):
                if graphical_board[i][j][0] is not None:
                    SCREEN.blit(graphical_board[i][j][0], graphical_board[i][j][1])

        return board, to_move
    else:
        return board, to_move



def msg_final(winner):
    print("winner!! ")
    decay_font = pygame.font.Font('assets/Roboto-Regular.ttf', 100)
    if winner == to_move:
        print("ganhou")
        text_surface = decay_font.render("Você Ganhou!",True,(0, 255,0))
    elif winner == 'DRAW':
        text_surface = decay_font.render("Empate",True,(255, 255,0))
    else:
        text_surface = decay_font.render("Você Perdeu!",True,(255, 0,0))
    text_rect = text_surface.get_rect(center=(WIDTH/2, HEIGHT/2))
    SCREEN.blit(text_surface, text_rect)
    pygame.display.update()

def msg_vez():
    if count > 1:
        decay_font = pygame.font.Font('assets/Roboto-Regular.ttf', 40)
        text_surface1 = decay_font.render("Sua vez" ,True,(0, 255, 0) if to_move == sua_vez else (204, 204, 204))
        text_surface2 = decay_font.render("Vez do adversário",True, (0, 255, 0)if to_move != sua_vez else (204, 204, 204) )

        SCREEN.blit(text_surface1, (400, 0))
        SCREEN.blit(text_surface2, (20, 0))

        pygame.display.update()
def check_win(board):
    winner = None
    for row in range(0, 3):
        if((board[row][0] == board[row][1] == board[row][2]) and (board [row][0] is not None)):
            winner = board[row][0]
            for i in range(0, 3):
                graphical_board[row][i][0] = pygame.image.load(f"assets/Winning {winner}.png")
                SCREEN.blit(graphical_board[row][i][0], graphical_board[row][i][1])
            pygame.display.update()
            msg_final(winner)
            return winner

    for col in range(0, 3):
        if((board[0][col] == board[1][col] == board[2][col]) and (board[0][col] is not None)):
            winner =  board[0][col]
            for i in range(0, 3):
                graphical_board[i][col][0] = pygame.image.load(f"assets/Winning {winner}.png")
                SCREEN.blit(graphical_board[i][col][0], graphical_board[i][col][1])
            pygame.display.update()
            msg_final(winner)
            return winner
   
    if (board[0][0] == board[1][1] == board[2][2]) and (board[0][0] is not None):
        winner =  board[0][0]
        graphical_board[0][0][0] = pygame.image.load(f"assets/Winning {winner}.png")
        SCREEN.blit(graphical_board[0][0][0], graphical_board[0][0][1])
        graphical_board[1][1][0] = pygame.image.load(f"assets/Winning {winner}.png")
        SCREEN.blit(graphical_board[1][1][0], graphical_board[1][1][1])
        graphical_board[2][2][0] = pygame.image.load(f"assets/Winning {winner}.png")
        SCREEN.blit(graphical_board[2][2][0], graphical_board[2][2][1])
        pygame.display.update()
        msg_final(winner)
        return winner
          
    if (board[0][2] == board[1][1] == board[2][0]) and (board[0][2] is not None):
        winner =  board[0][2]
        graphical_board[0][2][0] = pygame.image.load(f"assets/Winning {winner}.png")
        SCREEN.blit(graphical_board[0][2][0], graphical_board[0][2][1])
        graphical_board[1][1][0] = pygame.image.load(f"assets/Winning {winner}.png")
        SCREEN.blit(graphical_board[1][1][0], graphical_board[1][1][1])
        graphical_board[2][0][0] = pygame.image.load(f"assets/Winning {winner}.png")
        SCREEN.blit(graphical_board[2][0][0], graphical_board[2][0][1])
        pygame.display.update()
        msg_final(winner)
        return winner
    
    if winner is None:
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] != 'X' and board[i][j] != 'O':
                    return None
        winner = 'DRAW'
        msg_final(winner)
        return "DRAW"
    




main()

while True:
    
    msg_vez()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            client.close() 
            exit()
    
        if event.type == pygame.MOUSEBUTTONDOWN:
            board, to_move = add_XO(board, graphical_board, to_move, sua_vez)
        if check_win(board) is not None:
            game_finished = True
            count = 0
            
            
        if game_finished:
            print("acabou")
            time.sleep(2)
            board = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
            graphical_board = [[[None, None], [None, None], [None, None]], 
                                    [[None, None], [None, None], [None, None]], 
                                    [[None, None], [None, None], [None, None]]]
            print("aqui acabou!")
            
            SCREEN.fill(BG_COLOR)
            SCREEN.blit(BOARD, (64, 64))
            render_board(board, X_IMG, O_IMG)
            game_finished = False
        pygame.display.update()