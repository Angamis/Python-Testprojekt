from tkinter.constants import FALSE, TRUE
import pygame
import math
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox

#initialize pygame
pygame.init()

#create screen
screen = pygame.display.set_mode((1200, 800))

#Title and Icon
pygame.display.set_caption("Sieb des Eratosthenes")
icon = pygame.image.load('sieve.png')
pygame.display.set_icon(icon)

#window for tkinter
window = tk.Tk()
window.withdraw()
window.iconbitmap(default='sieve_icon.ico')

#Color definitions
color_white = (255, 255, 255)
color_black = (0, 0, 0)
color_purple = (102, 0, 204)
color_blue = (0, 51, 204)
color_cyan = ((51, 204, 204))
color_green = (0, 204, 0)
color_yellow = (255, 255, 0)
color_orange = (255, 153, 0)
color_red = (255, 51, 0)
color_brown = (102, 51, 0)

#defining a font
smallfont = pygame.font.SysFont('Corbel', 30)
tinyfont = pygame.font.SysFont('Corbel', 10)

#definitions of text
text_quit = smallfont.render('QUIT' , True , color_black)
text_entry = smallfont.render('Entry' , True , color_black)
text_start = smallfont.render('Start', True, color_black)

#global variables
numbers_list = []
box_size = 3
font_size_below_100 = 21
font_size = 21 
x_box_to_box = 10
number_of_horizontal_tiles = 10


#FUNCTIONS
#input dialog
def int_input():
    return simpledialog.askinteger(title="Limit", prompt="Wähle bis zu welcher positiven Zahl gerechnet werden soll:")

#create numbered boxes
def create_box(surface, x_coord, y_coord, text_number, color, size, fontsize):
    pygame.draw.rect(surface, color, [x_coord, y_coord, 10*size, 10*size])
    surface.blit(pygame.font.SysFont('Times', fontsize).render(str(text_number), True, color_black), (x_coord + 2 + size, y_coord + 2 + size)) 

#fill a list from 1 to n with ascending numbers
def fill_list(list, n):
    list=[]
    list.extend(range(1, n+1))
    return list

#prepare all parameters for create_box()
def set_parameters(list):
    if len(list) < 171:
        box_size = 5
        font_size_below_100 =35
        font_size = 23
    elif len(list) < 253:
        box_size = 4
        font_size_below_100 = 23
        font_size = 16
    elif len(list) < 449:
        box_size = 3
        font_size_below_100 = 16
        font_size = 10
    elif len(list) < 1051:
        box_size = 2
        font_size_below_100 = 10
        font_size = 6
    elif len(list) < 4251:
        box_size = 1
        font_size_below_100 = 10
        font_size = 6
    elif len(list) < 17001:
        box_size = 0.5
        font_size_below_100 = 10
        font_size = 6


    x_box_to_box = 14*box_size
    number_of_horizontal_tiles = math.floor(1190/x_box_to_box)

    return(box_size, font_size_below_100, font_size, x_box_to_box, number_of_horizontal_tiles)

#prepare a Surface with all drawn rectangels
def create_boxes():

    surf = pygame.Surface((1200, 800))
    surf.fill(color_brown)

    #creates all boxes up to the highest value that got entered by user, above 1050, no text will be drawn
    if len(numbers_list) < 1051:   
        for numbers in numbers_list:

            x_calling = (numbers-1) * x_box_to_box + 10 - math.floor((numbers-1)/number_of_horizontal_tiles) * number_of_horizontal_tiles * x_box_to_box
            y_calling = 100 + math.floor((numbers-1) / number_of_horizontal_tiles) * x_box_to_box

            if 1 < numbers < 100:
                create_box(surf, x_calling, y_calling, numbers, color_cyan, box_size, font_size_below_100)
            else:
                create_box(surf, x_calling, y_calling, numbers, color_cyan, box_size, font_size)

            #initial box, empty
            if numbers == 1:
                create_box(surf, 10, 100, "", color_cyan, box_size, 1)
    else:
        for numbers in numbers_list:

            x_calling = (numbers-1) * x_box_to_box + 10 - math.floor((numbers-1)/number_of_horizontal_tiles) * number_of_horizontal_tiles * x_box_to_box
            y_calling = 100 + math.floor((numbers-1) / number_of_horizontal_tiles) * x_box_to_box

            if 0 < numbers < 100:
                create_box(surf, x_calling, y_calling, "", color_cyan, box_size, font_size_below_100)
            else:
                create_box(surf, x_calling, y_calling, "", color_cyan, box_size, font_size)

    return surf



