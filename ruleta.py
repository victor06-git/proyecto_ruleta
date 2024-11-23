#!/usr/bin/env python3
import math
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import sys
import random


# Definir colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0) 
DARK_GREEN = (0, 180, 0)
GREY = (120,120,120)
YELLOW = (243,228,67)
BROWN = (98,52,18)
GRAY = (128,128,128)




#Para saber como va a girar la ruleta y definir el angulo que lleva cada número para mostrarlo

pygame.init()
clock = pygame.time.Clock()


# Definir la finestra
screen_width = 1400
screen_height = 750
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Ruleta')



clicked = False
mouse_x, mouse_y = -1, -1

rad_first = ((360 / 37) * (math.pi / 180)) #First angle
rad_second = ((360 / 37) * (math.pi / 180) + (rad_first)) #Second angle

rad_1 = rad_second
rad_2 = ((360 / 37) * (math.pi / 180) + (rad_1))

rad_num = ((360 / 37) * (math.pi / 180) * 5) / 2
rad_num1 = ((360 / 37) * (math.pi / 180) * 3) / 2

winning_number = None #El número ganador elegido
show_win_number = False #Enseñar número ganador
spinning = False #Verdadero/Falso inicio spin
spin_angle = 0 #ángulo de rotación
spin_speed = 0 #Velocidad de rotación
friction = 0.98 #Número para que la ruleta se detenga
min_speed = 0.01 #Mínima velocidad para que la ruleta siga girando
initial_speed = 25 #Velocidad inicial de giro

#Botón girar
button_width = 200
button_height = 50
button_x  = 600
button_y = 100
button_color = RED
button_hover_color = (255, 0, 0, 128)

#lista números ruleta
roulette_numbers = [32, 15, 19, 4, 21, 2, 25,
                        17, 34, 6, 27, 13, 36, 11,
                        30, 8, 23, 10, 5, 24, 16, 
                        33, 1, 20, 14, 31, 9, 22, 
                        18, 29, 7, 28, 12, 35, 3, 26]

# Bucle de l'aplicació
def main():
    is_looping = True
    
    while is_looping:
        is_looping = app_events()
        app_run()
        app_draw()
        
        clock.tick(60) # Limitar a 60 FPS

    # Fora del bucle, tancar l'aplicació
    pygame.quit()
    sys.exit()

# Gestionar events
# Gestionar events
def app_events():
    global clicked, mouse_pos, button_rect

    for event in pygame.event.get():
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:  # Botón cerrar ventana
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        
    return True

# Fer càlculs
def app_run():
    global rad_first, rad_second
    mouse_x, mouse_y = pygame.mouse.get_pos()
    pass

        
# Dibuixar
def app_draw():
    global button_rect
    # Pintar el fons de blanc
    screen.fill(GREY)

    draw_grid()
    
    draw_roulette() #Función draw ruleta
    draw_flecha() #Función dibujar flecha
    button_rect = draw_button(mouse_pos)
    table() #Función dibujar tabla
    banca() #Función dibujar banca
    fichas() #Función dibujar fichas
    draw_win_number() #Función dibuja número elegido
    
    pygame.display.update()
def is_click_on_button(pos, button_rect):
    return button_rect.collidepoint(pos)

def click(pos, button_rect):
    global spinning, spin_speed, show_win_number
    if is_click_on_button(pos, button_rect):
        spinning = True
        show_win_number = False
        spin_speed = initial_speed

