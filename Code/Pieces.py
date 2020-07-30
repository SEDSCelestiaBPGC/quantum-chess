import pygame
import os
from pygame.locals import *
import math


transparent = (0, 0, 0, 0)

# list of centers
centers = []
centrans = []  # transpose of centers
# required due to indexation issues with centers

x_center = 30
y_center = 30

while x_center != 510:
    while y_center != 510:
        centers.append((x_center, y_center))
        centrans.append((y_center, x_center))
        y_center += 60
    x_center += 60
    y_center = 30

# list of positons of squares

position_names = ['a8']

first_char = position_names[0][slice(1)]
second_char = position_names[0][slice(1, 2)]

while ord(first_char) != 105:
    while ord(second_char) != 49:
        second_char = chr(ord(second_char) - 1)
        position_names.append(str(first_char + second_char))
    first_char = chr(ord(first_char) + 1)
    second_char = '9'

# List of pieces

pieceslist = ['brook1', 'bknight1', 'bbishop1', 'bqueen', 'bking', 'bbishop2', 'bknight2', 'brook2',
              'bpawn1', 'bpawn2', 'bpawn3', 'bpawn4', 'bpawn5', 'bpawn6', 'bpawn7', 'bpawn8',
              'wpawn1', 'wpawn2', 'wpawn3', 'wpawn4', 'wpawn5', 'wpawn6', 'wpawn7', 'wpawn8',
              'wrook1', 'wknight1', 'wbishop1', 'wqueen', 'wking', 'wbishop2', 'wknight2', 'wrook2']

#   (Dictionary) boardstate :To store centere as key having pieceID as its value
boardstate = dict()  # Basically I put in center (centrans) value to get the name of piece (or 'empty') over it

for i in range(0, 16):
    boardstate[centrans[i]] = pieceslist[i]
for i in range(16, 48):
    boardstate[centrans[i]] = 'empty'
for i in range(48, 64):
    j = i - 32  # j= (i-48) + 16
    boardstate[centrans[i]] = pieceslist[j]

movedpiece = ''

# Function to update BoardState(BS)
def bsupdate(s_pos_o, s_pos_n):
    global movedpiece
    for j in range(0, 64):
        if s_pos_o == centrans[j]:
            movedpiece = boardstate[centrans[j]]
            boardstate[centrans[j]] = 'empty'
    for j in range(0, 64):
        if s_pos_n == centrans[j]:
            boardstate[centrans[j]] = movedpiece
    print(movedpiece, 'moved to', position_name(s_pos_n))
    #print('Board State: ', boardstate)


def isoccupied(pos):  # returns 0 if empty; 1 if occupied
    r = 0
    for i in range(0, 64):
        if pos == centrans[i]:
            if boardstate[centrans[i]] != 'empty':
                r = 1
            break
    return r

# function to identify name of posiiion on which the piece exists
def position_name(pos):
    for i in range(0, 64):
        if pos == centers[i]:
            pos_name = position_names[i]
    return pos_name

# nearest center to the mouseclick
def square(x):
    return x * x

def distance_formula(pos1, pos2):
    # pos1 and pos2 are tuples of 2 numbers
    return math.sqrt(square(pos2[0] - pos1[0]) + square(pos2[1] - pos1[1]))

def nearest_center(pos_mouse):
    # x, y = pygame.mouse.get_pos()
    # pos_mouse = (x,y)
    dist = temp = 5000000
    for i in range(0, 64):
        dist = distance_formula(pos_mouse, centers[i])
        if dist < temp:
            new_pos = centers[i]
            temp = dist
    return new_pos


# Identifying whether the king is in check or not:- to prevent castling
def check():
    return False


# To verify if the king can castle or not
def castle():
    return False


