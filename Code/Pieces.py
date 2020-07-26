import pygame
import os
import math

def square(x):
    return x * x

def distance_formula(pos1, pos2):
    # pos1 and pos2 are tuples of 2 numbers
    return math.sqrt(square(pos2[0] - pos1[0]) + square(pos2[1] - pos1[1]))
# ------------Rooks

#Initalize
brook1 = pygame.image.load("../Media/BlackRook.png")
brook1 = pygame.transform.scale(brook1,(50,50))
brook1_rect = brook1.get_rect()
brook1_rect.center = 30,30

brook2 = pygame.image.load("../Media/BlackRook.png")
brook2 = pygame.transform.scale(brook2,(50,50))
brook2_rect = brook2.get_rect()
brook2_rect.center = 450,30

wrook1 = pygame.image.load("../Media/WhiteRook.png")
wrook1 = pygame.transform.scale(wrook1,(50,50))
wrook1_rect = wrook1.get_rect()
wrook1_rect.center = 450,450

wrook2 = pygame.image.load("../Media/WhiteRook.png")
wrook2 = pygame.transform.scale(wrook2,(50,50))
wrook2_rect = wrook2.get_rect()
wrook2_rect.center = 30,450


#Valid Moves
def valid_move_rook (old_pos_name,new_pos_name):
    if old_pos_name[slice(1)] == new_pos_name[slice(1)]:
        return True
    if old_pos_name[slice(1,2)] == new_pos_name[slice(1,2)]:
        return True
    else:
        return False


# -------------------Bishops


#Initalize
bbishop1 = pygame.image.load("../Media/BlackBishop.png")
bbishop1 = pygame.transform.scale(bbishop1,(50,50))
bbishop1_rect = bbishop1.get_rect()
bbishop1_rect.center = 150,30

bbishop2 = pygame.image.load("../Media/BlackBishop.png")
bbishop2 = pygame.transform.scale(bbishop2,(50,50))
bbishop2_rect = bbishop2.get_rect()
bbishop2_rect.center = 330,30

wbishop1 = pygame.image.load("../Media/WhiteBishop.png")
wbishop1 = pygame.transform.scale(wbishop1,(50,50))
wbishop1_rect = wbishop1.get_rect()
wbishop1_rect.center = 150,450

wbishop2 = pygame.image.load("../Media/WhiteBishop.png")
wbishop2 = pygame.transform.scale(wbishop2,(50,50))
wbishop2_rect = wbishop2.get_rect()
wbishop2_rect.center = 330,450

#Valid Moves
def valid_move_bishop (old_pos_name,new_pos_name):
    fc_old = old_pos_name[slice(1)]
    sc_old = old_pos_name[slice(1,2)]
    fc_new = new_pos_name[slice(1)]
    sc_new = new_pos_name[slice(1,2)]

    for i in range(-8,9):
        if ord(fc_old) == (ord(fc_new) + i):
            if ord(sc_old) == (ord(sc_new) + i):
                return True

        if ord(fc_old) == (ord(fc_new) - i):
            if ord(sc_old) == (ord(sc_new) + i):
                return True

        if ord(fc_old) == (ord(fc_new) + i):
            if ord(sc_old) == (ord(sc_new) - i):
                return True

        if ord(fc_old) == (ord(fc_new) - i):
            if ord(sc_old) == (ord(sc_new) - i):
                return True



#-----------------Queen

#Initalize
bqueen = pygame.image.load("../Media/BlackQueen.png")
bqueen = pygame.transform.scale(bqueen,(50,50))
bqueen_rect = bqueen.get_rect()
bqueen_rect.center = 210,30

wqueen = pygame.image.load("../Media/WhiteQueen.png")
wqueen = pygame.transform.scale(wqueen,(50,50))
wqueen_rect = wqueen.get_rect()
wqueen_rect.center = 210,450

#Valid Moves
def valid_move_queen(old_pos_name,new_pos_name):
    fc_old = old_pos_name[slice(1)]
    sc_old = old_pos_name[slice(1,2)]
    fc_new = new_pos_name[slice(1)]
    sc_new = new_pos_name[slice(1,2)]

    if old_pos_name[slice(1)] == new_pos_name[slice(1)]:
        return True
    if old_pos_name[slice(1,2)] == new_pos_name[slice(1,2)]:
        return True

    for i in range(-8,9):
        if ord(fc_old) == (ord(fc_new) + i):
            if ord(sc_old) == (ord(sc_new) + i):
                return True

        if ord(fc_old) == (ord(fc_new) - i):
            if ord(sc_old) == (ord(sc_new) + i):
                return True

        if ord(fc_old) == (ord(fc_new) + i):
            if ord(sc_old) == (ord(sc_new) - i):
                return True

        if ord(fc_old) == (ord(fc_new) - i):
            if ord(sc_old) == (ord(sc_new) - i):
                return True


