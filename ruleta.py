#!/usr/bin/env python3
import math
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import sys
import random

#Lógica variables
players = {
    "player_purple":{
        "color": "purple",
        "money": 100,
        "your_turn":True,
        "chips":{
            "fitxa_100":0,
            "fitxa_50":1,
            "fitxa_20":1,
            "fitxa_10":2,
            "fitxa_5":2
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
            "fitxa_50":1,
            "fitxa_20":1,
            "fitxa_10":2,
            "fitxa_5":2
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
            "fitxa_100":0,
            "fitxa_50":1,
            "fitxa_20":1,
            "fitxa_10":2,
            "fitxa_5":2
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

draw_chips = [
    {"x": 545, "y":650, "radius":35, "color":BLUE, "value":100, "width":5},
    {"x": 645, "y":650, "radius":35, "color":PURPLE, "value":50, "width":5},
    {"x": 745, "y":650, "radius":35, "color":RED, "value":20, "width":5},
    {"x": 595, "y":595, "radius":35, "color":ORANGE, "value":10, "width":5},
    {"x": 695, "y":595, "radius":35, "color":GRAY, "value":5, "width":5}
]

font_chip = pygame.font.SysFont("Arial",18,bold=True) #--> El bold=True es para hacerlo en negrita


clicked = False
dragging = False
dragging_ficha = None
mouse_x, mouse_y = -1, -1

rad_first = ((360 / 37) * (math.pi / 180)) #First angle
rad_second = ((360 / 37) * (math.pi / 180) + (rad_first)) #Second angle

rad_1 = rad_second
rad_2 = ((360 / 37) * (math.pi / 180) + (rad_1))

rad_num = ((360 / 37) * (math.pi / 180) * 5) / 2
rad_num1 = ((360 / 37) * (math.pi / 180) * 3) / 2



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
    global clicked, rotation, change

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Botón cerrar ventana
            rotation = False
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            clicked = False
    return True

# Fer càlculs
def app_run():
    global rad_first, rad_second, clicked, draw_chips, dragging, dragging_ficha
    mouse_x, mouse_y = pygame.mouse.get_pos()

    
    offset_x = 0
    offset_y = 0

    """Aqui tengo que hacer varias cosas para mejorar la logica:

    1. Si clicked == True  
       - Identificar el puntero en que ficha esta. Por ejemplo si está haciendo click en una ficha de 100, que automáticamente reconozca
         la ficha de 100 (if clicked == true and mouse_x and mouse_y in circle_100:
         --> Arrastramos la ficha de 100

    2. Si clicked == False
        - Guardar la posición --> --> if circle_x in (cuadrado de apuestas) and circle_y in (cuadrado de apuestas)... ejecutamos la función de la apuesta específica)
        - Si el circulo está en la casilla --> (Cuantas fichas quieres apostar ?)
        - Si el circulo no está en la casilla, se vuelve a la posición inicial
         --> if circle_x in (cuadrado de apuestas) and circle_y in (cuadrado de apuestas)... ejecutamos la función de la apuesta específica)
    ***3***
        - En este punto se tiene que ejecutar la ruleta
        - Una vez ejecutada la ruleta las fichas vuelven a su posicón original
    
    """
    for ficha in reversed(draw_chips):

        puntero = math.sqrt((mouse_x - ficha["x"]) ** 2 + (mouse_y - ficha["y"])**2)#--> es la formula para poder clickar encima de la redonda

        if clicked and puntero <= ficha["radius"]:
            
            if not dragging:

                dragging = True
                dragging_ficha = ficha
                offset_x = mouse_x - ficha["x"]
                offset_y = mouse_y - ficha["y"]

            if dragging_ficha == ficha and dragging:

                ficha["x"] = mouse_x - offset_x
                ficha["y"] = mouse_y - offset_y

                print(f"Has clickado la ficha {ficha['value']}")

                """if ficha["value"] == 100:
                    print(f"Has clickado la ficha {ficha["value"]}")
            
                elif ficha["value"] == 50:
                    print(f"Has clickado la ficha {ficha["value"]}")
            
                elif ficha["value"] == 20:
                    print(f"Has clickado la ficha {ficha["value"]}")
            
                elif ficha["value"] == 10:
                    print(f"Has clickado la ficha {ficha["value"]}")

                elif ficha["value"] == 5:
                    print(f"Has clickado la ficha {ficha["value"]}")"""

        elif not clicked and dragging:
            dragging = False
            dragging_ficha = None

# Dibuixar
def app_draw():

    global draw_chips,font_chip
    # Pintar el fons de blanc
    screen.fill(GREY)

    draw_grid()
    
    draw_roulette() #Función draw ruleta
    table() #Función dibujar tabla
    banca()
    tablero_fichas("player_purple")

    pygame.display.update()



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
    
    #lista números ruleta
    roulette_numbers = [32, 15, 19, 4, 21, 2, 25,
                        17, 34, 6, 27, 13, 36, 11,
                        30, 8, 23, 10, 5, 24, 16, 
                        33, 1, 20, 14, 31, 9, 22, 
                        18, 29, 7, 28, 12, 35, 3, 26]
    
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

    tablero = [] #--> Creo esta lista vacia para despues poder hacer las apuestas por colores

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

            tablero.append({"numero":numbers , "color":color})

    return tablero

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

def tablero_fichas(player):

    y_offset = 0

    for player in players:

        if players[player]["your_turn"] == True:

            pygame.draw.rect(screen, DARK_GREEN, (500, 500, 300, 200))
            pygame.draw.rect(screen, YELLOW, (500, 500, 300, 200), 3)
            pygame.draw.rect(screen, GREEN, (503, 503, 97, 47))
            pygame.draw.line(screen, YELLOW, (500, 550), (600, 550), 3)
            pygame.draw.line(screen, YELLOW, (600, 550), (600, 500), 3)
            pygame.draw.line(screen, YELLOW, (600, 550), (799, 550), 3)
            pygame.draw.rect(screen, GREEN, (603, 503, 97*2, 47))
            
            font_text = pygame.font.SysFont(None, 27)
            text_fichas = font_text.render(str("FICHAS"), True, BLACK)
            text_player = font_text.render(str(player),True, BLACK)
            text_rect = (520, 520)
            player_rect = (640,517)
            screen.blit(text_fichas, text_rect)
            screen.blit(text_player,player_rect)

            for ficha in draw_chips:

                chip_type = f"fitxa_{ficha['value']}" #--> Aquí lo que hago es, el valor de las fihcas en value, lo inserto a la cadena de string de fitxa_... // Es decir, si el value = 100, se formarà la cadena de strings de "fitxa_100"
                chip_cantidad = players[player]["chips"].get(chip_type)#--> con esto obtengo el valor de la ficha  

                if chip_cantidad > 0:
                    
                    for i in range(chip_cantidad):

                        y_offset = ficha["y"]- i * (ficha["radius"] * 0.3 + 5) #El 0.3, es el numero para superponer las fichas una encima de otra

                        # Dibujar el círculo
                        pygame.draw.circle(screen, WHITE, (ficha["x"], y_offset), ficha["radius"])
                        pygame.draw.circle(screen, ficha["color"], (ficha["x"], y_offset), ficha["radius"],ficha["width"])

                        # Dibujar el valor de la ficha centrado
                        valor_ficha = font_chip.render(str(ficha["value"]), True, BLACK)
                        pos_ficha = valor_ficha.get_rect(center=(ficha["x"], y_offset))
                        screen.blit(valor_ficha, pos_ficha)

            
            #players[player]["your_turn"] = False


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



                
        
    #for player in player:

#print(manage_bet("player_purple"))

if __name__ == "__main__":
    main()