def unbritfn(cap_P):  # unbrit function;   cap_P= captured piece
    if cap_P == 'brook1':
        brook1.fill(transparent)
        brook1_rect.center = 2450, 2560
    if cap_P == 'brook2':
        brook2.fill(transparent)
        brook2_rect.center = 2050, 2870
    if cap_P == 'wrook1':
        wrook1.fill(transparent)
        wrook1_rect.center = 1010, 2020
    if cap_P == 'wrook2':
        wrook2.fill(transparent)
        wrook2_rect.center = 2068, 1054

    if cap_P == 'bknight1':
        bknight1.fill(transparent)
        bknight1_rect.center = 2760, 2340
    if cap_P == 'bknight2':
        bknight2.fill(transparent)
        bknight2_rect.center = 2110, 2240
    if cap_P == 'wknight1':
        wknight1.fill(transparent)
        wknight1_rect.center = 2000, 4000
    if cap_P == 'wknight2':
        wknight2.fill(transparent)
        wknight2_rect.center = 3000, 2000

    if cap_P == 'bbishop1':
        bbishop1.fill(transparent)
        bbishop1_rect.center = 3000, 3000
    if cap_P == 'bbishop2':
        bbishop2.fill(transparent)
        bbishop2_rect.center = 4000, 4000
    if cap_P == 'wbishop1':
        wbishop1.fill(transparent)
        wbishop1_rect.center = 4000, 2000
    if cap_P == 'wbishop2':
        wbishop2.fill(transparent)
        wbishop2_rect.center = 2000, 3000

    if cap_P == 'bqueen':
        bqueen.fill(transparent)
        bqueen_rect.center = 2000, 2000
    if cap_P == 'wqueen':
        wqueen.fill(transparent)
        wqueen_rect.center = 2000, 2000
    if cap_P == 'bking':
        bking.fill(transparent)
        bking_rect.center = 2000, 2000
    if cap_P == 'wking':
        wking.fill(transparent)
        wking_rect.center = 2000, 2000

    if cap_P == 'bpawn1':
        bpawn1.fill(transparent)
        bpawn1_rect.center = 2000, 2000
    if cap_P == 'bpawn2':
        bpawn2.fill(transparent)
        bpawn2_rect.center = 2000, 2000
    if cap_P == 'bpawn3':
        bpawn3.fill(transparent)
        bpawn3_rect.center = 2000, 2000
    if cap_P == 'bpawn4':
        bpawn4.fill(transparent)
        bpawn4_rect.center = 2000, 2000
    if cap_P == 'bpawn5':
        bpawn5.fill(transparent)
        bpawn5_rect.center = 2000, 2000
    if cap_P == 'bpawn6':
        bpawn6.fill(transparent)
        bpawn6_rect.center = 2000, 2000
    if cap_P == 'bpawn7':
        bpawn7.fill(transparent)
        bpawn7_rect.center = 2000, 2000
    if cap_P == 'bpawn8':
        bpawn8.fill(transparent)
        bpawn8_rect.center = 2000, 2000
    if cap_P == 'wpawn1':
        wpawn1.fill(transparent)
        wpawn1_rect.center = 2000, 2000
    if cap_P == 'wpawn2':
        wpawn2.fill(transparent)
        wpawn2_rect.center = 2000, 2000
    if cap_P == 'wpawn3':
        wpawn3.fill(transparent)
        wpawn3_rect.center = 2000, 2000
    if cap_P == 'wpawn4':
        wpawn4.fill(transparent)
        wpawn4_rect.center = 2000, 2000
    if cap_P == 'wpawn5':
        wpawn5.fill(transparent)
        wpawn5_rect.center = 2000, 2000
    if cap_P == 'wpawn6':
        wpawn6.fill(transparent)
        wpawn6_rect.center = 2000, 2000
    if cap_P == 'wpawn7':
        wpawn7.fill(transparent)
        wpawn7_rect.center = 2000, 2000
    if cap_P == 'wpawn8':
        wpawn8.fill(transparent)
        wpawn8_rect.center = 2000, 2000


capturedpieces = ['empty']


# Capture
def capture(s_pos_o, s_pos_n):
    for i in range(0, 64):
        if s_pos_n == centrans[i]:
            capturedpiece = boardstate[centrans[i]]
        if s_pos_o == centrans[i]:
            Cpiece = boardstate[centrans[i]]  # Cpiece = capturing piece
    if capturedpiece[slice(1)] != Cpiece[slice(1)]:
        unbritfn(capturedpiece)
        print(Cpiece, 'captured ', capturedpiece)
        capturedpieces.append(capturedpiece)
        print('Captured Pieces: ', capturedpieces)
        return 1
    else:
        return 0