#-----------------------Knights

#Initalize
bknight1 = pygame.image.load("../Media/BlackKnight.png")
bknight1 = pygame.transform.scale(bknight1,(50,50))
bknight1_rect = bknight1.get_rect()
bknight1_rect.center = 90,30

bknight2 = pygame.image.load("../Media/BlackKnight.png")
bknight2 = pygame.transform.scale(bknight2,(50,50))
bknight2_rect = bknight2.get_rect()
bknight2_rect.center = 390,30

wknight1 = pygame.image.load("../Media/WhiteKnight.png")
wknight1 = pygame.transform.scale(wknight1,(50,50))
wknight1_rect = wknight1.get_rect()
wknight1_rect.center = 90,450

wknight2 = pygame.image.load("../Media/WhiteKnight.png")
wknight2 = pygame.transform.scale(wknight2,(50,50))
wknight2_rect = wknight2.get_rect()
wknight2_rect.center = 390,450

#Valid Moves
def valid_move_knight(old_pos_name,new_pos_name):
    fc_old = old_pos_name[slice(1)]
    sc_old = old_pos_name[slice(1,2)]
    fc_new = new_pos_name[slice(1)]
    sc_new = new_pos_name[slice(1,2)]

    if ord(fc_old) == (ord(fc_new) + 2):
        if ord(sc_old) == (ord(sc_new) + 1):
            return True

    if ord(fc_old) == (ord(fc_new) - 2):
        if ord(sc_old) == (ord(sc_new) + 1):
            return True

    if ord(fc_old) == (ord(fc_new) + 2):
        if ord(sc_old) == (ord(sc_new) - 1):
            return True

    if ord(fc_old) == (ord(fc_new) - 2):
        if ord(sc_old) == (ord(sc_new) - 1):
            return True

    if ord(fc_old) == (ord(fc_new) + 1):
        if ord(sc_old) == (ord(sc_new) + 2):
            return True

    if ord(fc_old) == (ord(fc_new) - 1):
        if ord(sc_old) == (ord(sc_new) + 2):
            return True

    if ord(fc_old) == (ord(fc_new) + 1):
        if ord(sc_old) == (ord(sc_new) - 2):
            return True

    if ord(fc_old) == (ord(fc_new) - 1):
        if ord(sc_old) == (ord(sc_new) - 2):
            return True

    else:
        return False


# --------------------Kings

#Initalize
bking = pygame.image.load("../Media/BlackKing.png")
bking = pygame.transform.scale(bking,(50,50))
bking_rect = bking.get_rect()
bking_rect.center = 270,30

wking = pygame.image.load("../Media/WhiteKing.png")
wking = pygame.transform.scale(wking,(50,50))
wking_rect = wking.get_rect()
wking_rect.center = 270,450

#Valid Moves
def valid_move_king(old_pos_name,new_pos_name):
    fc_old = old_pos_name[slice(1)]
    sc_old = old_pos_name[slice(1,2)]
    fc_new = new_pos_name[slice(1)]
    sc_new = new_pos_name[slice(1,2)]

    if ord(fc_old) == (ord(fc_new) + 1):
        if ord(sc_old) == (ord(sc_new)):
            return True

    if ord(fc_old) == (ord(fc_new) - 1):
        if ord(sc_old) == (ord(sc_new)):
            return True

    if ord(fc_old) == (ord(fc_new)):
        if ord(sc_old) == (ord(sc_new) - 1):
            return True

    if ord(fc_old) == (ord(fc_new) ):
        if ord(sc_old) == (ord(sc_new) + 1):
            return True

    if ord(fc_old) == (ord(fc_new) + 1):
        if ord(sc_old) == (ord(sc_new) + 1):
            return True

    if ord(fc_old) == (ord(fc_new) - 1):
        if ord(sc_old) == (ord(sc_new) + 1):
            return True

    if ord(fc_old) == (ord(fc_new) + 1):
        if ord(sc_old) == (ord(sc_new) - 1):
            return True

    if ord(fc_old) == (ord(fc_new) - 1):
        if ord(sc_old) == (ord(sc_new) - 1):
            return True

    else:
        return False


# ---------------------Pawns

#Initialize
#blackpawns:
bpawn1 = pygame.image.load("../Media/BlackPawn.png")
bpawn1 = pygame.transform.scale(bpawn1,(50,50))
bpawn1_rect = bpawn1.get_rect()
bpawn1_rect.center = 30,90

