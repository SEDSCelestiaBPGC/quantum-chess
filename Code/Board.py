import pygame
import os
import math
from Pieces import *

pygame.init()

light_square=(255,255,204)
dark_square=(139,69,19)
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
        second_char = chr(ord(second_char)-1)
        position_names.append(str(first_char + second_char))
    first_char = chr(ord(first_char) + 1)
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
    dist = temp = 5000000
    for i in range(0,64):
        dist = distance_formula(pos_mouse,centers[i])
        if dist < temp:
            new_pos = centers[i]
            temp = dist

    return new_pos


#Make Board
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
    col_text=label_font.render(chr(ord('a')+i), True, black)
    row_text=label_font.render(str(8-i), True, black)
    board.blit(col_text, ((i*sq_dim)+22, board_height+8))
    board.blit(row_text, ((board_width+10), (i*sq_dim)+22))
pygame.draw.lines(board, black, True, [(0,0), (board_width, 0), (board_width, board_height), (0, board_height)], 2)
pygame.display.flip()


#Draw Pieces
def pieces():
    board.blit(brook1,brook1_rect)
    board.blit(brook2,brook2_rect)
    board.blit(wrook1,wrook1_rect)
    board.blit(wrook2,wrook2_rect)
    board.blit(bbishop1,bbishop1_rect)
    board.blit(bbishop2,bbishop2_rect)
    board.blit(wbishop1,wbishop1_rect)
    board.blit(wbishop2,wbishop2_rect)
    board.blit(bqueen,bqueen_rect)
    board.blit(wqueen,wqueen_rect)
    board.blit(bknight1,bknight1_rect)
    board.blit(bknight2,bknight2_rect)
    board.blit(wknight1,wknight1_rect)
    board.blit(wknight2,wknight2_rect)
    board.blit(bking,bking_rect)
    board.blit(wking,wking_rect)


selected_pos = [(0,0)]
p = 0


running  = True

while running:
    for event in pygame.event.get():
        for i in range(0,8):
            for j in range(0,8):
                sq_col=cols[(i+j)%2]
                pygame.draw.rect(board, sq_col, ((i*sq_dim), (j*sq_dim), sq_dim, sq_dim))

        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass

        elif event.type == pygame.MOUSEBUTTONUP:
            selected_pos.append(nearest_center(pygame.mouse.get_pos()))
            p+=1

            #rooks
            if selected_pos[p-1] == brook1_rect.center:
                if valid_move_rook(position_name(selected_pos[p-1]),position_name(selected_pos[p])) == True:
                    brook1_rect.center = selected_pos[p]
                    selected_pos.append((0,0))
                    p+=1
            if selected_pos[p-1] == brook2_rect.center:
                if valid_move_rook(position_name(selected_pos[p-1]),position_name(selected_pos[p])) == True:
                    brook2_rect.center = selected_pos[p]
                    selected_pos.append((0,0))
                    p+=1
            if selected_pos[p-1] == wrook1_rect.center:
                if valid_move_rook(position_name(selected_pos[p-1]),position_name(selected_pos[p])) == True:
                    wrook1_rect.center = selected_pos[p]
                    selected_pos.append((0,0))
                    p+=1
            if selected_pos[p-1] == wrook2_rect.center:
                if valid_move_rook(position_name(selected_pos[p-1]),position_name(selected_pos[p])) == True:
                    wrook2_rect.center = selected_pos[p]
                    selected_pos.append((0,0))
                    p+=1

            #bishops
            if selected_pos[p-1] == bbishop1_rect.center:
                if valid_move_bishop(position_name(selected_pos[p-1]),position_name(selected_pos[p])) == True:
                    bbishop1_rect.center = selected_pos[p]
                    selected_pos.append((0,0))
                    p+=1

            if selected_pos[p-1] == bbishop2_rect.center:
                if valid_move_bishop(position_name(selected_pos[p-1]),position_name(selected_pos[p])) == True:
                    bbishop2_rect.center = selected_pos[p]
                    selected_pos.append((0,0))
                    p+=1

            if selected_pos[p-1] == wbishop1_rect.center:
                if valid_move_bishop(position_name(selected_pos[p-1]),position_name(selected_pos[p])) == True:
                    wbishop1_rect.center = selected_pos[p]
                    selected_pos.append((0,0))
                    p+=1

            if selected_pos[p-1] == wbishop2_rect.center:
                if valid_move_bishop(position_name(selected_pos[p-1]),position_name(selected_pos[p])) == True:
                    wbishop2_rect.center = selected_pos[p]
                    selected_pos.append((0,0))
                    p+=1

            #queens
            if selected_pos[p-1] == bqueen_rect.center:
                if valid_move_queen(position_name(selected_pos[p-1]),position_name(selected_pos[p])) == True:
                    bqueen_rect.center = selected_pos[p]
                    selected_pos.append((0,0))
                    p+=1

            if selected_pos[p-1] == wqueen_rect.center:
                if valid_move_queen(position_name(selected_pos[p-1]),position_name(selected_pos[p])) == True:
                    wqueen_rect.center = selected_pos[p]
                    selected_pos.append((0,0))
                    p+=1

            #knights
            if selected_pos[p-1] == bknight1_rect.center:
                if valid_move_knight(position_name(selected_pos[p-1]),position_name(selected_pos[p])) == True:
                    bknight1_rect.center = selected_pos[p]
                    selected_pos.append((0,0))
                    p+=1

            if selected_pos[p-1] == bknight2_rect.center:
                if valid_move_knight(position_name(selected_pos[p-1]),position_name(selected_pos[p])) == True:
                    bknight2_rect.center = selected_pos[p]
                    selected_pos.append((0,0))
                    p+=1

            if selected_pos[p-1] == wknight1_rect.center:
                if valid_move_knight(position_name(selected_pos[p-1]),position_name(selected_pos[p])) == True:
                    wknight1_rect.center = selected_pos[p]
                    selected_pos.append((0,0))
                    p+=1

            if selected_pos[p-1] == wknight2_rect.center:
                if valid_move_knight(position_name(selected_pos[p-1]),position_name(selected_pos[p])) == True:
                    wknight2_rect.center = selected_pos[p]
                    selected_pos.append((0,0))
                    p+=1

            #kings
            if selected_pos[p-1] == bking_rect.center:
                if valid_move_king(position_name(selected_pos[p-1]),position_name(selected_pos[p])) == True:
                    bking_rect.center = selected_pos[p]
                    selected_pos.append((0,0))
                    p+=1

            if selected_pos[p-1] == wking_rect.center:
                if valid_move_king(position_name(selected_pos[p-1]),position_name(selected_pos[p])) == True:
                    wking_rect.center = selected_pos[p]
                    selected_pos.append((0,0))
                    p+=1

        pieces()
        pygame.display.update()



