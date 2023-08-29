#IMPORTO LAS LIBRERIAS PARA MI JUEGO
import pygame
import os
#FUNCIONES QUE ME PERMITEN MANIPULAR EL JUEGO
from random import randint  #Funcion devuelve numeros aleatorios 
from time import sleep #Funcion 

#ESTRUCTURA DE LA VENTANA DE MI JUEGO
pygame.init() #Funcion init que inicializa el juego
screen = pygame.display.set_mode((450, 450)) #Tamaño ancho y alto de la pantalla
clock = pygame.time.Clock()  #Controlo los fps(frames per second) o cuadros por segundo
pygame.display.set_caption('Juego Simon Dice')#Nombre de la ventana
FONT = pygame.font.Font(pygame.font.match_font('arial'), 50) # Fuentes y tamaño 
FONT_SMALL = pygame.font.Font(pygame.font.match_font('arial'), 20)

#PARA MANTENER ORGANIZADO Y EN POCAS LINEAS MI JUEGO TENDRE QUE CREAR MIS CLASES CON ATRIBUTOS Y FUNCIONALIDADES PARA EMPAQUETAR MIS DATOS
#TAMBIEN CREAR MIS DEFS(FUNCIONES) QUE ME PERMITEN REALIZAR CIERTAS TAREAS ESPECIFICAS, REUTILIZARLAS Y AHORRAR CODIGO.

#DEFINO MI CLASE BUTTON QUE ME PERMITIRA CONFIGURAR MIS BOTONES DE COLORES
class Button:
    def __init__(self, color, dark_color, pos): #Funcion que me permite inicializar los atributos de los botones
        self.color = color
        self.dark_color = dark_color
        self.rect = pygame.Rect(pos)
        self.draw(screen, self.color)

    def draw(self, screen, color): #Funcion que me permite dibujar los rectangulos del juego 
        pygame.draw.rect(screen, color, self.rect)
        pygame.display.update() #Se actualiza la pantalla

    def dark_light(self, screen): #Funcion que me permite oscurecer la luz cuanto se selecciona una tecla
        self.draw(screen, self.dark_color)
        sleep(.5)
        self.draw(screen, self.color)

#DEFINO MI FUNCION CLICK_BUTTON QUE ME PERMITIRA CONFIGURAR EL EVENTO CLICK EN EL BOTON
def click_button(mouse_pos, buttons):
    for button in buttons:
        if button.rect.collidepoint(mouse_pos):
            return button #Devuelvo el boton en el que se hizo click
    return None  #No devuelvo nada si no se hizo click en ningun boton


#DEFINO MIS FUNCIONES QUE ME PERMITIRAN ESCRIBIR TEXTO CON LAS CORDENADAS X e Y
def draw_text(surf, text, font, x, y):
    text_surface = font.render(text, True, (255, 255, 255)) #Color del texto blanco
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y) #Posicion del texto(cordenadas)
    surf.blit(text_surface, text_rect)

def replace_text(): #Funcion que me permite remplazar el texto anterior para mostrar el siguiente 
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, 450, 25))


#EMPIEZO CON LA LOGICA DE MI JUEGO E INICIALIZO MIS VARIABLES A UTILIZAR
end_screen = True #Boolean detiene la ejecucion del juego
running = True  #Booleano ejecuta del juego
simon_turn = True #Boolean le toca a Simon
score = 0 #Puntaje inicializado
correct_list = [] #Creo la lista con los colores finales
index = 0 #Devuelve la posición del elemento en la lista

#LISTA QUE CONTIENE LOS 4 COLORES DEL JUEGO CON SUS TONALIDADES RGB. SON UNA COLECCION DE ELEMENTOS EN UNA LISTA. 
buttons = [ #LISTA DE BOTONES DE COLORES
    Button(pygame.Color('red'), pygame.Color(160, 0, 0), (25, 25, 200, 200)), #Color rojo. Posicion 0
    Button(pygame.Color('green'), pygame.Color(0, 160, 0), (225, 25, 200, 200)), #Color verde. Posicion 1
    Button(pygame.Color('blue'), pygame.Color(0, 0, 160), (25, 225, 200, 200)), #Color azul. Posicion 2
    Button(pygame.Color('yellow'), pygame.Color(160, 160, 0), (225, 225, 200, 200)), #Color amarillo. Posicion 3
    ]

#BUCLE WHILE SE EJECUTARA SIEMPRE QUE LA CONDICION SE MANTENGA, EN ESTE CASO MIENTRAS SE EJECUTA EL JUEGO
while running:
    for event in pygame.event.get(): #Se interactua con los eventos del juego
        if event.type == pygame.QUIT: #Evento si quitan el juego, salimos
            running = False
            end_screen = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not simon_turn: # Si hicieron click y no es el turno de Simon,el usuario puede jugar 
            correct_button = correct_list[index] 
            button = click_button(event.pos, buttons)
            if button is None:  #No se presionan ningun boton y se para el bucle
                break
            elif button == correct_button:  #Si se presiona el boton correcto se suma puntaje
                button.dark_light(screen)
                index += 1 #A la posicion de la lista(color) se le suma otro. Se utiliza un contador y por cada ciclo se suma 1 
                if index == len(correct_list):  #LEN devuelve la cantidad de caracteres en la cadena de colores
                    simon_turn = True
                    score += 1
                    index = 0
            else:  #Si presiona el boton incorrecto se sale del juego y pierde
                running = False

    #CONDICION QUE SE CUMPLE EN CASO DE QUE SEA EL TURNO DE SIMON
    if simon_turn:
        replace_text() #Se remplaza el texto
        draw_text(screen, 'TURNO DE SIMON:', FONT_SMALL, 225, 2) #Salida por pantalla
        pygame.display.update() #Se actualiza la pantalla
        simon_turn = False 
        sleep(.5) #Tiempo de espera del programa
        correct_list.append(buttons[randint(0, 3)]) #De la lista de colores se elige un numero al azar con RANDINT 
        for button in correct_list: 
            button.dark_light(screen)#Boton más oscuro
            sleep(.15) #Tiempo de espera del programa

        #TURNO DEL USUARIO
        replace_text() #Se remplaza el texto
        draw_text(screen, 'TU TURNO:', FONT_SMALL, 225, 2) #Salida por pantalla
        pygame.display.update() #Se actualiza la pantalla
    clock.tick(30) #FPS(frames per second) o cuadros por segundo

#SALIDA POR PANTALLA FINAL CON PUNTUACION
screen.fill((0, 0, 0)) #Pantalla color negro
draw_text(screen, 'JUEGO TERMINADO', FONT, 225, 200) #Textos finales
draw_text(screen, 'PUNTAJE:', FONT, 225, 255)
draw_text(screen, str(score), FONT, 225, 305) #Puntuacion final
pygame.display.update() #Actualiza la pantalla

#BUCLE WHILE SE EJECUTARA SIEMPRE QUE LA CONDICION SE MANTENGA, NO FINALIZA LA VENTANA DE MI JUEGO, NO DESAPARECE Y PODEMOS INTERACTUAR CON ELLA
while end_screen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #Solamente cuando hagamos click en el boton cerrar se cerrara
            end_screen = False 
    clock.tick(30) #FPS(frames per second) o cuadros por segundo