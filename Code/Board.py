import pygame
import os
from pygame.locals import *
import math

light_square=(255,255,204)
dark_square=(26,4,0)
white=(255,255,255)
black=(0,0,0)
grey=(169,169,169)

#list of centers
centers = []

x_center = 30
y_center = 30

while x_center != 510:
    while y_center != 510:
        centers.append((x_center, y_center))
        y_center += 60
    x_center += 60
    y_center = 30

#list of positons of squares

position_names =['a8']

first_char = position_names[0][slice(1)]
second_char = position_names[0][slice(1,2)]

while ord(first_char) != 105:
    while ord(second_char) != 49:
        new_ascii_value = ord(second_char)-1
        second_char = chr(new_ascii_value)
        new_pos = first_char + second_char
        position_names.append(str(new_pos))
    new_ascii_value = ord(first_char)+ 1
    first_char = chr(new_ascii_value)
    second_char = '9'

#function to identify name of posiiion on which the piece exists
def position_name(pos):
    for i in range (0,64):
        if pos == centers[i]:
            pos_name = position_names[i]

    return pos_name

#nearest center to the mouseclick
def square(x):
    return x * x

def distance_formula(pos1, pos2):
    # pos1 and pos2 are tuples of 2 numbers
    return math.sqrt(square(pos2[0] - pos1[0]) + square(pos2[1] - pos1[1]))

def nearest_center (pos_mouse):
    #x, y = pygame.mouse.get_pos()
    #pos_mouse = (x,y)
    dist = temp = 5000000
    for i in range(0,64):
        dist = distance_formula(pos_mouse,centers[i])
        if dist < temp:
            new_pos = centers[i]
            temp = dist

    return new_pos


#function to test valid move of rooks
def valid_move_rook (old_pos_name,new_pos_name):
    if old_pos_name[slice(1)] == new_pos_name[slice(1)]:
        return True
    if old_pos_name[slice(1,2)] == new_pos_name[slice(1,2)]:
        return True
    else:
        return False

#initiate Rooks
brook1 = pygame.image.load("/home/lenovo/Desktop/Q-Computing/QOSI/quantum-chess/Media/BlackRook.png")
brook1 = pygame.transform.scale(brook1,(50,50))
brook1_rect = brook1.get_rect()
brook1_rect.center = 30,30

brook2 = pygame.image.load("/home/lenovo/Desktop/Q-Computing/QOSI/quantum-chess/Media/BlackRook.png")
brook2 = pygame.transform.scale(brook2,(50,50))
brook2_rect = brook2.get_rect()
brook2_rect.center = 450,30

wrook1 = pygame.image.load("/home/lenovo/Desktop/Q-Computing/QOSI/quantum-chess/Media/WhiteRook.png")
wrook1 = pygame.transform.scale(wrook1,(50,50))
wrook1_rect = wrook1.get_rect()
wrook1_rect.center = 450,450

wrook2 = pygame.image.load("/home/lenovo/Desktop/Q-Computing/QOSI/quantum-chess/Media/WhiteRook.png")
wrook2 = pygame.transform.scale(wrook2,(50,50))
wrook2_rect = wrook2.get_rect()
wrook2_rect.center = 30,450




def make_board():
    pygame.init()
    board_width=480
    margin=30
    board_height=board_width
    board = pygame.display.set_mode((board_width+margin, board_height+margin))
    board.fill(white)
    cols=[light_square, dark_square]
    sq_dim=board_width/8

    for i in range(0,8):
        for j in range(0,8):
            sq_col=cols[(i+j)%2]
            pygame.draw.rect(board, sq_col, ((i*sq_dim), (j*sq_dim), sq_dim, sq_dim))

    label_font=pygame.font.SysFont("calibri", 18)

    for i in range(0,8):
        #pygame.draw.line(board, grey, (board_width, (i+1)*sq_dim), (board_width+margin, (i+1)*sq_dim), 2)
        #pygame.draw.line(board, grey, ((i+1)*sq_dim, board_height), ((i+1)*sq_dim, board_height+margin), 2)
        col_text=label_font.render(chr(ord('A')+i), True, black)
        row_text=label_font.render(str(8-i), True, black)
        board.blit(col_text, ((i*sq_dim)+22, board_height+8))
        board.blit(row_text, ((board_width+10), (i*sq_dim)+22))
    pygame.draw.lines(board, black, True, [(0,0), (board_width, 0), (board_width, board_height), (0, board_height)], 2)

    pygame.display.flip()

    def rooks():
        board.blit(brook1,brook1_rect)
        board.blit(brook2,brook2_rect)
        board.blit(wrook1,wrook1_rect)
        board.blit(wrook2,wrook2_rect)


    selected_pos = [(0,0)]
    p=0
    moving =  False

    while True:
        for event in pygame.event.get():
            for i in range(0,8):
                for j in range(0,8):
                    sq_col=cols[(i+j)%2]
                    pygame.draw.rect(board, sq_col, ((i*sq_dim), (j*sq_dim), sq_dim, sq_dim))
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

            elif event.type == MOUSEBUTTONDOWN:
                pass

            elif event.type == MOUSEBUTTONUP:
                moving = False
                x, y = pygame.mouse.get_pos()
                selected_pos.append(nearest_center((x,y)))
                p+=1

                if selected_pos[p-1] == brook1_rect.center:
                    old_pos_name = position_name(selected_pos[p-1])
                    new_pos_name = position_name(selected_pos[p])
                    if valid_move_rook(old_pos_name,new_pos_name) == True:
                        brook1_rect.center = selected_pos[p]
                        selected_pos.append((0,0))
                        p+=1
                if selected_pos[p-1] == brook2_rect.center:
                    old_pos_name = position_name(selected_pos[p-1])
                    new_pos_name = position_name(selected_pos[p])
                    if valid_move_rook(old_pos_name,new_pos_name) == True:
                        brook2_rect.center = selected_pos[p]
                        selected_pos.append((0,0))
                        p+=1
                if selected_pos[p-1] == wrook1_rect.center:
                    old_pos_name = position_name(selected_pos[p-1])
                    new_pos_name = position_name(selected_pos[p])
                    if valid_move_rook(old_pos_name,new_pos_name) == True:
                        wrook1_rect.center = selected_pos[p]
                        selected_pos.append((0,0))
                        p+=1

                if selected_pos[p-1] == wrook2_rect.center:
                    old_pos_name = position_name(selected_pos[p-1])
                    new_pos_name = position_name(selected_pos[p])
                    if valid_move_rook(old_pos_name,new_pos_name) == True:
                        wrook2_rect.center = selected_pos[p]
                        selected_pos.append((0,0))
                        p+=1

            rooks()
            pygame.display.update()





make_board()