#main loop
while True:

    screen.fill(color_brown)
    mouse = pygame.mouse.get_pos()

    #catch all events here
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            #checks if the QUIT button is pressed
            if 10 <= mouse[0] <= 80 and 10 <= mouse[1] <= 40:
                result = messagebox.askyesno(title="Exit", message="Sie sind dabei, die Anwendung zu schliessen. Fortfahren?",icon='info', default='no')
                if result == True:
                    pygame.quit()

            #gets the max number for the sieve (Entry button)
            if 90 <= mouse[0] <=160 and 10 <= mouse[1] <= 40:
                highest_value = int_input()
                if not highest_value:
                    break
                while highest_value < 2 and highest_value > 17000:
                    messagebox.showinfo(title="Fehler", message="Bitte eine positive ganze Zahl zwischen 2 und 17'000 eingeben.")
                    highest_value = int_input()
                numbers_list = fill_list(numbers_list, highest_value)
                #sets all parameters for the function create_box()
                box_size, font_size_below_100, font_size, x_box_to_box, number_of_horizontal_tiles = set_parameters(numbers_list)
                surface = create_boxes()

            if 170 <= mouse[0] <= 240 and 10 <= mouse[1] <= 40 and numbers_list != []:

                x_calling = 10
                y_calling = 100
                create_box(surface, x_calling, y_calling, "", color_red, box_size, font_size_below_100)
                screen.blit(surface, (0, 0))
                pygame.display.update()

                prime_list = [True for i in range(highest_value+1)]

                p = 2
                while (p * p <= highest_value):
                    if (prime_list[p] == True):

                        
                        #update all multiples of p and also animation here
                        for i in range(p * p, highest_value + 1, p):

                            x_calling = (i-1) * x_box_to_box + 10 - math.floor((i-1)/number_of_horizontal_tiles) * number_of_horizontal_tiles * x_box_to_box
                            y_calling = 100 + math.floor((i-1) / number_of_horizontal_tiles) * x_box_to_box
                            create_box(surface, x_calling, y_calling, "", color_purple, box_size, font_size_below_100)
                            pygame.time.delay(50)
                            screen.blit(surface, (0, 0))
                            pygame.display.update()

                            prime_list[i] = False

                    
                    p += 1



    if numbers_list != []:    
        screen.blit(surface, (0, 0))


    #drawing of the 'QUIT' button
    if 10 <= mouse[0] <= 80 and 10 <= mouse[1] <= 40:
        pygame.draw.rect(screen, color_red, [10, 10, 70, 30])
    else:
        pygame.draw.rect(screen, color_green, [10, 10, 70, 30])     
    screen.blit(text_quit, (12, 12))

    #drawing of the 'Entry' button
    if 90 <= mouse[0] <= 160 and 10 <= mouse[1] <= 40:
        pygame.draw.rect(screen, color_green, [90, 10, 70, 30])
    else:
        pygame.draw.rect(screen, color_cyan, [90, 10, 70, 30])     
    screen.blit(text_entry, (92, 12))    

    #drawing of the 'Start' button
    if 170 <= mouse[0] <= 240 and 10 <= mouse[1] <= 40 and numbers_list != []:
        pygame.draw.rect(screen, color_green, [170, 10, 70, 30])
    elif 170 <= mouse[0] <= 240 and 10 <= mouse[1] <= 40 and numbers_list == []:
        pygame.draw.rect(screen, color_red, [170, 10, 70, 30])
    else: 
        pygame.draw.rect(screen, color_cyan, [170, 10, 70, 30])
    screen.blit(text_start, (172, 12))

    pygame.display.update()