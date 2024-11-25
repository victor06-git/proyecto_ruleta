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
        "your_turn":False,
        "chips":{
            "fitxa_100":3,
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
#Estas son las variables para detrerminar el area de apuestas
bet_even = pygame.Rect(850,100,100,100)
bet_odd = pygame.Rect(850,555,100,100)
bet_red = pygame.Rect(850,200,100,180)
bet_black = pygame.Rect(850,380,100,180)
bet_column_1 = pygame.Rect(950,650,50,50)
bet_column_2 = pygame.Rect(1050,650,50,50)
bet_column_3 = pygame.Rect(1150,650,50,50)

# Definir la finestra
screen_width = 1495
screen_height = 750
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Ruleta')

draw_chips = [
    {"x": 545, "y":650, "radius":25, "color":"", "value":100, "width":5},
    {"x": 645, "y":650, "radius":25, "color":"", "value":50, "width":5},
    {"x": 745, "y":650, "radius":25, "color":"", "value":20, "width":5},
    {"x": 595, "y":595, "radius":25, "color":"", "value":10, "width":5},
    {"x": 695, "y":595, "radius":25, "color":"", "value":5, "width":5}
]

dragg_draw_chips = [
    
]
registro_apuestas = {
    "par":{},
    "impar":{},
    "rojo":{},
    "negro":{},
    "columna_1":{},
    "columna_2":{},
    "columna_3":{},
    "numbers":{}
}

font_chip = pygame.font.SysFont("Arial",18,bold=True) #--> El bold=True es para hacerlo en negrita


clicked = False
dragging = False
dragging_chip = None
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

def registrar_apuestas(tipo_apuesta, tipo_ficha):

    if tipo_ficha not in registro_apuestas[tipo_apuesta]:
        registro_apuestas[tipo_apuesta][tipo_ficha] = 0
    
    elif tipo_ficha in registro_apuestas[tipo_apuesta]:
        registro_apuestas[tipo_apuesta][tipo_ficha] +=1
    
    print(f"Has apostado {registro_apuestas[tipo_apuesta][tipo_ficha]+1} fichas de valor {tipo_ficha} a {tipo_apuesta.capitalize()}")

def odd_even_event(player):
    oange = 1

# Fer càlculs
def app_run():
    global rad_first, rad_second, clicked, draw_chips, dragging, dragging_chip
    mouse_x, mouse_y = pygame.mouse.get_pos()

    offset_x = 0
    offset_y = 0
    height_casilla = (600 / 13)
    width_casilla = (300 / 3)
    apuesta_done = {} #--> Para guardar las apuestas

    """Aqui tengo que hacer varias cosas para mejorar la logica:
    ***3***
        - En este punto se tiene que ejecutar la ruleta
        - Una vez ejecutada la ruleta las fichas vuelven a su posicón original
    
    """
    for ficha in draw_chips:

        puntero = math.sqrt((mouse_x - ficha["x"]) ** 2 + (mouse_y - ficha["y"])**2)#--> es la formula para poder clickar encima de la redonda

        if clicked and puntero <= ficha["radius"]:
            
            if not dragging:

                dragging = True
                dragging_chip = ficha
                offset_x = mouse_x - ficha["x"]
                offset_y = mouse_y - ficha["y"]

                print(f"Has clickado la ficha {ficha["value"]}")

            if dragging and dragging_chip == ficha:
                dragging_chip["x"] = mouse_x - offset_x
                dragging_chip["y"] = mouse_y - offset_y

        elif not clicked and dragging:

            for ficha in draw_chips:

                if bet_even.collidepoint(ficha["x"],ficha["y"]):
                    registrar_apuestas("par", ficha["value"])
                    apuesta_done["par"] = ficha
                
                elif bet_odd.collidepoint(ficha["x"],ficha["y"]):
                    registrar_apuestas("impar", ficha["value"])
                    apuesta_done["impar"] = ficha
                
                elif bet_red.collidepoint(ficha["x"],ficha["y"]):
                    registrar_apuestas("rojo", ficha["value"])
                    apuesta_done["rojo"] = ficha
                
                elif bet_black.collidepoint(ficha["x"],ficha["y"]):
                    registrar_apuestas("negro", ficha["value"])
                    apuesta_done["negro"] = ficha
                
                elif bet_column_1.collidepoint(ficha["x"],ficha["y"]):
                    registrar_apuestas("columna_1", ficha["value"])
                    apuesta_done["columna_1"] = ficha
                
                elif bet_column_2.collidepoint(ficha["x"],ficha["y"]):
                    registrar_apuestas("columna_2", ficha["value"])
                    apuesta_done["columna_2"] = ficha

                elif bet_column_3.collidepoint(ficha["x"],ficha["y"]):
                    registrar_apuestas("columna_3", ficha["value"])
                    apuesta_done["columna_3"] = ficha

                else:

                    bet_number = None

                    for columna in range(3):
                        for fila in range(12):

                            pos_x = 950 + columna*width_casilla
                            pos_y = 100 + fila*height_casilla
                            rect_casilla = pygame.Rect(pos_x, pos_y, width_casilla, height_casilla)

                            if rect_casilla.collidepoint(ficha["x"], ficha["y"]):
                                ficha["x"] = pos_x + width_casilla // 2
                                ficha["y"] = pos_y + height_casilla // 2
                                bet_number = chips[columna][fila]
                                break#--> aquí paro el bucle cuando bet_number tiene un valor
                        
                        if bet_number is not None:#--> Lo pongo asi porque sin ome continuaria el bucle aun que ya tubiera valor
                            print(f"Has apostado al numero: {bet_number}")
                            registrar_apuestas("numbers",ficha["value"])
                            break

                    if bet_number is None and ficha == dragging_chip:

                        if ficha["value"] == 100:
                            ficha["x"], ficha["y"] = 545, 650
                        
                        elif ficha["value"] == 50:
                            ficha["x"], ficha["y"] = 645, 650
                        
                        elif ficha["value"] == 20:
                            ficha["x"], ficha["y"] = 745, 650
                        
                        elif ficha["value"] == 10:
                            ficha["x"], ficha["y"] = 595, 595

                        elif ficha["value"] == 5:
                            ficha["x"], ficha["y"] = 695, 595

            dragging = False
            dragging_chip = None

# Dibuixar
def app_draw():

    global draw_chips,font_chip
    # Pintar el fons de blanc
    screen.fill(GREY)

    draw_grid()
    
    draw_roulette() #Función draw ruleta
    table() #Función dibujar tabla
    banca()
    tablero_fichas()

    pygame.display.update()

#Logica de apuesta: def even_odd_event  () // def red_black_event () // def bet_number_table () // def column_event () // (PROVISIONAL) --> def number_roullette () ; return number
        
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
    pygame.draw.rect(screen, DARK_GREEN, (850, 100 ,100, 100)) #--> area para apostar en PAR
    pygame.draw.rect(screen, DARK_GREEN, (850 , 200, 100, 180))#--> area para apostar al color rojo
    pygame.draw.rect(screen, DARK_GREEN, (850 , 380, 100, 180))#--> area para apostar al color negro
    pygame.draw.rect(screen, DARK_GREEN, (850 ,555, 100, 100)) #--> area para apostar a Impar
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

            tablero.append({"numero":numbers , "color":color}) #--> Esto servirá para las apuestas de colores

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

def tablero_fichas():

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
            font_text_cantidad = pygame.font.SysFont("Arial", 14, bold=True)
            text_rect = (520, 520)
            player_rect = (640,517)
            screen.blit(text_fichas, text_rect)
            screen.blit(text_player,player_rect)

            for ficha in draw_chips:

                chip_type = f"fitxa_{ficha['value']}" #--> Aquí lo que hago es, el valor de las fihcas en value, lo inserto a la cadena de string de fitxa_... // Es decir, si el value = 100, se formarà la cadena de strings de "fitxa_100"
                chip_cantidad = players[player]["chips"].get(chip_type)#--> con esto obtengo las cantidades de el valor de la ficha  
                color = players[player]["color"]

                if chip_cantidad > 0:

                #for i in range(chip_cantidad): 
                #icha["y"]- i * (ficha["radius"] * 1.2 + 2)

                        #--> este es bloque de codigo que haga que salgan apiladas por cada moneda del mismo tipo que tengamos

                        y_offset = ficha["y"]
                        text_cantidad = font_text_cantidad.render("x"+ str(chip_cantidad),True, WHITE)
                        text_cantidad_rect = (ficha["x"]+30, y_offset)

                        pygame.draw.circle(screen, WHITE, (ficha["x"], y_offset), ficha["radius"])
                        pygame.draw.circle(screen, color, (ficha["x"], y_offset), ficha["radius"],ficha["width"])
                        screen.blit(text_cantidad,text_cantidad_rect)

                        
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

if __name__ == "__main__":
    main()