# for rook, queen, bishop, pawns; pc=piece; Func to identify state (if the sq.s is occupied or not) of squares b/w initial and final position
def in_bw_pieces(s_pos_o, s_pos_n, pc):  # returns 0 if in between sq.s are occupied
    (x_o, y_o) = s_pos_o
    (x_n, y_n) = s_pos_n
    if pc == 'rook':
        if x_n == x_o:
            for i in range(60, 6 * 60, 60):
                j = i
                if y_o > y_n:
                    j = -i
                if (x_o, y_o + j) != s_pos_n:
                    if isoccupied((x_o, y_o + j)) == 1:
                        return 0
                else:
                    return 1
        if y_n == y_o:
            for i in range(60, 6 * 60, 60):
                j = i
                if x_o > x_n:
                    j = -i
                if (x_o + j, y_o) != s_pos_n:
                    if isoccupied((x_o + j, y_o)) == 1:
                        return 0
                else:
                    return 1
    if pc == 'bishop':
        for i in range(60, 6 * 60, 60):
            j = i
            k = i
            if y_o > y_n:
                j = -i
            if x_o > x_n:
                k = -i
            if (x_o + k, y_o + j) != s_pos_n:
                if isoccupied((x_o + k, y_o + j)) == 1:
                    return 0
            else:
                return 1
    if pc == 'queen':
        if x_n == x_o or y_n == y_o:
            if x_n == x_o:
                for i in range(60, 6 * 60, 60):
                    j = i
                    if y_o > y_n:
                        j = -i
                    if (x_o, y_o + j) != s_pos_n:
                        if isoccupied((x_o, y_o + j)) == 1:
                            return 0
                    else:
                        return 1
            else:
                for i in range(60, 6 * 60, 60):
                    j = i
                    if x_o > x_n:
                        j = -i
                    if (x_o + j, y_o) != s_pos_n:
                        if isoccupied((x_o + j, y_o)) == 1:
                            return 0
                    else:
                        return 1

        for i in range(60, 6 * 60, 60):
            j = i
            k = i
            if y_o > y_n:
                j = -i
            if x_o > x_n:
                k = -i
            if (x_o + k, y_o + j) != s_pos_n:
                if isoccupied((x_o + k, y_o + j)) == 1:
                    return 0
            else:
                return 1
    if pc == 'bpawn':
        if isoccupied((x_o, y_o + 60)) == 1:
            return 0
        elif isoccupied((x_o, y_o + 120)) == 1:
            return 0
        else:
            return 1
    if pc == 'wpawn':
        if isoccupied((x_o, y_o - 60)) == 1:
            return 0
        elif isoccupied((x_o, y_o - 120)) == 1:
            return 0
        else:
            return 1


# function to test valid move of Kings..
def valid_move_king(s_pos_o, s_pos_n,selected_pos,p):  # Selected-POSition-Old/New
    if distance_formula(s_pos_n, s_pos_o) < 120:
        if isoccupied(selected_pos[p]) == 1:
            temp = capture(selected_pos[p - 1], selected_pos[p])
            if temp != 0:
                bsupdate(s_pos_o, s_pos_n)
                return True
            else:
                return False
        bsupdate(s_pos_o, s_pos_n)
        return True
    else:
        return False


# function to test valid move of rooks..
def valid_move_rook(old_pos_name, new_pos_name,selected_pos,p):
    if in_bw_pieces(selected_pos[p - 1], selected_pos[p], 'rook') == 0:
        return False
    elif old_pos_name[slice(1)] == new_pos_name[slice(1)]:
        if isoccupied(selected_pos[p]) == 1:
            temp = capture(selected_pos[p - 1], selected_pos[p])
            if temp != 0:
                bsupdate(selected_pos[p - 1], selected_pos[p])
                return True
            else:
                return False
        bsupdate(selected_pos[p - 1], selected_pos[p])
        return True
    elif old_pos_name[slice(1, 2)] == new_pos_name[slice(1, 2)]:
        if isoccupied(selected_pos[p]) == 1:
            temp = capture(selected_pos[p - 1], selected_pos[p])
            if temp != 0:
                bsupdate(selected_pos[p - 1], selected_pos[p])
                return True
            else:
                return False
        bsupdate(selected_pos[p - 1], selected_pos[p])
        return True
    else:
        return False


# function to test valid move of bishops..
def valid_move_bishop(old_pos_name, new_pos_name, s_pos_o, s_pos_n,selected_pos,p):
    nxoy = (new_pos_name[slice(1)] + old_pos_name[slice(1, 2)])  # Newpos-X Oldpos-Y
    nyox = (old_pos_name[slice(1)] + new_pos_name[slice(1, 2)])  # Newpos-Y Oldpos-X
    #   Getting centres for nxoy and nyox
    for k in range(0, 64):
        if nxoy == position_names[k]:
            c_nxoy = centers[k]
        if nyox == position_names[k]:
            c_nyox = centers[k]
    if in_bw_pieces(selected_pos[p - 1], selected_pos[p], 'bishop') == 0:
        return False
    if isoccupied(s_pos_n) == 1:
        temp = capture(s_pos_o, s_pos_n)
        if temp != 0:
            bsupdate(s_pos_o, s_pos_n)
            return True
        else:
            return False
    # if distance b/w (nyox and oldpos) and (nxoy and oldpos) is same, return True
    elif (distance_formula(c_nyox, s_pos_o) == distance_formula(c_nxoy, s_pos_o)):
        bsupdate(s_pos_o, s_pos_n)
        return True
    else:
        return False


