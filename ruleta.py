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

#Lógica
players = {
    "player_purple":{
        "color": "purple",
        "money": 100,
        "your_turn":True,
        "bet_chips":[],
        "draw_chips" : [
                    {"x": 545, "y": 650, "radius": 25, "color": "", "value": 100, "width": 5},
                    {"x": 645, "y": 650, "radius": 25, "color": "", "value": 50, "width": 5},
                    {"x": 745, "y": 650, "radius": 25, "color": "", "value": 20, "width": 5},
                    {"x": 595, "y": 595, "radius": 25, "color": "", "value": 10, "width": 5},
                    {"x": 695, "y": 595, "radius": 25, "color": "", "value": 5, "width": 5}
                ],
        "chips":{
            "fitxa_100":90,
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
        "bet_chips":[],
        "draw_chips" : [
                    {"x": 545, "y": 650, "radius": 25, "color": "", "value": 100, "width": 5},
                    {"x": 645, "y": 650, "radius": 25, "color": "", "value": 50, "width": 5},
                    {"x": 745, "y": 650, "radius": 25, "color": "", "value": 20, "width": 5},
                    {"x": 595, "y": 595, "radius": 25, "color": "", "value": 10, "width": 5},
                    {"x": 695, "y": 595, "radius": 25, "color": "", "value": 5, "width": 5}
                ],
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
        "bet_chips":[],
        "draw_chips" : [
                    {"x": 545, "y": 650, "radius": 25, "color": "", "value": 100, "width": 5},
                    {"x": 645, "y": 650, "radius": 25, "color": "", "value": 50, "width": 5},
                    {"x": 745, "y": 650, "radius": 25, "color": "", "value": 20, "width": 5},
                    {"x": 595, "y": 595, "radius": 25, "color": "", "value": 10, "width": 5},
                    {"x": 695, "y": 595, "radius": 25, "color": "", "value": 5, "width": 5}
                ],
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


registro_apuestas = {
    "par": {},
    "impar": {},
    "rojo": {},
    "negro" : {},
    "columna_1": {},
    "columna_2": {},
    "columna_3": {},
    "numbers": {}
    }

font_chip = pygame.font.SysFont("Arial", 18, bold = True)

# Definir la finestra
screen_width = 1400
screen_height = 750
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Ruleta')


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

winning_number = None #El número ganador elegido
show_win_number = False #Enseñar número ganador
spinning = False #Verdadero/Falso inicio spin
spin_angle = random.randint(0, 360) #ángulo de rotación (Hacer que salga según la probabilidad de 1.27%)
spin_speed = 0 #Velocidad de rotación
friction = 0.97 #Número para que la ruleta se detenga
min_speed = 0.01 #Mínima velocidad para que la ruleta siga girando
initial_speed = 15 #Velocidad inicial de giro

#Botón girar
button_width = 200
button_height = 50
button_x  = 600
button_y = 100
button_color = RED
button_hover_color = YELLOW

#surface lista
show_numbers = False
numbers3 = [2, 4, 5, 6, 7]


#lista números ruleta
roulette_numbers = [32, 15, 19, 4, 21, 2, 25,
                    17, 34, 6, 27, 13, 36, 11,
                    30, 8, 23, 10, 5, 24, 16, 
                    33, 1, 20, 14, 31, 9, 22, 
                    18, 29, 7, 28, 12, 35, 3, 26]

roulette_numbers2 = [0, 32, 15, 19, 4, 21, 2, 25,
                    17, 34, 6, 27, 13, 36, 11,
                    30, 8, 23, 10, 5, 24, 16, 
                    33, 1, 20, 14, 31, 9, 22, 
                    18, 29, 7, 28, 12, 35, 3, 26]

bet_even = pygame.Rect(850, 100, 100, 100)
bet_odd = pygame.Rect(850, 555, 100, 100)
bet_red = pygame.Rect(850, 200, 100, 180)
bet_black = pygame.Rect(850, 380, 100, 180)
bet_column_1 = pygame.Rect(950, 650, 50, 50)
bet_column_2 = pygame.Rect(1050, 650, 50, 50)
bet_column_3 = pygame.Rect(1150, 650, 50, 50)
    
key_space = False

                
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
def app_events():
    global clicked, button_rect, button_rect2, show_numbers

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Botón cerrar ventana
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            button_rect2 = pygame.Rect(button_x, button_y - 50, button_width, button_height)
            click(event.pos, button_rect) #click botón girar ruleta
            click2(event.pos) #click botón mostrar lista números rondas
            clicked = True

        elif event.type == pygame.MOUSEBUTTONUP:
            clicked = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                cambiar_turno(players)


    update_spin()
        
    return True
def cambiar_turno(players):

    jugadores = list(players.keys())

    for i in range(len(jugadores)):
        jugador = jugadores[i]

        if players[jugador]["your_turn"]:
            players[jugador]["your_turn"] = False

            next = (i+1) % len(jugadores)
            next_player = jugadores[next]
            players[next_player]["your_turn"] = True
            print(f"Turno del jugador {next_player}")
            break #El break es para que no lo imprima constantemente


# Fer càlculs
def app_run():
    global lista, clicked, draw_chips, dragging, dragging_chip, mouse_pos, key_space

    if show_numbers: 
        lista = "OCULTAR LISTA" 
    if not show_numbers: 
        lista = "MOSTRAR LISTA"

    # Mostrar la lista de números si está activa
    if show_numbers: 
        surface_x, surface_y = 10, 100
        screen.blit(surface, (surface_x, surface_y))
        surface_numbers()

    if show_numbers and len(numbers3) >= 1:
        numbers_surface = surface_numbers(numbers3)
        screen.blit(numbers_surface, (600, 50))

    mouse_pos = pygame.mouse.get_pos()
    mouse_x, mouse_y = mouse_pos

    offset_x = 0
    offset_y = 0
    height_casilla = 600 / 13
    width_casilla = 300 / 3
    apuesta_done = {}  # Registro de apuestas

    for player in players:
        jugador = players[player]

        if jugador["your_turn"]:
            for ficha in jugador["draw_chips"]:
                puntero = math.sqrt((mouse_x - ficha["x"]) ** 2 + (mouse_y - ficha["y"])**2)

                if clicked and puntero <= ficha["radius"]:
                    if not dragging:
                        dragging = True
                        dragging_chip = ficha
                        offset_x = mouse_x - ficha["x"]
                        offset_y = mouse_y - ficha["y"]
                        print(f"Has pulsado sobre la ficha {ficha['value']}")

                    if dragging and dragging_chip == ficha:
                        dragging_chip["x"] = mouse_x - offset_x
                        dragging_chip["y"] = mouse_y - offset_y
                
                elif not clicked and dragging:

                    for ficha in jugador["draw_chips"]:
                        if bet_even.collidepoint(ficha["x"], ficha["y"]):
                            #registrar_apuestas("par", ficha["value"])
                            print("Has apostado a 'PAR'")
                            apuesta_done["par"] = ficha
                            jugador["bet"]["odd_even"] = "par"
                            jugador["bet_chips"].append(
                                {
                                    "x": ficha["x"],
                                    "y": ficha["y"],
                                    "radius": ficha["radius"],
                                    "color": ficha["color"],
                                    "value": ficha["value"],
                                    "width": ficha["width"],
                                    "type_bet": "par"
                                }
                            )

                            print(jugador["bet_chips"])
                        
                        elif bet_odd.collidepoint(ficha["x"], ficha["y"]):
                            #registrar_apuestas("impar", ficha["value"])
                            print("Has apostado a 'Impar'")
                            apuesta_done["impar"] = ficha
                            jugador["bet"]["odd_even"] = "impar"
                            jugador["bet_chips"].append(
                                {
                                    "x": ficha["x"],
                                    "y": ficha["y"],
                                    "radius": ficha["radius"],
                                    "color": ficha["color"],
                                    "value": ficha["value"],
                                    "width": ficha["width"],
                                    "type_bet": "impar"
                                }
                            )
                        
                        elif bet_red.collidepoint(ficha["x"], ficha["y"]):
                            #registrar_apuestas("rojo", ficha["value"])
                            print("Has apostado al color 'ROJO'")
                            apuesta_done["rojo"] = ficha
                            jugador["bet"]["color"] = "red"
                            jugador["bet_chips"].append(
                                {
                                    "x": ficha["x"],
                                    "y": ficha["y"],
                                    "radius": ficha["radius"],
                                    "color": ficha["color"],
                                    "value": ficha["value"],
                                    "width": ficha["width"],
                                    "type_bet": "rojo"
                                }
                            )
                        
                        elif bet_black.collidepoint(ficha["x"], ficha["y"]):
                            #registrar_apuestas("negro", ficha["value"])
                            print("Has apostado al color 'NEGRO'")
                            jugador["bet"]["color"] = "black"
                            jugador["bet_chips"].append(
                                {
                                    "x": ficha["x"],
                                    "y": ficha["y"],
                                    "radius": ficha["radius"],
                                    "color": ficha["color"],
                                    "value": ficha["value"],
                                    "width": ficha["width"],
                                    "type_bet": "negro"
                                }
                            )
                        
                        elif bet_column_1.collidepoint(ficha["x"], ficha["y"]):
                            #registrar_apuestas("columna_1", ficha["value"])
                            print("Has apostado a la 'PRIMERA COLUMNA'")
                            apuesta_done["columna_1"] = ficha
                            jugador["bet"]["column"] = "1"
                            jugador["bet_chips"].append(
                                {
                                    "x": ficha["x"],
                                    "y": ficha["y"],
                                    "radius": ficha["radius"],
                                    "color": ficha["color"],
                                    "value": ficha["value"],
                                    "width": ficha["width"],
                                    "type_bet": "columna_1"
                                }
                            )
                        
                        elif bet_column_2.collidepoint(ficha["x"], ficha["y"]):
                            #registrar_apuestas("columna_2", ficha["value"])
                            print("Has apostado a la 'SEGUNDA COLUMNA'")
                            apuesta_done["columna_2"] = ficha
                            jugador["bet"]["column"] = "2"
                            jugador["bet_chips"].append(
                                {
                                    "x": ficha["x"],
                                    "y": ficha["y"],
                                    "radius": ficha["radius"],
                                    "color": ficha["color"],
                                    "value": ficha["value"],
                                    "width": ficha["width"],
                                    "type_bet": "columna_2"
                                }
                            )
                        
                        elif bet_column_3.collidepoint(ficha["x"], ficha["y"]):
                            #registrar_apuestas("columna_3", ficha["value"])
                            print("Has apostado a la 'TERCERA COLUMNA'")
                            apuesta_done["columna_3"] = ficha
                            jugador["bet"]["column_3"] = "1"
                            jugador["bet_chips"].append(
                                {
                                    "x": ficha["x"],
                                    "y": ficha["y"],
                                    "radius": ficha["radius"],
                                    "color": ficha["color"],
                                    "value": ficha["value"],
                                    "width": ficha["width"],
                                    "type_bet": "columna_3"
                                }
                            )
                        
                        else:
                            bet_number = None
                            for columna in range(3):
                                for fila in range(12):
                                    pos_x = 950 + columna * width_casilla
                                    pos_y = 100 + fila * height_casilla
                                    rect_casilla = pygame.Rect(pos_x, pos_y, width_casilla, height_casilla)

                                    if rect_casilla.collidepoint(ficha["x"], ficha["y"]):
                                        ficha["x"] = pos_x + width_casilla // 2
                                        ficha["y"] = pos_y + height_casilla // 2
                                        bet_number = chips[columna][fila]
                                        jugador["bet_chips"].append(
                                                                {
                                                                    "x": ficha["x"],
                                                                    "y": ficha["y"],
                                                                    "radius": ficha["radius"],
                                                                    "color": ficha["color"],
                                                                    "value": ficha["value"],
                                                                    "width": ficha["width"],
                                                                    "type_bet": "number",
                                                                    "value_number": bet_number
                                                                }
                                                            )
                                        print(jugador["bet_chips"])
                                
                                if bet_number is not None:
                                    print(f"Has apostado al número: {bet_number}")
                                    #registrar_apuestas("numbers", ficha["value"])
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
    global button_rect, button_rect2
    # Pintar el fons de blanc
    screen.fill(GREY)

    draw_grid()
    
    draw_roulette() #Función draw ruleta
    draw_flecha() #Función dibujar flecha
    button_rect = draw_button(mouse_pos)
    button_rect2 = draw_button2(mouse_pos)
    table() #Función dibujar tabla
    banca() #Función dibujar banca
    tablero_fichas()
    draw_win_number() #Función dibuja número elegido
    
    
    pygame.display.update()

def surface_numbers(numbers3):
    
    space = 30
    width = 200
    height = 500

    numbers_surface = pygame.Surface((width, height))
    numbers_surface.fill(GREEN)

    font = pygame.font.SysFont(None, 24)

    for j, number in enumerate(numbers3):
        text = font.render(f"{j}: {number}", True, WHITE)
        numbers_surface.blit(text, (10, j * space))

    return numbers_surface

def par_impar_event():

    global winning_number
    #Aqui tengo que juntar el numero ganador con algo para que se me pueda relacionar con par o impar
    for player in players:
        jugador = players[player]

        if jugador["bet"]["odd_even"] == "impar":
            for ficha in jugador["draw_chips"]:
                chip_type = f"fitxa_{ficha['value']}"
                chip_cantidad = 1*jugador["chip"].get(chip_type)
                if chip_type in jugador["chips"]:
                    jugador["chip"][chip_type] += chip_cantidad
                else:
                    jugador["chip"][chip_type] = chip_cantidad
                
                jugador["draw_chips"].append({
                    "x": ficha["x"]+5,
                    "y": ficha["y"]+5,
                    "radius": 25,
                    "color": jugador["color"],
                    "value": ficha["value"],
                    "width": 5
                })
        else:
            chip_type = f"fitxa_{ficha['value']}"
            chip_cantidad = 1*jugador["chips"].get(chip_type)
            if chip_type in jugador["chips"]:
                jugador["chips"][chip_type] -= chip_cantidad



def is_click_on_button(pos, button_rect):
    return button_rect.collidepoint(pos)


def click2(pos):
    global show_numbers
    if button_rect2.collidepoint(pos):
        show_numbers = not show_numbers

def click(pos, button_rect):
    global spinning, spin_speed, show_win_number
    if is_click_on_button(pos, button_rect):
        spinning = True
        show_win_number = False
        spin_speed = initial_speed

def draw_win_number():
    if show_win_number and winning_number is not None:
        font = pygame.font.Font(None, 32)
        text = font.render(f"Número ganador: {winning_number}", True, WHITE)
        text_rect = text.get_rect(center=(350, 150))

        panel_rect = text_rect.copy()
        panel_rect.inflate_ip(20, 20) #Aumentar el rectángulo para que se vea mejor el texto
        pygame.draw.rect(screen, BLACK, panel_rect)
        pygame.draw.rect(screen, YELLOW, panel_rect, 2)

        screen.blit(text, text_rect)
#Gira la ruleta con la velocidad inicial y muestra el número ganador
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
            winning_number = roulette_numbers2[sector - 1]
            show_win_number = True
            
def draw_button2(mouse_pos):

    button_rect2 = pygame.Rect(button_x, button_y - 55, button_width, button_height)

    if button_rect2.collidepoint(mouse_pos):
        color = DARK_GREEN
    else:
        color = BLUE
    
    if  show_numbers == True: 
        
        lista = "OCULTAR LISTA"

    elif show_numbers == False: 
        
        lista = "MOSTRAR LISTA"
    
    pygame.draw.rect(screen, color, button_rect2) #Draw button
    pygame.draw.rect(screen, WHITE, button_rect2, 2) #Draw border
    font = pygame.font.Font(None, 36)
    text2 = font.render(lista, True, WHITE)
    text_rect = text2.get_rect(center=(button_x + button_width / 2, button_y + button_height / 2 - 50))
    screen.blit(text2, text_rect)

    return button_rect2

def draw_button(mouse_pos):
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    if button_rect.collidepoint(mouse_pos):
        color = button_hover_color
    else:
        color = button_color
    
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
        (center_x + 250, center_y),
        (center_x + 285, center_y - 10),
        (center_x + 285, center_y + 10),
    ]

    pygame.draw.polygon(screen, RED, points)
    pygame.draw.polygon(screen, YELLOW, points, 2)

#Roulette
def draw_roulette():
    global rad_first, rad_second, spin_angle
    
    rad_first = ((360 / 37) * (math.pi / 180)) - (spin_angle * (math.pi / 180)) #First angle
    rad_second = ((360 / 37) * (math.pi / 180) + (rad_first)) #Second angle

    rad_1 = rad_second
    rad_2 = ((360 / 37) * (math.pi / 180) + (rad_1))

    rad_num = ((360 / 37) * (math.pi / 180) * 5) / 2 - (spin_angle * (math.pi / 180))
    rad_num1 = ((360 / 37) * (math.pi / 180) * 3) / 2 - (spin_angle * (math.pi / 180))
   
    
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

    #Casillas apuesta columna (números)
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


    tablero = []

    #FILAS--COLUMNAS TABLERO APUESTAS
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

            tablero.append({"numero": numbers, "color": color})

    return tablero

def par_par_event(player):

    global winning_number
    
    dictColor = table()

    for i in range(len(dictColor)):
        numero_ganador = dictColor[i]
        print(numero_ganador)

        if numero_ganador == winning_number and numero_ganador % 2 == 0:
            print("Has ganado la apuesta !")

            for ficha in players[player]["bet_chips"]:
                if ficha["type_bet"] == "par":
                    valor_añadir = ficha["value"]
                    chyp_type = f"fitxa_{valor_añadir}"
                    players[player]["chips"][chyp_type] += (1*len(ficha["type_bet"]))
                    players[player]["draw_chips"].append(
                        {
                            "x": ficha["x"],
                            "y": ficha["y"],
                            "radius" : ficha["radius"],
                            "value": ficha["value"],
                            "width": ficha["width"]
                        }
                    )
                else:
                    players[player]["chips"][chyp_type] -= (1*len(ficha["type_bet"]))
                    #Faltaria hacer una variable banca o algo que fuese un diccionario para dibujar todas las fichas que tienen que ir a la banca

            
    """for player in players:
        jugador = players[player]

        if jugador["bet"]["odd_even"] == "par":
            for ficha in jugador["draw_chips"]:
                chip_type = f"fitxa_{ficha['value']}"
                chip_cantidad = 1*jugador["chip"].get(chip_type)
                if chip_type in jugador["chips"]:
                    jugador["chip"][chip_type] += chip_cantidad
                else:
                    jugador["chip"][chip_type] = chip_cantidad
                
                jugador["draw_chips"].append({
                    "x": ficha["x"]+5,
                    "y": ficha["y"]+5,
                    "radius": 25,
                    "color": jugador["color"],
                    "value": ficha["value"],
                    "width": 5
                })
        else:
            chip_type = f"fitxa_{ficha['value']}"
            chip_cantidad = 1*jugador["chips"].get(chip_type)
            if chip_type in jugador["chips"]:
                jugador["chips"][chip_type] -= chip_cantidad"""
    print(dictColor)

def impar_event(player):

    global winning_number
    contador = 0
    dictColor = table()

    for i in range(len(dictColor)):
        numero_ganador = dictColor[i]
        print(numero_ganador)

        if numero_ganador == winning_number and numero_ganador % 2 != 0:
            print("Has ganado la apuesta !")

            for ficha in players[player]["bet_chips"]:
                if ficha["type_bet"] == "impar":
                    contador += 1
                    valor_añadir = ficha["value"]
                    chip_type = f"fitxa_{valor_añadir}"
                    #players[player]["chips"][chyp_type] += (1*contador)
                    players[player]["chips"][chip_type] += (1*len(ficha["type_bet"]))
                    players[player]["draw_chips"].append(
                        {
                            "x": ficha["x"],
                            "y": ficha["y"],
                            "radius" : ficha["radius"],
                            "value": ficha["value"],
                            "width": ficha["width"]
                        }
                    )
                else:
                    #players[player]["chips"][chyp_type] -= (1*contador)
                    players[player]["chips"][chip_type] -= (1*len(ficha["type_bet"]))
                    #Faltaria hacer una variable banca o algo que fuese un diccionario para dibujar todas las fichas que tienen que ir a la banca
#FÚNCION FICHAS
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

#FÚNCION tablero fichas (cambiar)
def tablero_fichas():
    font_text_cantidad = pygame.font.SysFont("Arial", 14, bold=True)
    font_text = pygame.font.SysFont(None, 27)

    for player in players:
        info = players[player]
        if info["your_turn"]:
            # Dibujar el marco del tablero
            pygame.draw.rect(screen, DARK_GREEN, (500, 500, 300, 200))
            pygame.draw.rect(screen, YELLOW, (500, 500, 300, 200), 3)
            pygame.draw.rect(screen, GREEN, (503, 503, 97, 47))
            pygame.draw.line(screen, YELLOW, (500, 550), (600, 550), 3)
            pygame.draw.line(screen, YELLOW, (600, 550), (600, 500), 3)
            pygame.draw.line(screen, YELLOW, (600, 550), (799, 550), 3)
            pygame.draw.rect(screen, GREEN, (603, 503, 97 * 2, 47))

            # Textos
            text_fichas = font_text.render("FICHAS", True, BLACK)
            text_player = font_text.render(player, True, BLACK)
            screen.blit(text_fichas, (520, 520))
            screen.blit(text_player, (640, 517))

            # Dibujar las fichas
            for ficha in info["draw_chips"]:
                chip_type = f"fitxa_{ficha['value']}"
                chip_cantidad = info["chips"].get(chip_type, 0)

                if chip_cantidad > 0:
                    text_cantidad = font_text_cantidad.render(f"x{chip_cantidad}", True, WHITE)
                    text_cantidad_rect = (ficha["x"] + 30, ficha["y"])

                    pygame.draw.circle(screen, WHITE, (ficha["x"], ficha["y"]), ficha["radius"])
                    pygame.draw.circle(screen, info["color"], (ficha["x"], ficha["y"]), ficha["radius"], ficha["width"])
                    screen.blit(text_cantidad, text_cantidad_rect)

                    valor_ficha = font_text_cantidad.render(str(ficha["value"]), True, BLACK)
                    pos_ficha = valor_ficha.get_rect(center=(ficha["x"], ficha["y"]))
                    screen.blit(valor_ficha, pos_ficha)





def registrar_apuestas(tipo_apuesta, tipo_ficha):

    if tipo_ficha not in registro_apuestas[tipo_apuesta]:
        registro_apuestas[tipo_apuesta][tipo_ficha] = 0
    
    elif tipo_ficha in registro_apuestas[tipo_apuesta]:
        registro_apuestas[tipo_apuesta][tipo_ficha] +=1
    
    print(f"Has apostado {registro_apuestas[tipo_apuesta][tipo_ficha]+1} fichas de valor {tipo_ficha} a {tipo_apuesta.capitalize()}")



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





if __name__ == "__main__":
    main()



