import pygame
import math
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
from tkinter.constants import FALSE, TRUE

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

#global constants
#animation is faster, the lower this value is
ANIMATION_SPEED = 50

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
        font_size_below_100 = 25
        font_size = 18
    elif len(list) < 449:
        box_size = 3
        font_size_below_100 = 18
        font_size = 13
    elif len(list) < 1051:
        box_size = 2
        font_size_below_100 = 12
        font_size = 7
    elif len(list) < 4251:
        box_size = 1
        font_size_below_100 = 12
        font_size = 7
    elif len(list) < 17001:
        box_size = 0.5
        font_size_below_100 = 12
        font_size = 7

    x_box_to_box = 14*box_size
    number_of_horizontal_tiles = math.floor(1190/x_box_to_box)

    return(box_size, font_size_below_100, font_size, x_box_to_box, number_of_horizontal_tiles)

#prepare a Surface with all drawn boxes, uses create_box()
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

            #gets the max number for the sieve (Entry button is pressed)
            if 90 <= mouse[0] <=160 and 10 <= mouse[1] <= 40:
                highest_value = int_input()
                if not highest_value:
                    break
                while highest_value < 2 or highest_value > 17000:
                    messagebox.showinfo(title="Fehler", message="Bitte eine positive ganze Zahl zwischen 2 und 17'000 eingeben.")
                    highest_value = int_input()

                if 1 < highest_value <= 17000:
                    numbers_list = fill_list(numbers_list, highest_value)
                    #sets all parameters for the function create_box()
                    box_size, font_size_below_100, font_size, x_box_to_box, number_of_horizontal_tiles = set_parameters(numbers_list)
                    surface = create_boxes()

            #starts the animation and claculation of the prime numbers (Start button is pressed)
            if 170 <= mouse[0] <= 240 and 10 <= mouse[1] <= 40 and numbers_list != []:

                #disables all click interaction with the program
                pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)

                x_calling = 10
                y_calling = 100
                create_box(surface, x_calling, y_calling, "", color_red, box_size, font_size_below_100)
                screen.blit(surface, (0, 0))
                pygame.display.update()

                prime_list = [True for i in range(highest_value+1)]
                color = 0
                p = 2

                while (p * p <= highest_value):
                    if (prime_list[p] == True):

                        
                        #update all multiples of p and animate the sieve
                        for i in range(p * p, highest_value + 1, p):

                            x_calling = (i-1) * x_box_to_box + 10 - math.floor((i-1)/number_of_horizontal_tiles) * number_of_horizontal_tiles * x_box_to_box
                            y_calling = 100 + math.floor((i-1) / number_of_horizontal_tiles) * x_box_to_box

                            #color setter for all multiples of a prime
                            if color == 0:
                                create_box(surface, x_calling, y_calling, "", color_purple, box_size, font_size_below_100)
                            elif color == 1:
                                create_box(surface, x_calling, y_calling, "", color_white, box_size, font_size_below_100)
                            elif color == 2:
                                create_box(surface, x_calling, y_calling, "", color_blue, box_size, font_size_below_100)
                            elif color == 3:
                                create_box(surface, x_calling, y_calling, "", color_green, box_size, font_size_below_100)
                            elif color == 4:
                                create_box(surface, x_calling, y_calling, "", color_yellow, box_size, font_size_below_100)
                            elif color == 5:
                                create_box(surface, x_calling, y_calling, "", color_orange, box_size, font_size_below_100)
                            else:
                                create_box(surface, x_calling, y_calling, "", color_black, box_size, font_size_below_100)
                                color = -1

                            pygame.time.delay(ANIMATION_SPEED)
                            screen.blit(surface, (0, 0))
                            pygame.display.update()

                            prime_list[i] = False

                    #resets color to first one if all are used
                    if color == -1:
                        color = 0
                    else:
                        color += 1

                    p += 1
                
                #makes the program clickable again
                pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)

                #enters the indices of the found primes (and therefore the primes) into a list, romoves entry 0 and 1
                found_primes = [i for i, x in enumerate(prime_list) if x == True]
                found_primes.pop(0)
                found_primes.pop(0)

                #prepares the element with all prime numbers separated by a comma and a space
                comma_and_space = ", "
                output_primes = comma_and_space.join(list(map(str, found_primes)))

                messagebox.showinfo("Ihre Primzahlen:", output_primes)

    #draws all boxes, if there are any present
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