# function to test valid move of Knights..
def valid_move_knight(s_pos_o, s_pos_n,selected_pos,p):  # Selected-POSition-Old/New
    if distance_formula(s_pos_n, s_pos_o) == math.sqrt(5 * 60 * 60):  # 134.16407864998737
        if isoccupied(selected_pos[p]) == 1:
            temp = capture(selected_pos[p - 1], selected_pos[p])
            if temp == 1:
                bsupdate(s_pos_o, s_pos_n)
                return True
            else:
                return False
        bsupdate(s_pos_o, s_pos_n)
        return True
    else:
        return False


# function to test valid move of Queens..
def valid_move_queen(old_pos_name, new_pos_name, s_pos_o, s_pos_n,selected_pos,p):
    nxoy = (new_pos_name[slice(1)] + old_pos_name[slice(1, 2)])  # Newpos-X Oldpos-Y
    nyox = (old_pos_name[slice(1)] + new_pos_name[slice(1, 2)])  # Newpos-Y Oldpos-X
    #   Getting centres for nxoy and nyox
    for k in range(0, 64):
        if nxoy == position_names[k]:
            c_nxoy = centers[k]
        if nyox == position_names[k]:
            c_nyox = centers[k]
    if in_bw_pieces(selected_pos[p - 1], selected_pos[p], 'queen') == 0:
        return False
    if isoccupied(s_pos_n) == 1:
        temp = capture(s_pos_o, s_pos_n)
        if temp == 1:
            bsupdate(s_pos_o, s_pos_n)
            return True
        else:
            return False
    # if distance b/w (nyox and oldpos) and (nxoy and oldpos) is same, return True
    elif (distance_formula(c_nyox, s_pos_o) == distance_formula(c_nxoy, s_pos_n)):
        bsupdate(s_pos_o, s_pos_n)
        return True
    elif old_pos_name[slice(1)] == new_pos_name[slice(1)]:
        bsupdate(s_pos_o, s_pos_n)
        return True
    elif old_pos_name[slice(1, 2)] == new_pos_name[slice(1, 2)]:
        bsupdate(s_pos_o, s_pos_n)
        return True
    else:
        return False


# function to test valid move of black Pawns...
def valid_move_bpawn(old_pos_name, new_pos_name, s_pos_o, s_pos_n,selected_pos,p):  # Selected-POSition-Old/New
    if old_pos_name[slice(1)] == new_pos_name[slice(1)]:
        if distance_formula(s_pos_n, s_pos_o) == 120:
            if in_bw_pieces(selected_pos[p - 1], selected_pos[p], 'bpawn') == 0:
                return False
            if old_pos_name[slice(1, 2)] == '7':
                bsupdate(s_pos_o, s_pos_n)
                return True
        elif distance_formula(s_pos_n, s_pos_o) == 60:
            if isoccupied(s_pos_n) == 1:
                return False
            if ord(old_pos_name[slice(1, 2)]) > ord(new_pos_name[slice(1, 2)]):
                bsupdate(s_pos_o, s_pos_n)
                return True
    # capture by pawn
    elif distance_formula(s_pos_n, s_pos_o) == 60 * math.sqrt(2):  # 84.8528137423857
        if ord(old_pos_name[slice(1, 2)]) > ord(new_pos_name[slice(1, 2)]):
            if isoccupied(s_pos_n) == 1:
                temp = capture(selected_pos[p - 1], selected_pos[p])
                if temp == 1:
                    bsupdate(s_pos_o, s_pos_n)
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False