def draw_win_number():
    if show_win_number and winning_number is not None:
        font = pygame.font.Font(None, 64)
        text = font.render(f"Número ganador: {winning_number}", True, WHITE)
        text_rect = text.get_rect(center=(screen_width // 2 + 200, 50))

        panel_rect = text_rect.copy()
        panel_rect.inflate_ip(20, 20)
        pygame.draw.rect(screen, BLACK, panel_rect)
        pygame.draw.rect(screen, YELLOW, panel_rect, 2)

        screen.blit(text, text_rect)

def update_spin():
    global spinning, spin_angle, spin_speed, winning_number, show_win_number
    if spinning:
        spin_angle += spin_speed
        spin_speed *= friction

        if spin_speed < min_speed:
            spinning = False
            spin_speed = 0

            current_angle = spin_angle % 360
            sector = int((current_angle / (360 / 37)) % 37)
            winning_number = roulette_numbers[sector]
            show_win_number = True

def draw_button(mouse_pos):
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    if button_rect.collidepoint(mouse_pos):
        color = button_color
    else:
        color = button_hover_color
    
    pygame.draw.rect(screen, color, button_rect) #Draw button
    pygame.draw.rect(screen, WHITE, button_rect, 2) #Draw border

    #Texto button
    font = pygame.font.Font(None, 36)
    text = font.render("GIRAR", True, WHITE)
    text_rect = text.get_rect(center=(button_x + button_width / 2, button_y + button_height / 2))
    screen.blit(text, text_rect)

    return button_rect  

def draw_flecha():
    center_x = screen_width  // 2 / 2
    center_y = screen_height // 2 - 100

    points = [
        (center_x + 265, center_y),
        (center_x + 285, center_y - 10),
        (center_x + 285, center_y + 10),
    ]

    pygame.draw.polygon(screen, RED, points)
    pygame.draw.polygon(screen, YELLOW, points, 2)
#Roulette
def draw_roulette():
    global rad_first, rad_second
    
    rad_first = ((360 / 37) * (math.pi / 180)) #First angle
    rad_second = ((360 / 37) * (math.pi / 180) + (rad_first)) #Second angle

    rad_1 = rad_second
    rad_2 = ((360 / 37) * (math.pi / 180) + (rad_1))

    rad_num = ((360 / 37) * (math.pi / 180) * 5) / 2
    rad_num1 = ((360 / 37) * (math.pi / 180) * 3) / 2
   
    
    #Ruleta parte verde del 0
    pygame.draw.polygon(screen, GREEN, [((screen_width // 2) / 2, screen_height // 2 - 100),
                        ((screen_width // 2) / 2 + (250 * math.cos(rad_first)), screen_height // 2 + (250 * math.sin(rad_first)) - 100),
                        ((screen_width // 2) / 2 + (250 * math.cos(rad_second)), screen_height // 2 + (250 * math.sin(rad_second)) - 100)])
    pygame.draw.polygon(screen, YELLOW, [((screen_width // 2) / 2, screen_height // 2 - 100), 
                                         ((screen_width // 2) / 2 + (250 * math.cos(rad_first)), screen_height // 2 + (250 * math.sin(rad_first)) - 100),
                                         ((screen_width // 2) / 2 + (250 * math.cos(rad_second)), screen_height // 2 + (250 * math.sin(rad_second)) - 100)], 2)
       
    #RULETA ROJO/NEGRO
    for angle in range(36):    

        if angle % 2 == 0:
            color = RED
        else:
            color = BLACK

        pygame.draw.polygon(screen, color, [(screen_width // 2 / 2 , screen_height // 2 - 100), 
                                            (screen_width // 2 / 2 + (250 * math.cos(rad_1)), screen_height // 2 + (250 * math.sin(rad_1)) - 100),
                                            (screen_width // 2 / 2 + (250 * math.cos(rad_2)), screen_height // 2 + (250 * math.sin(rad_2)) - 100)])
        pygame.draw.polygon(screen, YELLOW, [(screen_width // 2 / 2 , screen_height // 2 - 100), 
                                             (screen_width // 2 / 2 + (250 * math.cos(rad_1)), screen_height // 2 + (250 * math.sin(rad_1)) - 100),
                                             (screen_width // 2 / 2 + (250 * math.cos(rad_2)), screen_height // 2 + (250 * math.sin(rad_2)) - 100)], 2)
        rad_1 += ((360 / 37) * (math.pi / 180))
        rad_2 += ((360 / 37) * (math.pi / 180))
    
    #Centro ruleta y borde / decoración
    pygame.draw.circle(screen, BROWN, (screen_width // 2 / 2, screen_height // 2 - 100), 260, 20)
    pygame.draw.circle(screen, BROWN, (screen_width // 2 / 2, screen_height // 2 - 100), 150)
    pygame.draw.circle(screen, GRAY, (screen_width // 2 / 2, screen_height // 2 - 100), 190, 10)
    
    #Lineas interiors ruleta
    pygame.draw.line(screen, BLACK, (screen_width // 2 / 2, screen_height // 2 - 100), (screen_width // 2 / 2, screen_height // 2 + 50), 3)
    pygame.draw.line(screen, BLACK, (screen_width // 2 / 2, screen_height // 2 - 100), (screen_width // 2 / 2, screen_height // 2 - 250), 3)
    pygame.draw.line(screen, BLACK, (screen_width // 2 / 2, screen_height // 2 - 100), (screen_width // 2 / 2 + 148, screen_height // 2 - 100), 3)
    pygame.draw.line(screen, BLACK, (screen_width // 2 / 2, screen_height // 2 - 100), (screen_width // 2 / 2 - 148, screen_height // 2 - 100), 3)
    pygame.draw.line(screen, BLACK, (screen_width // 2 / 2, screen_height // 2 - 100), (screen_width // 2 / 2 + (148 * math.cos(math.pi / 4)), screen_height // 2 - 100 + (148 * math.sin(math.pi / 4))), 3)
    pygame.draw.line(screen, BLACK, (screen_width // 2 / 2, screen_height // 2 - 100), (screen_width // 2 / 2 - (148 * math.cos(math.pi / 4)), screen_height // 2 - 100 + (148 * math.sin(math.pi / 4))), 3)
    pygame.draw.line(screen, BLACK, (screen_width // 2 / 2, screen_height // 2 - 100), (screen_width // 2 / 2 + (148 * math.cos(1.25 * math.pi)), screen_height // 2 - 100 + (148 * math.sin(1.25 * math.pi))), 3)
    pygame.draw.line(screen, BLACK, (screen_width // 2 / 2, screen_height // 2 - 100), (screen_width // 2 / 2 - (148 * math.cos(1.25 * math.pi)), screen_height // 2 - 100 + (148 * math.sin(1.25 * math.pi))), 3)
    
    #Part interior
    pygame.draw.circle(screen, BLACK, (screen_width // 2 / 2, screen_height // 2 - 100), 30)
    pygame.draw.circle(screen, YELLOW, (screen_width // 2 / 2, screen_height // 2 - 100), 18)
    pygame.draw.line(screen, YELLOW, (screen_width // 2 / 2, screen_height // 2 - 100), (screen_width // 2 / 2, screen_height // 2 - 30), 5)
    pygame.draw.circle(screen, YELLOW, (screen_width // 2 /2, screen_height // 2 - 30), 10)
    
    pygame.draw.line(screen, YELLOW, (screen_width // 2 / 2, screen_height // 2 - 100), (screen_width // 2 / 2, screen_height // 2 - 170), 5)
    pygame.draw.circle(screen, YELLOW, (screen_width // 2 /2, screen_height // 2 - 170), 10)
   
    pygame.draw.line(screen, YELLOW, (screen_width // 2 / 2, screen_height // 2 - 100), (screen_width // 2 / 2 + 70, screen_height // 2 - 100), 5)
    pygame.draw.circle(screen, YELLOW, (screen_width // 2 / 2 + 70, screen_height // 2 - 100), 10)

    pygame.draw.line(screen, YELLOW, (screen_width // 2 / 2, screen_height // 2 - 100), (screen_width // 2 / 2 - 70, screen_height // 2 - 100), 5)
    pygame.draw.circle(screen, YELLOW, (screen_width // 2 / 2 - 70, screen_height // 2 - 100), 10)
    
    x0 = (screen_width // 2 / 2 ) + (215 * math.cos(rad_num1))
    y0 = screen_height // 2  + (215 * math.sin(rad_num1)) - 100
    font0 = pygame.font.Font(None, 20)
    text0 = font0.render(str(0), True, WHITE)
    text_rect0 = (x0,y0)
    screen.blit(text0, text_rect0)
    
    for number in roulette_numbers:    
        x = (screen_width // 2 / 2) + (215 * math.cos(rad_num))
        y = (screen_height // 2 )+ (215 * math.sin(rad_num)) - 100
        font = pygame.font.Font(None, 20)
        text = font.render(str(number), True, WHITE)
        text_rect = (x,y)
        screen.blit(text, text_rect)
        rad_num += ((360/37) * (math.pi/180)) 

#Tabla de apuestas
def table():
    #Parte del 0
    points_rect0 = [(1100, 50), (950, 100), (1250, 100), (1100, 50)]
    pygame.draw.polygon(screen, BLACK, points_rect0, 3)
    pygame.draw.polygon(screen, DARK_GREEN, points_rect0)
    

    font = pygame.font.SysFont(None, 30)
    text = font.render(str(0), True, WHITE)
    text_rect = (((950 + 1250) / 2 - 4) , 70) #Posicion de texto 0 centrado
    screen.blit(text, text_rect)
    
    height_casella = (600 / 13)
    width_casella = (300 / 3)

    #Casillas apuesta columna
    pygame.draw.rect(screen, DARK_GREEN, (950 + (width_casella), 100 + (600 / 13) * 12, width_casella, height_casella))
    pygame.draw.rect(screen, DARK_GREEN, (950 - 3 , 100 + (600 / 13) * 12, width_casella + 3, height_casella))
    pygame.draw.rect(screen, DARK_GREEN, (950 + (2 * width_casella), 100 + (600 / 13) * 12, width_casella, height_casella))
    pygame.draw.rect(screen, BLACK, (950 + (width_casella), 100 + (600 / 13) * 12, width_casella, height_casella), 3)
    pygame.draw.rect(screen, BLACK, (950 - 3 , 100 + (600 / 13) * 12, width_casella + 3, height_casella), 3)
    pygame.draw.rect(screen, BLACK, (950 + (2 * width_casella), 100 + (600 / 13) * 12, width_casella, height_casella), 3)
    font = pygame.font.SysFont(None, 30)
    text = font.render(str("2 to 1"), True, WHITE)
    text_rect = (((950 - 24) + (width_casella // 2)) , 665) 
    screen.blit(text, text_rect)
    text_rect2 = (((1025) + (width_casella // 2)) , 665) 
    screen.blit(text, text_rect2)
    text_rect3 = (((1125) + (width_casella // 2)) , 665) 
    screen.blit(text, text_rect3)
    
    #Pares/ Impares/ Rojo/ Negro
    pygame.draw.rect(screen, DARK_GREEN, (850, 100 ,100, 100))
    pygame.draw.rect(screen, DARK_GREEN, (850 , 200, 100, 180))
    pygame.draw.rect(screen, DARK_GREEN, (850 , 380, 100, 180))
    pygame.draw.rect(screen, DARK_GREEN, (850 ,555, 100, 100))
    pygame.draw.rect(screen, BLACK, (850, 100 ,100, 100), 3)
    pygame.draw.rect(screen, BLACK, (850 , 200, 100, 180), 3)
    pygame.draw.rect(screen, BLACK, (850 , 380, 100, 180), 3)
    pygame.draw.rect(screen, BLACK, (850 ,555, 100, 100), 3)

    #Rombos rojo y negro
    pygame.draw.polygon(screen, RED, [(900, (200 + ((180 / 2) / 4))),
                                      (850 + (100 / 4), (200 + (180 / 2))), 
                                      (900, (200 + 3 * (180 / 4) + 25)),
                                      (950 - ((100 / 4)), (200 + (180 / 2)))])
    
    pygame.draw.polygon(screen, BLACK, [(900, (380 + ((180 / 2) / 4))),
                                      (850 + (100 / 4), (380 + (180 / 2))), 
                                      (900, (380 + 3 * (180 / 4) + 25)),
                                      (950 - ((100 / 4)), (380 + (180 / 2)))])
    
    #EVEN/ODD
    font = pygame.font.SysFont(None, 35)
    text = font.render(str("PAR"), True, WHITE)
    text_rect = (((877) , 140))
    screen.blit(text, text_rect)
    text2 = font.render(str("IMPAR"), True, WHITE)
    text_rect2 = (((865) , 595))
    screen.blit(text2, text_rect2)  


    for  columna in range(3):
        for fila in range(12):
            
            if columna == 0:
                if fila == 0 or  fila == 2 or  fila == 5 or fila == 6 or  fila == 8 or fila == 11:
                    color = RED
                else: 
                    color = BLACK
            if columna == 1:
                if fila == 0 or fila == 2 or fila == 3 or  fila == 5 or fila == 6 or fila ==8 or fila == 9 or fila == 11:
                    color = BLACK
                else:
                    color = RED
            if columna == 2:
                if fila == 0 or fila == 2 or fila == 3 or fila == 5 or  fila == 6 or  fila == 8 or  fila == 9 or  fila == 11:
                    color = RED
                else:
                    color = BLACK

            if columna == 0:
                column_number = 0
            elif columna == 1:
                column_number = 1
            else:
                column_number = 2
            

            #Casillas apuestas números
            pygame.draw.rect(screen, color, (950 + (columna * width_casella), 100 + (fila * height_casella), width_casella, height_casella)) #Relleno de color la casilla
            pygame.draw.rect(screen, WHITE, (950 + (columna * width_casella), 100 + (fila * height_casella), width_casella, height_casella), 1) #Contorno casilla
            
            
            #Números casillas
            numbers = chips[column_number][fila]
            font = pygame.font.SysFont(None, 25)
            text = font.render(str(numbers), True, WHITE)
            text_rect = (950 + (columna * width_casella) + 50, 100 + ( fila * height_casella) + 15) #Posicion de texto
            screen.blit(text, text_rect)
    
def banca():    
    pygame.draw.rect(screen, DARK_GREEN, (50, 550, 350, 150))
    pygame.draw.rect(screen, YELLOW, (50, 550, 350, 150), 3)
    pygame.draw.rect(screen, GREEN, (53, 553, 97, 47))
    font = pygame.font.SysFont(None, 27)
    text = font.render(str("BANCA"), True, BLACK)
    text_rect = (60, 570)
    screen.blit(text, text_rect)
    pygame.draw.line(screen, YELLOW, (50, 600), (150, 600), 3)
    pygame.draw.line(screen, YELLOW, (150, 550), (150, 600), 3)

def fichas():
    pygame.draw.rect(screen, DARK_GREEN, (500, 500, 300, 200))
    pygame.draw.rect(screen, YELLOW, (500, 500, 300, 200), 3)
    pygame.draw.rect(screen, GREEN, (503, 503, 97, 47))
    pygame.draw.line(screen, YELLOW, (500, 550), (600, 550), 3)
    pygame.draw.line(screen, YELLOW, (600, 550), (600, 500), 3)
    font = pygame.font.SysFont(None, 27)
    text = font.render(str("FICHAS"), True, BLACK)
    text_rect = (520, 520)
    screen.blit(text, text_rect)
    

#graellas
def draw_grid():
    
    # Color de la cuadrícula
    GRID_COLOR = (50, 50, 50)
    
    # Tamaño de las celdas
    cell_size = 50
    
    # Dibujar líneas verticales
    for x in range(0, screen_width, cell_size):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, screen_height))
        
        # Añadir texto de coordenadas X
        font = pygame.font.Font(None, 20)
        text = font.render(str(x), True, (200, 200, 200))
        screen.blit(text, (x+2, 2))
    
    # Dibujar líneas horizontales
    for y in range(0, screen_height, cell_size):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (screen_width, y))
        
        # Añadir texto de coordenadas Y
        font = pygame.font.Font(None, 20)
        text = font.render(str(y), True, (200, 200, 200))
        screen.blit(text, (2, y + 2))

#Lógica
players = {
    "player_purple":{
        "color": "purple",
        "money": 100,
        "your_turn":False,
        "chips":{
            "fitxa_100":90,
            "fitxa_50":0,
            "fitxa_20":0,
            "fitxa_10":0,
            "fitxa_5":0
        },
        "bet":{
            "odd_even":"",
            "column":"",
            "number":"",
            "color":"",
        }
    },
    "player_blue":{
        "color": "blue",
        "money": 100,
        "your_turn":False,
        "chips":{
            "fitxa_100":0,
            "fitxa_50":0,
            "fitxa_20":0,
            "fitxa_10":0,
            "fitxa_5":0
        },
        "bet":{
            "odd_even":"",
            "column":"",
            "number":"",
            "color":"",
        }
    },
    "player_orange":{
        "color": "orange",
        "money": 100,
        "your_turn":False,
        "chips":{
            "fitxa_100":90,
            "fitxa_50":0,
            "fitxa_20":0,
            "fitxa_10":0,
            "fitxa_5":0
        },
        "bet":{
            "odd_even":"",
            "column":"",
            "number":"",
            "color":"",
        }

    }
}

chips = [[1,4,7,10,13,16,19,22,25,28,31,34],
         [2,5,8,11,14,17,20,23,26,29,32,35],
         [3,6,9,12,15,18,21,24,27,30,33,36]]

numbers = list(range(37))

chip_0 = 0

#def lost_money(player) --> maneja la logica de la perdida de diner0
#def gain_money(player) --> maneja la logica de la ganancia de dinero
#def manage_money(player) --> en función de si gana o pierde, se añade a player["dinero"]
#def banca_rota(player)--> maneja la logica de cuando te quedas en banca rota
#def comprar fichas (player) --> Esta funcion permite comprar fichas

def buy_chips(player):

    ask_to_buy = input("Deseas comprar mas fitxas? [y/n] ").lower()

    if ask_to_buy == "yes":
        how_many = input("Select the chips to buy: [1. for 100 // 2. for 50 // 3: for 20 // 4. for 10 // 5. for 5] ")

        cuantity = int(input("How many do you want to buy ? "))

        while True:
            if how_many == "1":

                if players[player]["money"] >= (cuantity*100):

                    players[player]["money"] -= (cuantity*100)
                    players[player]["chips"]["fitxa_100"] += cuantity
                    print(f"Has adquirido {cuantity} fitxas de 100")

                else:
                    print("You do not have enough money")

            elif how_many == "2":

                if players[player]["money"] >= (cuantity*50):

                    players[player]["money"] -= (cuantity*50)
                    players[player]["chips"]["fitxa_50"] += cuantity
                    print(f"Has adquirido {cuantity} fitxas de 50")

                else:
                    print("You do not have enough money")

            elif how_many == "3":

                if players[player]["money"] >= (cuantity*20):

                    players[player]["money"] -= (cuantity*20)
                    players[player]["chips"]["fitxa_20"] += cuantity
                    print(f"Has adquirido {cuantity} fitxas de 20")

                else:
                    print("You do not have enough money")
            
            elif how_many == "4":

                if players[player]["money"] >= (cuantity*10):

                    players[player]["money"] -= (cuantity*10)
                    players[player]["chips"]["fitxa_10"] += cuantity
                    print(f"Has adquirido {cuantity} fitxas de 10")

                else:
                    print("You do not have enough money")
            
            elif how_many == "5":

                if players[player]["money"] >= (cuantity*5):

                    players[player]["money"] -= (cuantity*5)
                    players[player]["chips"]["fitxa_5"] += cuantity
                    print(f"Has adquirido {cuantity} fitxas de 5")
                else:
                    print("You do not have enough money")

            continue_to_purchase = input("Desas seguir comprando ? [y/no] ").lower()

            if continue_to_purchase == "no":
                break


def manage_bet(player):
    ask_bet = input("A que deseas apostar ? [1. Pares o Impares // 2. Columnas // 3. Numeros // 4. Color] ")

    if ask_bet == "1":

        while True:
            ask_chips = input("Cuantas fichas deseas apostar ? [1. Fitxas 100 // 2. Fitxas 50 // 3. Fitxas 20 // 4. Fitxas 10 // 5. Fitxas 5] ")

            if ask_chips == "1":
                ask_chips_100 = int(input("Cuantas fitxas de 100 quieres apostar ? \n"))

                if players[player]["chips"]["fitxa_100"] < ask_chips_100:
                    print("Error: no dispones de tantas fitxas")
                    buy_chips(player)

                elif players[player]["chips"]["fitxa_100"] >= ask_chips_100:

                    players[player]["bet"]["odd_even"] = True
                    players[player]["chips"]["fitxa_100"] -= ask_chips_100

                    print(f"Has apostado {ask_chips_100} de 100 a 'Pares o Impares'")
                    """AQUI SE PODRIA LLAMAR A UNA FUNCIÓN QUE DIGA BET_SUCCESFULL = TRUE OR FALSE, SI ES TRUE SE GANA EL DINERO SI ES FALSE SE PIERDE EL DINERO"""

            if ask_chips == "2":
                ask_chips_100 = int(input("Cuantas fitxas de 50 quieres apostar ?\n "))

                if players[player]["chips"]["fitxa_50"] < ask_chips_100:
                    print("Error: no dispones de tantas fitxas")
                    buy_chips(player)

                elif player[player]["chips"]["fitxa_50"] >= ask_chips_100:

                    players[player]["bet"]["odd_even"] = True
                    player[player]["chips"]["fitxa_50"] -= ask_chips_100

                    print(f"Has apostado {ask_chips_100} de 50 a 'Pares o Impares'")
            
            if ask_chips == "3":
                ask_chips_100 = int(input("Cuantas fitxas de 20 quieres apostar ?\n "))

                if players[player]["chips"]["fitxa_20"] < ask_chips_100:
                    print("Error: no dispones de tantas fitxas")
                    buy_chips(player)

                elif player[player]["chips"]["fitxa_20"] >= ask_chips_100:

                    players[player]["bet"]["odd_even"] = True
                    players[player]["chips"]["fitxa_20"] -= ask_chips_100

                    print(f"Has apostado {ask_chips_100} de 20 a 'Pares o Impares'")
            
            if ask_chips == "4":
                ask_chips_100 = int(input("Cuantas fitxas de 10 quieres apostar ?\n "))

                if players[player]["chips"]["fitxa_10"] < ask_chips_100:
                    print("Error: no dispones de tantas fitxas")
                    buy_chips(player)

                elif player[player]["chips"]["fitxa_10"] >= ask_chips_100:

                    players[player]["bet"]["odd_even"] = True
                    players[player]["chips"]["fitxa_10"] -= ask_chips_100

                    print(f"Has apostado {ask_chips_100} de 10 a 'Pares o Impares'")
            
            if ask_chips == "5":
                ask_chips_100 = int(input("Cuantas fitxas de 5 quieres apostar ?\n "))

                if players[player]["chips"]["fitxa_5"] < ask_chips_100:
                    print("Error: no dispones de tantas fitxas")
                    buy_chips(player)

                elif player[player]["chips"]["fitxa_5"] >= ask_chips_100:

                    players[player]["bet"]["odd_even"] = True
                    players[player]["chips"]["fitxa_5"] -= ask_chips_100

                    print(f"Has apostado {ask_chips_100} de 5 a 'Pares o Impares'")

            ask_for_betting = input("Deseas seguir apostando ? [y/n] ")
            if ask_for_betting == "no":
                break
                
        
    #for player in player:

#print(manage_bet("player_purple"))

if __name__ == "__main__":
    main()