bpawn2 = pygame.image.load("../Media/BlackPawn.png")
bpawn2 = pygame.transform.scale(bpawn2,(50,50))
bpawn2_rect = bpawn2.get_rect()
bpawn2_rect.center = 90,90

bpawn3 = pygame.image.load("../Media/BlackPawn.png")
bpawn3 = pygame.transform.scale(bpawn3,(50,50))
bpawn3_rect = bpawn3.get_rect()
bpawn3_rect.center = 150,90

bpawn4 = pygame.image.load("../Media/BlackPawn.png")
bpawn4 = pygame.transform.scale(bpawn4,(50,50))
bpawn4_rect = bpawn4.get_rect()
bpawn4_rect.center = 210,90

bpawn5 = pygame.image.load("../Media/BlackPawn.png")
bpawn5 = pygame.transform.scale(bpawn5,(50,50))
bpawn5_rect = bpawn5.get_rect()
bpawn5_rect.center = 270,90

bpawn6 = pygame.image.load("../Media/BlackPawn.png")
bpawn6 = pygame.transform.scale(bpawn6,(50,50))
bpawn6_rect = bpawn6.get_rect()
bpawn6_rect.center = 330,90

bpawn7 = pygame.image.load("../Media/BlackPawn.png")
bpawn7 = pygame.transform.scale(bpawn7,(50,50))
bpawn7_rect = bpawn7.get_rect()
bpawn7_rect.center = 390,90

bpawn8 = pygame.image.load("../Media/BlackPawn.png")
bpawn8 = pygame.transform.scale(bpawn8,(50,50))
bpawn8_rect = bpawn8.get_rect()
bpawn8_rect.center = 450,90
#white pawns:
wpawn1 = pygame.image.load("../Media/WhitePawn.png")
wpawn1 = pygame.transform.scale(wpawn1,(50,50))
wpawn1_rect = wpawn1.get_rect()
wpawn1_rect.center = 30,390

wpawn2 = pygame.image.load("../Media/WhitePawn.png")
wpawn2 = pygame.transform.scale(wpawn2,(50,50))
wpawn2_rect = wpawn2.get_rect()
wpawn2_rect.center = 90,390

wpawn3 = pygame.image.load("../Media/WhitePawn.png")
wpawn3 = pygame.transform.scale(wpawn3,(50,50))
wpawn3_rect = wpawn3.get_rect()
wpawn3_rect.center = 150,390

wpawn4 = pygame.image.load("../Media/WhitePawn.png")
wpawn4 = pygame.transform.scale(wpawn4,(50,50))
wpawn4_rect = wpawn4.get_rect()
wpawn4_rect.center = 210,390

wpawn5 = pygame.image.load("../Media/WhitePawn.png")
wpawn5 = pygame.transform.scale(wpawn5,(50,50))
wpawn5_rect = wpawn5.get_rect()
wpawn5_rect.center = 270,390

wpawn6 = pygame.image.load("../Media/WhitePawn.png")
wpawn6 = pygame.transform.scale(wpawn6,(50,50))
wpawn6_rect = wpawn6.get_rect()
wpawn6_rect.center = 330,390

wpawn7 = pygame.image.load("../Media/WhitePawn.png")
wpawn7 = pygame.transform.scale(wpawn7,(50,50))
wpawn7_rect = wpawn7.get_rect()
wpawn7_rect.center = 390,390

wpawn8 = pygame.image.load("../Media/WhitePawn.png")
wpawn8 = pygame.transform.scale(wpawn8,(50,50))
wpawn8_rect = wpawn8.get_rect()
wpawn8_rect.center = 450,390

#Valid Moves
def valid_move_bpawn(old_pos_name, new_pos_name, s_pos_o, s_pos_n):        # Selected-POSition-Old/New
   if old_pos_name[slice(1)] == new_pos_name[slice(1)]:
       if  distance_formula(s_pos_n, s_pos_o) == 120:
           if old_pos_name[slice(1, 2)] == '7':
               return True
       elif distance_formula(s_pos_n, s_pos_o) == 60:
           if ord(old_pos_name[slice(1, 2)]) > ord(new_pos_name[slice(1, 2)]):
               return True
   else:
       return False

def valid_move_wpawn(old_pos_name, new_pos_name, s_pos_o, s_pos_n):        # Selected-POSition-Old/New
   if old_pos_name[slice(1)] == new_pos_name[slice(1)]:
       if  distance_formula(s_pos_n, s_pos_o) == 120:
           if old_pos_name[slice(1, 2)] == '2':
               return True
       elif distance_formula(s_pos_n, s_pos_o) == 60:
           if ord(old_pos_name[slice(1, 2)]) < ord(new_pos_name[slice(1, 2)]):
               return True
   else:
       return False