# function to test valid move of white Pawns...
def valid_move_wpawn(old_pos_name, new_pos_name, s_pos_o, s_pos_n,selected_pos,p):  # Selected-POSition-Old/New
    if old_pos_name[slice(1)] == new_pos_name[slice(1)]:
        if distance_formula(s_pos_n, s_pos_o) == 120:
            if in_bw_pieces(selected_pos[p - 1], selected_pos[p], 'wpawn') == 0:
                return False
            if old_pos_name[slice(1, 2)] == '2':
                bsupdate(s_pos_o, s_pos_n)
                return True
        elif distance_formula(s_pos_n, s_pos_o) == 60:
            if isoccupied(s_pos_n) == 1:
                return False
            if ord(old_pos_name[slice(1, 2)]) < ord(new_pos_name[slice(1, 2)]):
                bsupdate(s_pos_o, s_pos_n)
                return True
    # capture by pawn
    elif distance_formula(s_pos_n, s_pos_o) == 60 * math.sqrt(2):  # 84.8528137423857
        if ord(old_pos_name[slice(1, 2)]) < ord(new_pos_name[slice(1, 2)]):
            if isoccupied(s_pos_n) == 1:
                temp = capture(selected_pos[p - 1], selected_pos[p])
                if temp == 1:
                    bsupdate(s_pos_o, s_pos_n)
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False

#   To set alternate turns for White and Black
def turn(selected_pos,p):
    for i in range(0, 64):
        if selected_pos[p] != centrans[i]:
            continue
        else:
            selectedpiece = boardstate[selected_pos[p]]
            print(selectedpiece, 'Selected')
            if selectedpiece[slice(1)] == movedpiece[slice(1)]:
                print('Other player should move')
                selected_pos = selected_pos[:-1]
                p -= 1
                print(selectedpiece, 'Unselected')
                return False
            else:
                return True

brook1 = pygame.image.load("../Media/BlackRook.png")
brook1 = pygame.transform.scale(brook1, (50, 50))
brook1_rect = brook1.get_rect()
brook1_rect.center = 30, 30

brook2 = pygame.image.load("../Media/BlackRook.png")
brook2 = pygame.transform.scale(brook2, (50, 50))
brook2_rect = brook2.get_rect()
brook2_rect.center = 450, 30

wrook1 = pygame.image.load("../Media/WhiteRook.png")
wrook1 = pygame.transform.scale(wrook1, (50, 50))
wrook1_rect = wrook1.get_rect()
wrook1_rect.center = 30, 450

wrook2 = pygame.image.load("../Media/WhiteRook.png")
wrook2 = pygame.transform.scale(wrook2, (50, 50))
wrook2_rect = wrook2.get_rect()
wrook2_rect.center = 450, 450

# initiate Bishops
bbishop1 = pygame.image.load("../Media/BlackBishop.png")
bbishop1 = pygame.transform.scale(bbishop1, (50, 50))
bbishop1_rect = bbishop1.get_rect()
bbishop1_rect.center = 150, 30

bbishop2 = pygame.image.load("../Media/BlackBishop.png")
bbishop2 = pygame.transform.scale(bbishop2, (50, 50))
bbishop2_rect = bbishop2.get_rect()
bbishop2_rect.center = 330, 30

wbishop1 = pygame.image.load("../Media/WhiteBishop.png")
wbishop1 = pygame.transform.scale(wbishop1, (50, 50))
wbishop1_rect = wbishop1.get_rect()
wbishop1_rect.center = 150, 450

wbishop2 = pygame.image.load("../Media/WhiteBishop.png")
wbishop2 = pygame.transform.scale(wbishop2, (50, 50))
wbishop2_rect = wbishop2.get_rect()
wbishop2_rect.center = 330, 450

# initiate Knights
bknight1 = pygame.image.load("../Media/BlackKnight.png")
bknight1 = pygame.transform.scale(bknight1, (50, 50))
bknight1_rect = bknight1.get_rect()
bknight1_rect.center = 90, 30

bknight2 = pygame.image.load("../Media/BlackKnight.png")
bknight2 = pygame.transform.scale(bknight2, (50, 50))
bknight2_rect = bknight2.get_rect()
bknight2_rect.center = 390, 30

wknight1 = pygame.image.load("../Media/WhiteKnight.png")
wknight1 = pygame.transform.scale(wknight1, (50, 50))
wknight1_rect = wknight1.get_rect()
wknight1_rect.center = 90, 450

wknight2 = pygame.image.load("../Media/WhiteKnight.png")
wknight2 = pygame.transform.scale(wknight2, (50, 50))
wknight2_rect = wknight2.get_rect()
wknight2_rect.center = 390, 450

# initiate Queens
bqueen = pygame.image.load("../Media/BlackQueen.png")
bqueen = pygame.transform.scale(bqueen, (50, 50))
bqueen_rect = bqueen.get_rect()
bqueen_rect.center = 210, 30

