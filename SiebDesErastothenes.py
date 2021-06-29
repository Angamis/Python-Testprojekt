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
pygame.display.set_caption("Sieb des Erastothenes")
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

#variables
numbers_list = []
box_size = 3
font_size_below_100 = 21
font_size = 21 
x_calling = 0
y_calling = 0
x_box_to_box = 10
number_of_horizontal_tiles = 10
is_initialized = FALSE

#FUNCTIONS
#input dialog
def int_input():
    return simpledialog.askinteger(title="Limit", prompt="Wähle bis zu welcher positiven Zahl gerechnet werden soll:")

#create numbered boxes
def create_box(x_coord, y_coord, text_number, color, size, fontsize):
    pygame.draw.rect(screen, color, [x_coord, y_coord, 10*size, 10*size])
    screen.blit(pygame.font.SysFont('Times', fontsize).render(str(text_number), True, color_black), (x_coord + 2 + size, y_coord + 2 + size)) 

#fill a list from 1 to n with ascending numbers
def fill_list(list, n):
    list=[]
    list.extend(range(1, n+1))
    return list

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
        font_size_below_100 = 0
        font_size = 0

    x_box_to_box = 14*box_size
    number_of_horizontal_tiles = math.floor(1190/x_box_to_box)

    return(box_size, font_size_below_100, font_size, x_box_to_box, number_of_horizontal_tiles)


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

            #gets the max number for the sieve
            if 90 <= mouse [0] <=160 and 10 <= mouse[1] <= 40:
                highest_value = int_input()
                if not highest_value:
                    break
                while highest_value < 2 and highest_value > 4250:
                    messagebox.showinfo(title="Fehler", message="Bitte eine positive ganze Zahl zwischen 2 und 4250 eingeben.")
                    highest_value = int_input()
                numbers_list = fill_list(numbers_list, highest_value)
                #sets all parameters for the function create_box()
                box_size, font_size_below_100, font_size, x_box_to_box, number_of_horizontal_tiles = set_parameters(numbers_list)



    #create grid of all numbers up to maximum entered    
    for numbers in numbers_list:

#            x_calling = numbers * 10boxsize+spacing - (10boxsize+spacing-10) - math.floor((numbers - 1) / horizontaltiles) * horizontaltiles*(10boxsize+spacing)
#            y_calling = 100 + math.floor((numbers - 1) / horizontaltiles) * 10boxsize+spacing

        x_calling = (numbers-1) * x_box_to_box + 10 - math.floor((numbers-1)/number_of_horizontal_tiles) * number_of_horizontal_tiles * x_box_to_box
        y_calling = 100 + math.floor((numbers-1) / number_of_horizontal_tiles) * x_box_to_box

        if 1 < numbers < 100:
            create_box(x_calling, y_calling, numbers, color_cyan, box_size, font_size_below_100)
        else:
            create_box(x_calling, y_calling, numbers, color_cyan, box_size, font_size)

        #initial box, empty, without ifelse!!!!
        if numbers == 1:
            create_box(10, 100, "", color_cyan, box_size, 1)
        


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


    pygame.display.update()