wqueen = pygame.image.load("../Media/WhiteQueen.png")
wqueen = pygame.transform.scale(wqueen, (50, 50))
wqueen_rect = wqueen.get_rect()
wqueen_rect.center = 210, 450

# initiate Kings
bking = pygame.image.load("../Media/BlackKing.png")
bking = pygame.transform.scale(bking, (50, 50))
bking_rect = bking.get_rect()
bking_rect.center = 270, 30

wking = pygame.image.load("../Media/WhiteKing.png")
wking = pygame.transform.scale(wking, (50, 50))
wking_rect = wking.get_rect()
wking_rect.center = 270, 450

# initiate Pawns
bpawn1 = pygame.image.load("../Media/Blackpawn.png")
bpawn1 = pygame.transform.scale(bpawn1, (50, 50))
bpawn1_rect = bpawn1.get_rect()
bpawn1_rect.center = 30, 90

bpawn2 = pygame.image.load("../Media/Blackpawn.png")
bpawn2 = pygame.transform.scale(bpawn2, (50, 50))
bpawn2_rect = bpawn2.get_rect()
bpawn2_rect.center = 90, 90

bpawn3 = pygame.image.load("../Media/Blackpawn.png")
bpawn3 = pygame.transform.scale(bpawn3, (50, 50))
bpawn3_rect = bpawn3.get_rect()
bpawn3_rect.center = 150, 90

bpawn4 = pygame.image.load("../Media/Blackpawn.png")
bpawn4 = pygame.transform.scale(bpawn4, (50, 50))
bpawn4_rect = bpawn4.get_rect()
bpawn4_rect.center = 210, 90

bpawn5 = pygame.image.load("../Media/Blackpawn.png")
bpawn5 = pygame.transform.scale(bpawn5, (50, 50))
bpawn5_rect = bpawn5.get_rect()
bpawn5_rect.center = 270, 90

bpawn6 = pygame.image.load("../Media/Blackpawn.png")
bpawn6 = pygame.transform.scale(bpawn6, (50, 50))
bpawn6_rect = bpawn6.get_rect()
bpawn6_rect.center = 330, 90

bpawn7 = pygame.image.load("../Media/Blackpawn.png")
bpawn7 = pygame.transform.scale(bpawn7, (50, 50))
bpawn7_rect = bpawn7.get_rect()
bpawn7_rect.center = 390, 90

bpawn8 = pygame.image.load("../Media/Blackpawn.png")
bpawn8 = pygame.transform.scale(bpawn8, (50, 50))
bpawn8_rect = bpawn8.get_rect()
bpawn8_rect.center = 450, 90

# white pawns:

wpawn1 = pygame.image.load("../Media/Whitepawn.png")
wpawn1 = pygame.transform.scale(wpawn1, (50, 50))
wpawn1_rect = wpawn1.get_rect()
wpawn1_rect.center = 30, 390

wpawn2 = pygame.image.load("../Media/Whitepawn.png")
wpawn2 = pygame.transform.scale(wpawn2, (50, 50))
wpawn2_rect = wpawn2.get_rect()
wpawn2_rect.center = 90, 390

wpawn3 = pygame.image.load("../Media/Whitepawn.png")
wpawn3 = pygame.transform.scale(wpawn3, (50, 50))
wpawn3_rect = wpawn3.get_rect()
wpawn3_rect.center = 150, 390

wpawn4 = pygame.image.load("../Media/Whitepawn.png")
wpawn4 = pygame.transform.scale(wpawn4, (50, 50))
wpawn4_rect = wpawn4.get_rect()
wpawn4_rect.center = 210, 390

wpawn5 = pygame.image.load("../Media/Whitepawn.png")
wpawn5 = pygame.transform.scale(wpawn5, (50, 50))
wpawn5_rect = wpawn5.get_rect()
wpawn5_rect.center = 270, 390

wpawn6 = pygame.image.load("../Media/Whitepawn.png")
wpawn6 = pygame.transform.scale(wpawn6, (50, 50))
wpawn6_rect = wpawn6.get_rect()
wpawn6_rect.center = 330, 390

wpawn7 = pygame.image.load("../Media/Whitepawn.png")
wpawn7 = pygame.transform.scale(wpawn7, (50, 50))
wpawn7_rect = wpawn7.get_rect()
wpawn7_rect.center = 390, 390

wpawn8 = pygame.image.load("../Media/Whitepawn.png")
wpawn8 = pygame.transform.scale(wpawn8, (50, 50))
wpawn8_rect = wpawn8.get_rect()
wpawn8_rect.center = 450, 390